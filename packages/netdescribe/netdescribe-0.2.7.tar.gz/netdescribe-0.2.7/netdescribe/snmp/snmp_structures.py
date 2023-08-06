#!/usr/bin/env python3

#   Copyright [2018] [James Fleming <james@electronic-quill.net]
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
Data structures that are common across the objects
"""

# Built-in modules
import ipaddress
from typing import NamedTuple

SystemData = NamedTuple('SystemData', [
    ('sysDescr', str),      # Detailed text description of the system
    ('sysObjectID', str),   # Vendor's OID identifying the device; should correspond to make/model
    ('sysName', str),       # Usually either the hostname or the host's FQDN
    ('sysLocation', str)    # Physical location of the device
    ])

Interface = NamedTuple('Interface', [
    ('ifIndex', int),
    ('ifDescr', str),       # Should include the name of the manufacturer, the product name and the
                            # version of the hardware interface.
    ('ifType', str),        # http://www.alvestrand.no/objectid/1.3.6.1.2.1.2.2.1.3.html
    ('ifSpeed', int),       # Estimate of bandwidth in bits per second
    ('ifPhysAddress', str), # MAC address or equivalent
    ('ifName', str),        # As assigned by the local device, for CLI administration
    ('ifHighSpeed', int),   # Estimate of the interface's bandwidth in units of 1,000,000 bps
    ('ifAlias', str)        # Administrator-configured description string for the interface.
    ])

IpAddress = NamedTuple('IpAddress', [
    ('ipAddressIfIndex', int),  # IF-MIB index for the interface on which this address is configured
    ('protocol', str),          # IP protocol version: ipv4 | ipv6
    ('address', str),           # IP address
    ('prefixlength', int),      # integer, 0-128
    ('addressType', str)        # Address type: unicast, multicast or broadcast
    ])

IpAddr = NamedTuple('IpAddr', [
    ('ipAdEntIfIndex', int),   # The IP-MIB index for the associated interface
    ('ipAdEntAddr', ipaddress.IPv4Address),      # The actual IP address
    ('ipAdEntNetMask', str)    # The address' netmask
    ])

# BGP4 instance-wide details
# On systems with multiple BGP instances, this describes (only) the BGP instance being queried,
# so each one will need to be queried separately.
BgpInstance = NamedTuple('BgpInstance', [
    ('bgpLocalAs', str),
    ('bgpIdentifier', str)
    ])

# Describes entries in BGP4-MIB::bgpPeerTable as a subset of bgpPeerEntry
BgpPeerEntry = NamedTuple('BgpPeerEntry', [
    ('bgpPeerIdentifier', str),
    ('bgpPeerHoldTime', int),
    ('bgpPeerKeepAlive', int),
    ('bgpPeerState', int),  # See https://oidref.com/1.3.6.1.2.1.15.3.1.2
    ('bgpPeerHoldTimeConfigured', int),
    ('bgpPeerKeepAliveConfigured', int),
    ('bgpPeerAdminStatus', int),    # See https://oidref.com/1.3.6.1.2.1.15.3.1.3
    ('bgpPeerLocalAddr', str),
    ('bgpPeerLocalPort', int),
    ('bgpPeerRemoteAddr', str),
    ('bgpPeerRemotePort', int),
    ('bgpPeerRemoteAs', str)
    ])
