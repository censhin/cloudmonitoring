#!/usr/bin/env python

import requests
import json


class CloudMonitoring:
    """
    Cloud Monitoring API bindings. Written according to the
    specifications in the Rackspace Cloud Developer and API
    Documentation. Complete functionality described in the
    Cloud Monitoring API is not implemented at this time.
    """
    def __init__(self, username, apiKey):
        """
        Auth to account, and initialize class variables.
        """
        url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
        headers = {'Content-type':'application/json'}
        credentials = {'username':username, 'apiKey':apiKey}
        payload = {'auth':{'RAX-KSKEY:apiKeyCredentials':credentials}}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        d = r.json
        self.token = d['access']['token']['id']
        self.account = d['access']['token']['tenant']['id']
        self.M_URL = 'https://monitoring.api.rackspacecloud.com/v1.0'
        self.INFO_URL = '%s/%s/agents' % (self.M_URL, self.account)
        self.headers = {'X-Auth-Token': self.token,
                'Accept': 'application/json'}

    def create_entity(self):
        """
        Creates a Cloud Monitoring entity.
        """
        url = '%s/%s/entities' % (self.M_URL, self.account)
        headers = {'X-Auth-Token': self.token,
                'Content-Type': 'application/json',
                'Accept': 'application/json'}
        payload = {'ip_addresses': {'default': '192.0.2.15'},
                'label': 'test', 'metadata': {}}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        return r.json

    def list_entities(self):
        """
        Lists Cloud Monitoring entities installed on all servers,
        and their information.
        """
        url = '%s/%s/entities' % (self.M_URL, self.account)
        r = requests.get(url, headers=self.headers)
        return r.json

    def list_aids(self):
        """
        Lists all Cloud Monitoring entity's agent ID values.
        """
        aids = []
        e_list = self.list_entities()
        value_list = e_list['values']
        for i in range(len(value_list)):
            if value_list[i]['agent_id'] != None:
                aids.append(value_list[i]['agent_id'])
        return aids

    def list_ipv4s(self):
        """
        Lists all Cloud Monitoring entity's IPv4 values.
        """
        ipv4s = []
        e_list = self.list_entities()
        value_list = e_list['values']
        for i in range(len(value_list)):
            if value_list[i]['ip_addresses'] != None:
                if 'public0_v4' in value_list[i]['ip_addresses']:
                    ipv4s.append(value_list[i]['ip_addresses']['public0_v4'])
                elif 'public1_v4' in value_list[i]['ip_addresses']:
                    ipv4s.append(value_list[i]['ip_addresses']['public1_v4'])
        return ipv4s

    def get_aids_by_ipv4(self):
        """
        Associates Cloud Monitoring entity's agent ID values with
        their IPv4 values, and returns a dictionary containing
        this information. IPv4 values are the dictionary's keys,
        and the agent ID values are those keys' values.
        """
        d = {}
        aids = []
        ipv4s = []
        e_list = self.list_entities()
        value_list = e_list['values']
        for i in range(len(value_list)):
            if value_list[i]['agent_id'] != None and value_list[i]['ip_addresses'] != None:
                aids.append(value_list[i]['agent_id'])
                if 'public0_v4' in value_list[i]['ip_addresses']:
                    ipv4s.append(value_list[i]['ip_addresses']['public0_v4'])
                elif 'public1_v4' in value_list[i]['ip_addresses']:
                    ipv4s.append(value_list[i]['ip_addresses']['public1_v4'])
        for a, i in zip(aids, ipv4s):
            d[i] = a
        return d

    def list_monitoring_zones(self):
        """
        Lists all Cloud Monitoring's zones.
        """
        url = '%s/%s/monitoring_zones' % (self.M_URL, self.account)
        headers = {'X-Auth-Token': self.token, 'Accept': 'application/json'}
        r = requests.get(url, headers=self.headers)
        return r.json

    def get_cpu_info(self, aid):
        """
        Returns the specified agent's CPU information.
        """
        url = '%s/%s/host_info/cpus' % (self.INFO_URL, aid)
        r = requests.get(url, headers=self.headers)
        return r.json

    def get_disk_info(self, aid):
        """
        Returns the specified agent's disk information.
        """
        url = '%s/%s/host_info/disks' % (self.INFO_URL, aid)
        r = requests.get(url, headers=self.headers)
        return r.json

    def get_fs_info(self, aid):
        """
        Returns the specified agent's file system information.
        """
        url = '%s/%s/host_info/filesystems' % (self.INFO_URL, aid)
        r = requests.get(url, headers=self.headers)
        return r.json

    def get_memory_info(self, aid):
        """
        Returns the specified agent's memory information.
        """
        url = '%s/%s/host_info/memory' % (self.INFO_URL, aid)
        r = requests.get(url, headers=self.headers)
        return r.json

    def get_network_info(self, aid):
        """
        Returns the specified agent's network information.
        """
        url = '%s/%s/host_info/network_interfaces' % (self.INFO_URL, aid)
        r = requests.get(url, headers=self.headers)
        return r.json

    def get_proc_info(self, aid):
        """
        Returns the specified agent's process information.
        """
        url = '%s/%s/host_info/processes' % (self.INFO_URL, aid)
        r = requests.get(url, headers=self.headers)
        return r.json

    def get_sys_info(self, aid):
        """
        Returns the specified agent's system information.
        """
        url = '%s/%s/host_info/system' % (self.INFO_URL, aid)
        r = requests.get(url, headers=self.headers)
        return r.json

    def get_who_info(self, aid):
        """
        Returns the usernames of users logged into the
        specified agent's server.
        """
        url = '%s/%s/host_info/who' % (self.INFO_URL, aid)
        r = requests.get(url, headers=self.headers)
        return r.json
