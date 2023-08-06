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
General SNMP functions
"""

# pylint: disable=wrong-import-order

# Third-party libraries
import pysnmp.hlapi
from typing import List#, NamedTuple
from collections import namedtuple

# Built-in modules
import logging
#import re


# Data structures
#SnmpDatum = NamedTuple('SnmpDatum', [
#    ('oid', str),       # The OID itself
#    ('value', str)])
SnmpDatum = namedtuple('SnmpDatum', [
    'oid',      # The OID as returned directly by pysnmp, without processing.
    'value'])


# Basic functions

# pylint: disable=too-many-arguments
def snmp_get(engine: pysnmp.hlapi.SnmpEngine,
             auth: pysnmp.hlapi.CommunityData,
             target: pysnmp.hlapi.UdpTransportTarget,
             mib: str,
             attr: str,
             logger: logging.Logger) -> str:
    '''
    Perform an SNMP GET for a single OID or scalar attribute.
    Return only the value.
    '''
    logger.debug('Getting %s::%s from %s', mib, attr, target.transportAddr[0])
    # Create an ObjectType object to represent the OID
    oid = pysnmp.hlapi.ObjectType(pysnmp.hlapi.ObjectIdentity(mib, attr, 0))
    # Construct an iterator
    cmd = pysnmp.hlapi.getCmd(engine, auth, target, pysnmp.hlapi.ContextData(), oid)
    # Fetch the data, and any error information returned, using the iterator
    error_indication, error_status, error_index, var_binds = next(cmd)
    # Handle any errors
    if error_indication:
        logger.error(error_indication)
        raise RuntimeError(error_indication)
    if error_status:
        logger.error(f"{error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1][0] or '?'}")
        raise RuntimeError(error_status.prettyPrint())
    # If we actually got something, return it.
    # var_binds should be a sequence of ObjectType instances, representing the MIB variables
    # returned by the server, in the form of a tuple.
    # From the first instance in the tuple, fetch the value and pretty-print it.
    # The first value in an ObjectType instance is the variable identifier; the second is its value.
    val = var_binds[0][1]
    logger.debug(f'Retrieved value "{val}" of type {type(val)}')
    #return val.prettyPrint()
    return val

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
def snmp_walk(engine: pysnmp.hlapi.SnmpEngine,
             auth: pysnmp.hlapi.CommunityData,
             target: pysnmp.hlapi.UdpTransportTarget,
             mib: str,
             attr: str,
             logger: logging.Logger) -> List[SnmpDatum]:
    '''
    Walk an SNMP OID.
    Return a list of SnmpDatum namedtuples, containing the OIDs and values received.
    Conversion/processing is left for the calling function.
    '''
    logger.debug('Walking %s::%s on %s', mib, attr, target.transportAddr[0])
    # Build and execute the command
    obj = pysnmp.hlapi.ObjectIdentity(mib, attr)
    oid = pysnmp.hlapi.ObjectType(obj)
    cmd = pysnmp.hlapi.nextCmd(engine,
                               auth,
                               target,
                               pysnmp.hlapi.ContextData(),
                               oid,
                               lexicographicMode=False)
    returnval: List[SnmpDatum] = []
    for (error_indication, error_status, error_index, var_binds) in cmd:
        # Handle the responses
        if error_indication:
            logger.error(error_indication)
        elif error_status:
            logger.error('%s at %s',
                         error_status.prettyPrint(),
                         error_index and var_binds[int(error_index) - 1][0] or '?')
        # If we actually got something, return it as an SnmpDatum
        else:
            for var in var_binds:
                #
                logger.debug(f'Type of OID "{var[0].prettyPrint()}" is {type(var[0])}')
                logger.debug(f'Type of value "{var[1].prettyPrint()}" is {type(var[1])}')
                datum = SnmpDatum(oid=var[0], value=var[1])
                # Update the accumulator
                returnval.append(datum)
    return returnval
