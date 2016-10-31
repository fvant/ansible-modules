from jinja2.utils import soft_unicode

import boto3
import re

def _string_sanity_check(string):
    if string is None:
        return ''
    if not isinstance(string, basestring):
        return str(string)
    return string

def get_subnets(value, tag_key, tag_value, return_key='id'):
    # return an attribute for all subnets that match
    subnets = []
    for item in value:
      for key, value in item['tags'].iteritems():
        if key.lower() == tag_key.lower() and value.lower().startswith(tag_value.lower()):
          subnets.append(item[return_key])

    return subnets

def get_subnets_full(value, tag_key, tag_value):
    # return subnets that match
    subnets = []
    for item in value:
      for key, value in item['tags'].iteritems():
        if key.lower() == tag_key.lower() and value.lower() == tag_value.lower():
          subnets.append(item)

    return subnets

#
# Use this one in context files.
#
def get_dns_zone(zone_name, tag_key = None):

    zone_name = _string_sanity_check(zone_name)

    if not (zone_name.endswith('.')):
        zone_name += '.'

    if tag_key:
        tag_key = tag_key.lower()

    try:
        client = boto3.client('route53')
        zones = client.list_hosted_zones()

        for zone in zones['HostedZones']:
            if (zone['Name'] != zone_name):
                continue

            if (tag_key == 'id'):
                return zone['Id'].split('/')[-1]
            elif tag_key == 'name':
                return zone['Name']
            elif tag_key == 'private':
                return zone['Config']['PrivateZone']

            return zone
    except:
        raise AnsibleError('Error getting Route53 Zone info')

    return None

#
# Use this one in combination with:
# $ aws route53 list-hosted-zones-by-name --dns-name {{ vpc_dns_zone }} --max-items 2 --output json
#
def get_dns_zone_cli(value, zone_name):
    if not (zone_name.endswith('.')):
        zone_name += '.'

    for zone in value['HostedZones']:
        if zone['Name'] == zone_name:
            return zone


class FilterModule(object):

    def filters(self):
        return {
            'get_subnets': get_subnets,
            'get_subnets_full': get_subnets_full,
            'get_dns_zone_cli': get_dns_zone_cli,
            'get_dns_zone': get_dns_zone
        }
