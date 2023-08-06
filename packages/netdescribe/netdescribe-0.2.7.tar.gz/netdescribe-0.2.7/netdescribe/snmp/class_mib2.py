#!/usr/bin/env python3

#   Copyright [2018-2022] [James Fleming <james@electronic-quill.net]
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Generic SNMP MIB-II object
"""

# pylint: disable=wrong-import-order

# Third-party libraries
import pysnmp
from typing import Dict, List, Optional, Union

# Local modules
from netdescribe.snmp.snmp_functions import SnmpDatum, snmp_get, snmp_walk
from netdescribe.snmp.snmp_structures import Interface, IpAddr, IpAddress, SystemData
from netdescribe.snmp.snmp_structures import BgpInstance, BgpPeerEntry
import netdescribe.utils

# Built-in modules
import collections
import ipaddress
import json
import logging  # For type annotations
import re


# Sorry, pylint, but it's just this complex
# pylint: disable=too-many-instance-attributes
class Mib2:
    '''
    Generic device conforming to SNMP MIB-II.
    Attribute values are left as the datatypes returned by pysnmp wherever feasible,
    and converted to other formats as late as possible.
    '''

    # It just has that many attributes to track. Cope.
    # pylint: disable=too-many-arguments
    def __init__(self,
                 target: pysnmp.hlapi.UdpTransportTarget,
                 engine: pysnmp.hlapi.SnmpEngine,
                 auth: pysnmp.hlapi.CommunityData,
                 logger: logging.Logger,
                 sys_object_id: Optional[str] = None):
        # SNMP and overhead parameters
        self.target = target
        self.engine = engine
        self.auth = auth
        self.logger = logger
        self.default_mib: str = 'SNMPv2-MIB'
        # Things that can vary between subclasses.
        # Enables us to, e.g, drop 'ifAlias' when querying Brocade MLX to work around Ironware's
        # broken implementation.
        # Device attributes
        self.system_data: Optional[SystemData] = None
        self._interfaces: List[Interface] = []
        self._ipaddrs: List[IpAddr] = []
        self._ipaddresses: List[IpAddress] = []
        self._sys_object_id: Optional[str] = sys_object_id
        # Structure of bgp4 dict:
        # key = instance-name (default is "default")
        # value = hash:
        # - 'instance' = BgpInstance namedtuple
        # - 'peers' = list of BgpPeerEntry namedtuples
        # Protected attribute, to capture it if it's supplied
        self._bgp4: Optional[Dict[str, Dict[BgpInstance, List[BgpPeerEntry]]]] = None

    def __get(self,
              attribute: str,
              mib: Optional[str] = None,
              auth: Optional[pysnmp.hlapi.CommunityData] = None,
              target: Optional[pysnmp.hlapi.UdpTransportTarget] = None) -> str:
        'Convenience function for performing SNMP GET'
        # Figure out the optional parameters
        # auth
        if auth:
            authz = auth
        else:
            authz = self.auth
        # target
        if target:
            targetz = target
        else:
            targetz = self.target
        # mib
        if mib:
            mibz = mib
        else:
            mibz = self.default_mib
        # Now fetch the data
        return snmp_get(self.engine, authz, targetz, mibz, attribute, self.logger)

    def __walk(self,
               table: str,
               row: str,
               auth: Optional[pysnmp.hlapi.CommunityData] = None,
               target: Optional[pysnmp.hlapi.UdpTransportTarget] = None) -> List[SnmpDatum]:
        'Convenience function for performing SNMP WALK'
        # Figure out the optional parameters
        if auth:
            authz = auth
        else:
            authz = self.auth
        if target:
            targetz = target
        else:
            targetz = self.target
        # Now fetch the data
        return snmp_walk(self.engine, authz, targetz, table, row, self.logger)

    def identify(self) -> SystemData:
        '''
        Return an snmp.snmp_structures.systemData namedtuple.
        Memoised method: if the object already has this data, it won't re-poll the device.
        '''
        hostname = self.target.transportAddr[0]
        self.logger.debug('Returning basic details for %s', hostname)
        # If this data isn't already present, retrieve and set it.
        if not self.system_data:
            # Pre-fetch the values
            self.logger.debug('system_data attribute is null; polling the device for details.')
            sys_descr = self.__get(attribute='sysDescr')
            sys_name = self.__get(attribute='sysName')
            sys_location = str(self.__get(attribute='sysLocation')).strip('"')
            # Inject this one straight into `self` because it's a defined attribute
            if not self._sys_object_id:
                self._sys_object_id = self.__get(attribute='sys_object_id')
            # Assemble the return value, and inject it into `self`
            self.system_data = SystemData(sysName=sys_name,
                                          sysDescr=sys_descr,
                                          sysObjectID=str(self._sys_object_id),
                                          sysLocation=sys_location)
            self.logger.debug('Retrieved data %s', self.system_data)
        # Return the cached data
        return self.system_data

    def interfaces(self) -> List[Interface]:
        '''
        Return a list of Interface namedtuples.
        If self.interfaces already contains a non-empty list, it will simply return that list.
        If not, it will query the device to populate it first.
        '''
        # If it's not already recorded in this object, fetch the contents into it first.
        # Note: this approach doesn't work on Linux, because ifNumber isn't implemented there.
        if not self._interfaces:
            # Fetch the interface data into an intermediate accumulator.
            # Structure of the dict: {ifIndex: { attributename: value }}
            interfaces: Dict[int, Dict] = {}
            # __walk returns a list of SnmpDatum named tuples
            self.logger.debug('Walking IF-MIB::ifName')
            for iface in self.__walk('IF-MIB', 'ifName'):
                index = int(iface.oid[-1])
                val = str(iface.value)
                self.logger.debug(f'Initialising index {index} with value "{val}" of type {type(val)}.')
                interfaces[index] = {'ifName': val }
            # ifDescr
            self.logger.debug('Walking IF-MIB::ifDescr')
            for iface in self.__walk('IF-MIB', 'ifDescr'):
                index = int(iface.oid[-1])
                val = str(iface.value)
                self.logger.debug(f'Updating index {index} with ifDescr value "{val}" of type {type(val)}.')
                interfaces[index]['ifDescr'] = val
            # ifAlias
            for iface in self.__walk('IF-MIB', 'ifAlias'):
                interfaces[int(iface.oid[-1])]['ifAlias'] = str(iface.value)
            # ifType
            for iface in self.__walk('IF-MIB', 'ifType'):
                interfaces[int(iface.oid[-1])]['ifType'] = str(iface.value)
            # ifPhysAddress
            for iface in self.__walk('IF-MIB', 'ifPhysAddress'):
                interfaces[int(iface.oid[-1])]['ifPhysAddress'] = str(iface.value)
            # ifSpeed
            for iface in self.__walk('IF-MIB', 'ifSpeed'):
                interfaces[int(iface.oid[-1])]['ifSpeed'] = int(iface.value)
            # ifHighSpeed
            for iface in self.__walk('IF-MIB', 'ifHighSpeed'):
                interfaces[int(iface.oid[-1])]['ifHighSpeed'] = int(iface.value)
            # Having retrieved the data, create the list
            interfacelist: List[Interface] = []
            for index, details in interfaces.items():
                interfacelist.append(Interface(ifIndex=index,
                                               ifName=details['ifName'],
                                               ifDescr=details['ifDescr'],
                                               ifType=details['ifType'],
                                               ifSpeed=details['ifSpeed'],
                                               ifPhysAddress=details['ifPhysAddress'],
                                               ifHighSpeed=details['ifHighSpeed'],
                                               ifAlias=details['ifAlias']))
            self._interfaces = interfacelist
        # Return the data cached in the object
        return self._interfaces

    def populate_ip_addresses(self) -> bool:
        '''
        Fetch the address data for this device, and populate self._ipaddresses with it.
        Polls the preferred, but less widely-implemented, ipAddressTable.
        Covers both IPv4 and IPv6.
        Essentially a helper-function for ip_addresses().
        '''
        self.logger.debug('Retrieving IP addresses from ipAddressTable')
        # Create an intermediate accumulator for building up a list of IpAddress namedtuples
        # because the necessary data is distributed across several OIDs.
        acc: Dict[str, Dict[str, Union[str, int]]] = {}
        # acc structure (after all passes are complete):
        # {IP Address: {
        #     'ipAddressIfIndex': SNMP index
        #     'protocol' = IP protocol version, i.e. ipv4 or ipv6
        #     'prefixlength' = integer, 0-32
        #     'type' = address type: unicast, multicast, anycast or broadcast
        #     }
        # }
        self.logger.debug('Retrieving indices and addresses')
        # ipAddressIfIndex OID
        # - the value is the interface's index in IF-MIB.
        #   - It _must_ match the corresponding value in that interface's `ifIndex` field,
        #     as stored in self._interfaces. self.ifaces_with_addresses(), self.ip_addresses_to_dict
        #     and self.ip_addrs_to_dict all depend on this.
        # - the OID/index contains the address type (IPv4 vs IPv6) and the address itself,
        #   separated by a dot.
        #   The address is wrapped in quotes, hence the offset indices at each end.
        for datum in self.__walk('IP-MIB', 'ipAddressIfIndex'):
            # We need the IP version, and it's always in the OID returned to us, so we may as well
            # extract it now.
            # IP version is the 12th element of this OID, unless you're counting from zero.
            if datum.oid[11] == 4:
                protocolversion = 'ipv4'
            else:
                protocolversion = 'ipv6'
            # Extract the address. Yes, this really is the less-bad way.
            self.logger.debug(f'Extracting IP address from OID {datum.oid.prettyPrint()}')
            address = ipaddress.ip_address(re.split('"', datum.oid.prettyPrint())[1])
            # Initialise the accumulator entry for this address
            acc[address] = {'ipAddressIfIndex': int(datum.value),
                            'protocol': protocolversion}
            # pylint: disable=line-too-long
            self.logger.debug(f'Initialising address {address} in the accumulator with index {datum.value} and version {protocolversion}.')
        self.logger.debug('Retrieving prefix lengths')
        # Prefix length / ipAddressPrefix
        # The value for this OID contains all sorts of crap prepended to the actual prefix-length,
        # so we have to break it up and extract the last element from the resulting list.
        for datum in self.__walk('IP-MIB', 'ipAddressPrefix'):
            address = ipaddress.ip_address(re.split('"', datum.oid.prettyPrint())[1])
            # When queried for ipAddressPrefix, Brocade Ironware returns an upraised middle finger
            # in the form of SNMPv2-SMI::zeroDotZero.
            # Catch and handle this case.
            if str(datum.value[-1]) == 'SNMPv2-SMI::zeroDotZero':
                prefixlength = 0
            else:
                prefixlength = datum.value[-1]
            # Now set the value
            acc[address]['prefixlength'] = prefixlength
            self.logger.debug('Accumulated prefixlength %s for address %s',
                              acc[address]['prefixlength'], address)
        # Types - unicast, anycast or broadcast.
        # No multicast here; these are handled in another table again.
        self.logger.debug('Retrieving address types')
        for datum in self.__walk('IP-MIB', 'ipAddressType'):
            address = ipaddress.ip_address(re.split('"', datum.oid.prettyPrint())[1])
            acc[address]['addressType'] = str(datum.value)
            self.logger.debug(f'Accumulated type {acc[address]["addressType"]} for address {address}')
        # Populate self._ipaddresses with a list of IpAddress namedtuples
        self._ipaddresses = [IpAddress(ipAddressIfIndex=int(details['ipAddressIfIndex']),
                                       protocol=str(details['protocol']),
                                       address=address,
                                       prefixlength=int(details['prefixlength']),
                                       addressType=str(details['addressType']))
                             for address, details in acc.items()]
        self.logger.debug(f"Fetched address-list: {self._ipaddresses}")
        return True

    def ip_addresses(self) -> List[IpAddress]:
        '''
        Return the device´s IP address table, as a list of IpAddress namedtuples.
        If this isn't already populated, queries the device first.
        NB: Covers both IPv4 and IPv6.
        '''
        # If we don't already have this data, fetch it and populate that attribute in `self`.
        if not self._ipaddresses:
            self.populate_ip_addresses()
        # Having ensured we have this data, return it
        return self._ipaddresses

    def ip_addresses_to_dict(self) -> Dict[int, List[Dict]]:
        '''
        Convert the list of ipAddress namedtuples to a dict.
        Its keys are the ipAddressIfIndex value, i.e. the IF-MIB index for that interface.
        Each value is a list of dicts, because an interface may have any number of addresses.
        Used via self.as_dict() as a helper for self.as_json().
        '''
        acc = collections.defaultdict(list)
        for address in self._ipaddresses:
            acc[address.ipAddressIfIndex].append({'protocol': str(address.protocol),
                                                  'address': str(address.address),
                                                  'prefixLength': int(address.prefixlength),
                                                  'addressType': str(address.addressType)})
        return acc


    def populate_ip_addrs(self) -> bool:
        '''
        Fetch the device's IP address table from the deprecated but still widely-used ipAddrTable
        and populate self.ip_addrs with the resulting list of IpAddr objects.
        Helper function for ip_addrs().
        '''
        self.logger.debug('Retrieving IPv4 addresses from ipAddrTable')
        # Accumulator structure:
        # - index: ipAddress = the address in question
        #   - index: str =  SNMP index
        #   - netmask: IpAddress
        acc: Dict[ipaddress.IPv4Address, Dict] = {}
        # Fetch each interface's address and IP-MIB index, and initialise its entry in the
        # accumulator with those.
        for item in self.__walk('IP-MIB', 'ipAdEntIfIndex'):
            self.logger.debug(f'Processing address OID {item.oid.prettyPrint()}')
            # pylint: disable=anomalous-backslash-in-string
            address = ipaddress.ip_address(re.split('\.', item.oid.prettyPrint(), maxsplit=1)[1])
            self.logger.debug(f'Initialising address {address} in the accumulator with index {item.value}')
            acc[address] = {'index': int(item.value)}
        # Add the netmask for each address
        self.logger.debug('Retrieving netmasks')
        for item in self.__walk('IP-MIB', 'ipAdEntNetMask'):
            self.logger.debug(f'Processing address OID {item.oid.prettyPrint()}')
            # pylint: disable=anomalous-backslash-in-string
            address = ipaddress.ip_address(re.split('\.', item.oid.prettyPrint(), maxsplit=1)[1])
            self.logger.debug(f'Augmenting address {address} with netmask {item.value.prettyPrint()}')
            acc[address]['netmask'] = item.value.prettyPrint()
        # Assemble the fetched data into a list of IpAddr namedtuples
        self._ipaddrs = [IpAddr(ipAdEntIfIndex=details['index'],
                                ipAdEntAddr=address,
                                ipAdEntNetMask=details['netmask'])
                         for address, details in acc.items()]
        return True

    def ip_addrs(self) -> List[IpAddr]:
        '''
        Return the device´s IP address table, as a list of ipAddr namedtuples.
        If this isn't already populated, queries the device first.
        NB: Ipv4-only, by definition.
        '''
        # If we already have this data, fetch it.
        if not self._ipaddrs:
            self.populate_ip_addrs()
        # Now return it
        return self._ipaddrs

    def ip_addrs_to_dict(self) -> Dict[int, List[Dict]]:
        '''
        Convert the list of ipAddr namedtuples to a dict whose keys are the ipAdEntIfIndex value,
        i.e. the IF-MIB index for the associated interface.
        Converts the netmask to a prefix-length, for consistency with the ipAddresses table.
        Intended as a helper function for combining addresses with interfaces.
        '''
        result = collections.defaultdict(list)
        for addr in self._ipaddrs:
            # Derive the prefixlength, and get a simpler varname for address while we're at it.
            (address, prefixlength) = re.split(
                '/',
                ipaddress.IPv4Interface(f"{addr.ipAdEntAddr}/{addr.ipAdEntNetMask}").with_prefixlen)
            # Assemble and insert the actual entry
            result[addr.ipAdEntIfIndex].append({'protocol': 'ipv4',    # IPv4-only table
                                                'address': address,
                                                'prefixLength': prefixlength,
                                                'addressType': 'unknown'})
        return result

    # Assumes self._interfaces[n].ifIndex matches the key in the output dict from
    # self.ip_addrs_to_dict() and self.ip_addresses_to_dict().
    def ifaces_with_addrs(self) -> Dict[str, Dict]:
        '''
        Return a dict of dicts:
        - convert the list of interface namedtuples to a dict whose index is ifName
        - add an attribute 'addresses' whose value is a list of dicts representing addresses.
        Output format uses the following structure of keys:
        - <ifName>
            - ifIndex
            - ifDescr
            - ifType
            - ifSpeed
            - ifPhysAddress
            - ifName
            - ifHighSpeed
            - ifAlias
            - addresses
                - protocol
                - address
                - prefixLength
                - addressType
        Used in self.to_dict(), as a helper for self.as_json().
        '''
        result: Dict[str, Dict] = {} # Accumulator for the return value
        # Which addresses store should we use?
        # Prefer the newer table
        if self._ipaddresses:
            addresslist = self.ip_addresses_to_dict()
        # ...but use the deprecated one, if that's all we have.
        elif self._ipaddrs:
            addresslist = self.ip_addrs_to_dict()
        # Failing all else, provide a last-resort default.
        # This simplifies the code in the next section, by removing the need for a conditional.
        else:
            addresslist = collections.defaultdict(list)
        # Now iterate over the interfaces
        for iface in self._interfaces:
            # Assemble and insert the entry
            result[iface.ifName] = {'ifIndex': iface.ifIndex,
                                    'ifDescr': iface.ifDescr,
                                    'ifType': iface.ifType,
                                    'ifSpeed': iface.ifSpeed,
                                    'ifPhysAddress': iface.ifPhysAddress,
                                    'ifName': iface.ifName,
                                    'ifHighSpeed': iface.ifHighSpeed,
                                    'ifAlias': iface.ifAlias,
                                    'addresses': addresslist[iface.ifIndex]}
        return result

    def bgp4_instance(self, auth=None, target=None):
        '''
        Return a hash-table of BGP4 data for the named BGP4 instance on the target.
        Arguments, both optional for overriding the default:
        - auth = community-string. These tend to vary with multiple instances.
        - target = target address. This can be different for querying difference instances.
        '''
        # Figure out the optional parameters
        if auth:
            authz = auth
        else:
            authz = self.auth
        if target:
            targetz = target
        else:
            targetz = self.target
        # Assemble and return the results
        return {'instance': self.bgp4_system(auth=authz, target=targetz),
                'peers': self.bgp4_peerings(auth=authz, target=targetz)}

    def bgp4_system(self, auth=None, target=None):
        '''
        Return instance-wide details for BGP4:
        - local ASN
        - local identifier (router ID)
        Assumes a single BGP instance on the target host.
        '''
        # Figure out the optional parameters
        if auth:
            authz = auth
        else:
            authz = self.auth
        if target:
            targetz = target
        else:
            targetz = self.target
        # Assemble and return the results
        return BgpInstance(bgpLocalAs=self.__get(attribute='localAs',
                                                 mib='BGP4-MIB',
                                                 auth=authz,
                                                 target=targetz),
                           bgpIdentifier=self.__get(attribute='localIdentifier',
                                                    mib='BGP4-MIB',
                                                    auth=authz,
                                                    target=targetz))

    def bgp4_peerings(self, auth=None, target=None):
        '''
        Return a list of peering objects, derived from bgpPeerTable.
        Assumes a single BGP instance on the target host.
        '''
        # Figure out the optional parameters
        if auth:
            authz = auth
        else:
            authz = self.auth
        if target:
            targetz = target
        else:
            targetz = self.target
        result = collections.defaultdict(dict) # Result accumulator
        for row in ['bgpPeerIdentifier',
                    'bgpPeerHoldTime']:
            for peer in self.__walk("BGP4-MIB", row, auth=authz, target=targetz):
                result[peer.oid][row] = peer.value
        # OMG pylint, stop trying to make procedural happen. This is a comprehension.
        # pylint: disable=consider-using-dict-items
        return [BgpPeerEntry(bgpPeerIdentifier=result[peer]['bgpPeerIdentifier'],
                             bgpPeerHoldTime=result[peer]['bgpPeerHoldTime'],
                             bgpPeerKeepAlive=result[peer]['bgpPeerKeepAlive'],
                             bgpPeerState=result[peer]['bgpPeerState'],
                             bgpPeerHoldTimeConfigured=result[peer]['bgpPeerHoldTimeConfigured'],
                             bgpPeerKeepAliveConfigured=result[peer]['bgpPeerKeepAliveConfigured'],
                             bgpPeerAdminStatus=result[peer]['bgpPeerAdminStatus'],
                             bgpPeerLocalAddr=result[peer]['bgpPeerLocalAddr'],
                             bgpPeerLocalPort=result[peer]['bgpPeerLocalPort'],
                             bgpPeerRemoteAddr=result[peer]['bgpPeerRemoteAddr'],
                             bgpPeerRemotePort=result[peer]['bgpPeerRemotePort'],
                             bgpPeerRemoteAs=result[peer]['bgpPeerRemoteAs'],
                             )
                for peer in result.keys()]

    def as_dict(self):
        'Return the object´s contents as a dict'
        return {'system': {'sysDescr': str(self.system_data.sysDescr),
                           'sysObjectID': str(self.system_data.sysObjectID),
                           'sysName': str(self.system_data.sysName),
                           'sysLocation': str(self.system_data.sysLocation)},
                'interfaces': self.ifaces_with_addrs()}

    def as_json(self):
        'Return a print representation of this object'
        return json.dumps(self.as_dict(),
                          indent=4,
                          sort_keys=True,
                          cls=netdescribe.utils.IPInterfaceEncoder)

    def __str__(self):
        'Return a print representation of this object'
        return self.as_json()

    def discover(self):
        'Perform full discovery on this device, and report on the result.'
        self.identify()
        self.interfaces()
        self.ip_addrs()
        self.ip_addresses()
        return True
