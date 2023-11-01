#!/usr/bin/python3

import boto3
import json

def get_ec2_inventory():
    ec2 = boto3.client('ec2', region_name='us-west-2')  # Replace with your AWS region

    response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Environment', 'Values': ['my_env']}
        ]
    )
    reservations = response['Reservations']

    inventory = {
        '_meta': {
            'hostvars': {}
        },
        'ec2_instances': {
            'hosts': [],
            'vars': {}
        }
    }

    for reservation in reservations:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            public_ip = instance.get('PublicIpAddress', 'unknown')
            private_ip = instance.get('PrivateIpAddress', 'unknown')

            inventory['ec2_instances']['hosts'].append(public_ip)
            inventory['_meta']['hostvars'][public_ip] = {
                'ansible_host': public_ip,
                'private_ip': private_ip,
                # Add more host-specific variables as needed
            }

    return inventory

if __name__ == '__main__':
    inventory = get_ec2_inventory()
    print(json.dumps(inventory))


