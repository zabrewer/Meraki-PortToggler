#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Meraki-PortToggler Console Script.

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""
__author__ = "Zach Brewer"
__email__ = "zbrewer@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import requests
import json
import warnings
import click
import click_config_file

#### setup baseURL for API call functions ###
base_url = 'https://api.meraki.com/api/v0'

#### Error trapping ###
class Error(Exception):
    """

    Base module exception

    """
    pass

class OrgPermissionError(Error):
    """

    Thrown when supplied API Key does not have access to supplied Organization ID

    """

    def __init__(self):
        self.default = 'Invalid Organization ID - Current API Key does not have access to this Organization'

    def __str__(self):
        return repr(self.default)

class DashboardObject(object):
    """

    Base Dashboard object

    """
    pass

### Valid JSON Check ###
def __isjson(myjson):
    """

    Args:
        myjson: String variable to be validated if it is JSON

    Returns: None

    """
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True

### more handler functions ### 

def __returnhandler(statuscode, returntext, objtype, suppressprint):
    """

    Args:
        statuscode: HTTP Status Code
        returntext: JSON String
        objtype: Type of object that operation was performed on (i.e. SSID, Network, Org, etc)
        suppressprint: Suppress any print output when function is called

    Returns:
        errmsg: If returntext JSON contains {'errors'} element
        returntext: If no error element, returns returntext

    """

    validreturn = __isjson(returntext)
    noerr = False
    errmesg = ''

    if validreturn:
        returntext = json.loads(returntext)

        try:
            errmesg = returntext['errors']
        except KeyError:
            noerr = True
        except TypeError:
            noerr = True

    if str(statuscode) == '200' and validreturn:
        if suppressprint is False:
            print('\n{0} Operation Successful - Use --action=status option for verification\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '200':
        if suppressprint is False:
            print('{0} Operation Successful\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '201' and validreturn:
        if suppressprint is False:
            print('{0} Added Successfully - See returned data for results\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '201':
        if suppressprint is False:
            print('{0} Added Successfully\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '204' and validreturn:
        if suppressprint is False:
            print('{0} Deleted Successfully - See returned data for results\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '204':
        print('{0} Deleted Successfully\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '400' and validreturn and noerr is False:
        if suppressprint is False:
            print('Bad Request - See returned data for error details\n')
        return errmesg
    elif str(statuscode) == '400' and validreturn and noerr:
        if suppressprint is False:
            print('Bad Request - See returned data for details\n')
        return returntext
    elif str(statuscode) == '400':
        if suppressprint is False:
            print('Bad Request - No additional error data available\n')
    elif str(statuscode) == '401' and validreturn and noerr is False:
        if suppressprint is False:
            print('Unauthorized Access - See returned data for error details\n')
        return errmesg
    elif str(statuscode) == '401' and validreturn:
        if suppressprint is False:
            print('Unauthorized Access')
        return returntext
    elif str(statuscode) == '404' and validreturn and noerr is False:
        if suppressprint is False:
            print('Resource Not Found - See returned data for error details\n')
        return errmesg
    elif str(statuscode) == '404' and validreturn:
        if suppressprint is False:
            print('Resource Not Found')
        return returntext
    elif str(statuscode) == '500':
        if suppressprint is False:
            print('HTTP 500 - Server Error')
        return returntext
    elif validreturn and noerr is False:
        if suppressprint is False:
            print('HTTP Status Code: {0} - See returned data for error details\n'.format(str(statuscode)))
        return errmesg
    else:
        print('HTTP Status Code: {0} - No returned data\n'.format(str(statuscode)))

### begin main code ###

# Return a switch port via API
# https://api.meraki.com/api_docs#return-a-switch-port
def getswitchportdetail(apikey, serialnum, portnum, suppressprint=False):
    calltype = 'Switch Port Detail'
    geturl = '{0}/devices/{1}/switchPorts/{2}'.format(str(base_url), str(serialnum), str(portnum))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


# Update a switch port via API
# leaving a lot of this here even though it is not accessible via the CLI [zb]
# as it is written now in case this tool needs to be updated for more use cases [zb]
# https://api.meraki.com/api_docs#update-a-switch-port
def updateswitchport(apikey, serialnum, portnum, name=None, tags=None, enabled=None, porttype=None, vlan=None, voicevlan=None, allowedvlans=None, poe=None, isolation=None, rstp=None, stpguard=None, accesspolicynum=None, suppressprint=False):

    calltype = 'Switch Port'
    puturl = '{0}/devices/{1}/switchPorts/{2}'.format(str(base_url), str(serialnum), str(portnum))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    putdata = {}

    if name is not None:
        putdata['name'] = str(name)

    if tags is not None:
        putdata['tags'] = __listtotag(tags)

    if enabled is None:
        pass
    elif isinstance(enabled, bool):
        putdata['enabled'] = enabled
    else:
        raise ValueError('Enabled must be a boolean variable')

    if porttype is None:
        pass
    elif porttype in ('access', 'trunk'):
        putdata['type'] = str(porttype)
    else:
        raise ValueError('Type must be either "access" or "trunk"')

    if vlan is not None:
        putdata['vlan'] = str(vlan)

    if voicevlan is not None:
        putdata['voiceVlan'] = voicevlan

    if allowedvlans is not None:
        putdata['allowedVlans'] = allowedvlans

    if poe is None:
        pass
    elif isinstance(poe, bool):
        putdata['poeEnabled'] = poe
    else:
        raise ValueError('PoE enabled must be a boolean variable')

    if isolation is None:
        pass
    elif isinstance(isolation, bool):
        putdata['isolation'] = isolation
    else:
        raise ValueError('Port isolation must be a boolean variable')

    if rstp is None:
        pass
    elif isinstance(rstp, bool):
        putdata['rstpEnabled'] = rstp
    else:
        raise ValueError('RSTP enabled must be a boolean variable')

    if stpguard is None:
        pass
    elif stpguard.lower() in ('disabled', 'root guard', 'bpdu guard', 'loop guard'):
        putdata['stpGuard'] = stpguard
    else:
        raise ValueError('Valid values for STP Guard are "disabled", "Root guard", "BPDU guard", or "Loop guard"')

    if accesspolicynum is not None:
        putdata['accessPolicyNumber'] = accesspolicynum

    dashboard = requests.put(puturl, data=json.dumps(putdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

### begin CLI code ###
@click.command()
@click.option(
    '--api-key', '-A', type=str,
    help='your API key from the meraki dashboard'
)
## passes API key from config to CLI, config file should contain apikey = "[key value]"
@click_config_file.configuration_option()
@click.option('--serialnumber', '-SN', type=str, help='Serial Number of the Switch', required=True)
@click.option('--action', type=click.Choice(['enable', 'disable','status']), required=True)
@click.option(
    '--switchport', '-SP', type=str,
    help='SwitchPort to Enable/Disable', required=True
)
def cli(api_key, serialnumber, switchport, action):
    """
    A simple CLI app to disable/enable a port.  Requires API key from Meraki Dashboard,
    Serial Number of the switch, and port number of the port. 
    
    Especially useful for disabling stacking ports which can only be disabled from the Meraki
    API.

    The API key can be stored in a file and called with the --config FILEPATH option instead
    of using the -A or --api-key Options.  API key should be stored in file as follows:
    api_key = '[KEY VALUE FROM DASHBOARD]'

    THIS SOFTWARE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND.  AUTHOR IS NOT RESPONSIBLE 
    FOR ANYTHING, ESPECIALLY IF YOU DISABLE AN UPLINK PORT OR OTHER ACTIVE PORT!

    Examples:

    python PortToggler.py --api-key 123456789 --serialnumber A1B2C3D4 --switchport 5 --action=disable
    
    python PortToggler.py -A 123456789 -SN A1B2C3D4 -SP 5 --action=disable
    
    python PortToggler.py --config /path/to/file/api.cfg --serialnumber A1B2C3D4 --switchport 5 --action=disable

    python PortToggler.py --config api.cfg --serialnumber A1B2C3D4 --switchport 5 --action=disable

    * config file should contain one line similar to the following (single quotes required): api_key = '123456789'
    * if you use both --config and --api options, --api will always take precedence over the api key in the file 
    """
        
    if action == 'enable':
        updateswitchport(apikey = api_key, serialnum = serialnumber, portnum = switchport, enabled = True)
    elif action == 'disable':
        click.confirm('Are you sure you want to disable port number ' + switchport + '?', abort=True)
        updateswitchport(apikey = api_key, serialnum = serialnumber, portnum = switchport, enabled = False)
    elif action == 'status':
        detail = getswitchportdetail(apikey = api_key, serialnum = serialnumber, portnum = switchport)
        if detail is not None and detail["enabled"]:
            click.echo('Port number ' + switchport +' is ' + 'enabled, see details below:\n')
            for key, value in detail.items():
                print(key, '=', value)
        elif detail is not None and detail["enabled"] == False:
            click.echo('Port number ' + switchport +' is ' + 'disabled, see details below:\n')
            for key, value in detail.items():
                print(key, '=', value)
        else:
            click.echo('\nNO DATA RETURNED. \n\n' +
            '**Check the following:** \n\n' +
            '- Is the API key generated on dashboard? \n' +
            '- Are there typos in switch SN or other attributes? \n' +
            '- Does API key have access to the switch org (org admins) or network (network admins)?'
            )
    print('\n')
if __name__ == "__main__":
    cli()