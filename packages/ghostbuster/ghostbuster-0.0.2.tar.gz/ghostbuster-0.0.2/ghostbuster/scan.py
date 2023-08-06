#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This CLI tool can be used to scan for dangling elastic IPs in your AWS accounts by correlating data
betwen Route53 records and Elastic IPs / IPs in your AWS account.

.. currentmodule:: assetnote_cli.cli
.. moduleauthor:: shubham_shah <sshah@assetnote.io>
"""
import csv
import datetime
import requests
import click
from .__init__ import Info, pass_info
import boto3
import CloudFlare
import awsipranges
from slack_sdk.webhook import WebhookClient


@click.group(
    help="Commands that help you scan your AWS account for dangling elastic IPs"
)
@click.pass_context
def cli(ctx: click.Context):
    """CLI handler for scanning actions"""
    pass


# logic taken from https://github.com/jacobfgrant/route53-lambda-backup


def get_route53_hosted_zones(route53, next_zone=None):
    """Recursively returns a list of hosted zones in Amazon Route 53."""
    if next_zone:
        response = route53.list_hosted_zones_by_name(
            DNSName=next_zone[0], HostedZoneId=next_zone[1]
        )
    else:
        response = route53.list_hosted_zones_by_name()
    hosted_zones = response["HostedZones"]
    # if response is truncated, call function again with next zone name/id
    if response["IsTruncated"]:
        hosted_zones += get_route53_hosted_zones(
            route53, (response["NextDNSName"], response["NextHostedZoneId"])
        )
    return hosted_zones


def get_route53_zone_records(route53, zone_id, next_record=None):
    """Recursively returns a list of records of a hosted zone in Route 53."""
    if next_record:
        response = route53.list_resource_record_sets(
            HostedZoneId=zone_id,
            StartRecordName=next_record[0],
            StartRecordType=next_record[1],
        )
    else:
        response = route53.list_resource_record_sets(HostedZoneId=zone_id)
    zone_records = response["ResourceRecordSets"]
    # if response is truncated, call function again with next record name/id
    if response["IsTruncated"]:
        zone_records += get_route53_zone_records(
            route53, zone_id, (response["NextRecordName"], response["NextRecordType"])
        )
    return zone_records


def get_record_value(record):
    """Return a list of values for a hosted zone record."""
    # test if record's value is Alias or dict of records
    try:
        value = [
            ":".join(
                [
                    "ALIAS",
                    record["AliasTarget"]["HostedZoneId"],
                    record["AliasTarget"]["DNSName"],
                ]
            )
        ]
    except KeyError:
        value = []
        for v in record["ResourceRecords"]:
            value.append(v["Value"])
    return value


def try_record(test, record):
    """Return a value for a record"""
    # test for Key and Type errors
    try:
        value = record[test]
    except KeyError:
        value = ""
    except TypeError:
        value = ""
    return value


@click.option(
    "--regions", default="us-east-1", help="Comma delimited list of regions to run on."
)
@click.option(
    "--exclude", default="", help="Comma delimited list of profile names to exclude."
)
@click.option(
    "--allregions",
    default=False,
    is_flag=True,
    help="Run on all regions.",
)
@click.option(
    "--cloudflaretoken",
    default="",
    help="Pull DNS records from Cloudflare, provide a CF API token.",
)
@click.option(
    "--records",
    required=False,
    type=click.Path(exists=True),
    help="Manually specify DNS records to check against. Ghostbuster will check these IPs after checking retrieved DNS records. See records.csv for an example.",
)
@click.option(
    "--slackwebhook",
    default="",
    help="Specify a Slack webhook URL to send notifications about potential takeovers.",
)
@cli.command(help="Scan for dangling elastic IPs inside your AWS accounts.")
@pass_info
def dangling(
    _: Info,
    regions: str,
    exclude: str,
    allregions: bool,
    cloudflaretoken: str,
    records: str,
    slackwebhook: str,
):
    """Scan for dangling elastic IPs inside your AWS accounts."""
    session = boto3.Session()
    profiles = session.available_profiles
    if exclude != "":
        exclude_list = exclude.split(",")
        for excluded_profile in exclude_list:
            profiles.remove(excluded_profile)
    dns_records = []
    # collection of records from cloudflare
    if cloudflaretoken != "":
        click.echo("Obtaining all zone names from Cloudflare.")
        cf = CloudFlare.CloudFlare(token=cloudflaretoken, raw=True)
        # get zone names
        cloudflare_zones = []
        try:
            page_number = 0
            while True:
                page_number += 1
                raw_results = cf.zones.get(
                    params={"per_page": 100, "page": page_number}
                )
                zones = raw_results["result"]
                for zone in zones:
                    zone_id = zone["id"]
                    zone_name = zone["name"]
                    cloudflare_zones.append({"name": zone_name, "id": zone_id})
                total_pages = raw_results["result_info"]["total_pages"]
                if page_number == total_pages:
                    break
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit("Failed to retreive zones %d %s - api call failed" % (e, e))

        click.echo("Obtaining DNS A records for all zones from Cloudflare.")
        # get dns records for zones
        for zone in cloudflare_zones:
            try:
                page_number = 0
                while True:
                    page_number += 1
                    raw_results = cf.zones.dns_records.get(
                        zone["id"], params={"per_page": 100, "page": page_number}
                    )
                    cf_dns_records = raw_results["result"]
                    for record in cf_dns_records:
                        if record.get("content"):
                            if record["type"] == "A":
                                dns_records.append(
                                    {
                                        "name": record["name"],
                                        "records": [record["content"]],
                                    }
                                )
                    total_pages = raw_results["result_info"]["total_pages"]
                    if page_number == total_pages:
                        break
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                exit("Failed to retreive DNS records %d %s - api call failed" % (e, e))

        click.echo("Obtained {0} DNS A records so far.".format(len(dns_records)))

    # collection of records from r53
    for profile in profiles:
        profile_session = boto3.session.Session(profile_name=profile)
        route53 = profile_session.client("route53")
        click.echo(
            "Obtaining Route53 hosted zones for AWS profile: {0}.".format(profile)
        )
        hosted_zones = get_route53_hosted_zones(route53)
        for zone in hosted_zones:
            zone_records = get_route53_zone_records(route53, zone["Id"])
            for record in zone_records:
                if record["Type"] == "A":
                    # we aren't interested in alias records
                    if record.get("AliasTarget"):
                        # skip
                        pass
                    else:
                        a_records = []
                        for r53value in record["ResourceRecords"]:
                            a_records.append(r53value["Value"])
                        r53_obj = {"name": record["Name"], "records": a_records}
                        dns_records.append(r53_obj)

    click.echo("Obtained {0} DNS A records so far.".format(len(dns_records)))

    # collection of IPs
    if allregions:
        ec2 = boto3.client("ec2")
        aws_regions = [
            region["RegionName"] for region in ec2.describe_regions()["Regions"]
        ]
    else:
        aws_regions = regions.split(",")
    elastic_ips = []
    # collect elastic compute addresses / EIPs for all regions
    for region in aws_regions:
        for profile in profiles:
            click.echo(
                "Obtaining EIPs for region: {}, profile: {}".format(region, profile)
            )
            profile_session = boto3.session.Session(profile_name=profile)
            client = profile_session.client("ec2", region_name=region)
            # super annoying, boto3 doesn't have a native paginator class for describe_addresses
            while True:
                addresses_dict = []
                if addresses_dict and "NextToken" in addresses_dict:
                    addresses_dict = client.describe_addresses(
                        NextToken=addresses_dict["NextToken"]
                    )
                else:
                    addresses_dict = client.describe_addresses()
                for eip_dict in addresses_dict["Addresses"]:
                    elastic_ips.append(eip_dict["PublicIp"])
                if "NextToken" not in addresses_dict:
                    break

            click.echo(
                "Obtaining IPs for network interfaces for region: {}, profile: {}".format(
                    region, profile
                )
            )
            nic_paginator = client.get_paginator("describe_network_interfaces")
            for resp in nic_paginator.paginate():
                for interface in resp.get("NetworkInterfaces", []):
                    if interface.get("Association"):
                        nic_public_ip = interface["Association"]["PublicIp"]
                        elastic_ips.append(nic_public_ip)

    unique_ips = list(set(elastic_ips))
    click.echo("Obtained {0} unique elastic IPs from AWS.".format(len(unique_ips)))

    dns_ec2_ips = []
    # find all DNS records that point to EC2 IP addresses
    aws_ip_ranges = awsipranges.get_ranges()
    for record_set in dns_records:
        for record in record_set["records"]:
            aws_metadata = aws_ip_ranges.get(record)
            if aws_metadata:
                for service in aws_metadata.services:
                    if service == "EC2":
                        dns_ec2_ips.append(record_set)
    takeovers = []
    # check to see if any of the record sets we have, we don't own the elastic IPs
    for record_set in dns_ec2_ips:
        for record in record_set["records"]:
            if record not in elastic_ips:
                takeovers.append(record_set)
                click.echo("Takeover possible: {}".format(record_set))

    # check if manually specified A records exist in AWS acc (eips/public ips)
    if records:
        with open(records, "r") as fp:
            csv_reader = csv.DictReader(fp)
            for row in csv_reader:
                aws_metadata = aws_ip_ranges.get(row["record"])
                if aws_metadata:
                    for service in aws_metadata.services:
                        if service == "EC2":
                            if row["record"] not in elastic_ips:
                                takeover_obj = {
                                    "name": row["name"],
                                    "records": [row["record"]],
                                }
                                takeovers.append(takeover_obj)
                                click.echo("Takeover possible: {}".format(takeover_obj))

    # send slack webhooks, with retries incase of 429s
    if slackwebhook != "":
        webhook = WebhookClient(url=slackwebhook)
        from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler

        rate_limit_handler = RateLimitErrorRetryHandler(max_retry_count=1)
        webhook.retry_handlers.append(rate_limit_handler)
        for takeover in takeovers:
            payload = "Potential AWS Elastic IP takeover: {} Records: {}".format(
                takeover["name"], takeover["records"]
            )
            _ = webhook.send(text=payload)
