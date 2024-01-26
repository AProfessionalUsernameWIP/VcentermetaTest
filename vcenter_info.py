"""
Script Name: vcenter_info.py
Author: Alexander Wojcik
Date: 2023-01-25 13:15:00
Description: This script connects to a VMware vCenter server, retrieves information about virtual machines (VMs) in a specified cluster, and prints this information in a structured JSON format. It is designed to run on both Windows and Linux environments.
"""
import atexit
import json
import sys
import os
import ssl
from configparser import ConfigParser, NoSectionError, NoOptionError
from pyVim import connect

def get_config(config_path):
    # Load and validate config from file, return as dict
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    config = ConfigParser()
    config.read(config_path)
    
    try:
        vcenter_config = {
            'vcenter_host': config.get('vCenter', 'host'),
            'vcenter_user': config.get('vCenter', 'user'),
            'vcenter_password': config.get('vCenter', 'password'),
            'cluster_name': config.get('Cluster', 'name')
        }
    except (NoSectionError, NoOptionError) as e:
        raise ValueError(f"Missing or invalid configuration: {e}")

    return vcenter_config

def connect_to_vcenter(credentials):
    # Establish connection to vCenter, return service content
    try:
        sslContext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)  # Handles TLS error
        sslContext.check_hostname = False  # Required to set verify mode to CERT_NONE
        sslContext.verify_mode = ssl.CERT_NONE  # Disables SSL cert checking
        service_instance = connect.SmartConnect(host=credentials['vcenter_host'],
                                                     user=credentials['vcenter_user'],
                                                     pwd=credentials['vcenter_password'],
                                                     port=443,
                                                     sslContext=sslContext)
        atexit.register(connect.Disconnect, service_instance)
        return service_instance.RetrieveContent()
    except connect.SmartConnectException as e:
        raise ConnectionError(f"Could not connect to vCenter: {e}")

def get_cluster_hosts(content, cluster_name):
    # Retrieve hosts from specified cluster
    for datacenter in content.rootFolder.childEntity:
        if not hasattr(datacenter, 'hostFolder'):
            raise AttributeError("Datacenter does not have a 'hostFolder' attribute")

        for cluster in datacenter.hostFolder.childEntity:
            if cluster.name == cluster_name:
                return cluster.host if cluster.host else None

    raise ValueError(f"Cluster '{cluster_name}' not found")

def get_vms_info(hosts):
    # Get VM information from hosts
    if not hosts:
        print("No hosts found in the cluster.")
        return None

    vms_data = []
    for host in hosts:
        if not host.vm:
            print(f"No VMs found on host: {host.name}")
            continue

        for vm in host.vm:
            vm_info = {
                "name": vm.summary.config.name,
                "creator": "unknown",
                "creation_date": str(vm.config.createDate),
                "resource_allocation": {
                    "cpu": vm.config.hardware.numCPU,
                    "memory": vm.config.hardware.memoryMB
                }
            }
            vms_data.append(vm_info)

    if not vms_data:
        print("No VMs found in any of the hosts.")
        return None

    return vms_data

def main(config_path):
    try:
        config = get_config(config_path)
        content = connect_to_vcenter(config)
        hosts = get_cluster_hosts(content, config['cluster_name'])

        if hosts is None:
            print("Cluster has no hosts.")
            return

        vms_data = get_vms_info(hosts)

        if vms_data:
            print(json.dumps(vms_data, indent=4))
        else:
            print("Exiting as no VM data could be retrieved.")
    except (FileNotFoundError, ValueError, ConnectionError, AttributeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_config_file>", file=sys.stderr)
        sys.exit(1)
    config_file_path = sys.argv[1]
    main(config_file_path)