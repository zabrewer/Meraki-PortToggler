# Meraki-PortToggler
Python 3.5+ command line utility to enable/disable Meraki switch ports via the API.

## Purpose
I ran into a use case where Meraki stacking ports had to be temporarily disabled on Meraki MS switches being deployed at multiple sites.

As stack ports can only be disabled via the Meraki API,  I created this tool (and compiled it) to assist on-site installers stacking ports on new installs and then re-enable the stacking ports at a later date.

It can also be used to toggle any switchport via the API and check the status.

## Installation
PortToggler was tested/written on Python 3.7 but should work on 3.5+.  It requires the following Python modules:
* requests
* click
* click_config_file

My preferred method of installation is in a Python virtual environment.

**1. Make a new virtual environment:**
```
virtualenv -m PortToggler
```
(generic command structure is):
python3 -m venv /path/to/new/virtual/environment



**2. activate the virtual environment:**
mac/linux (from PortToggler virtual environment directory):
```
source bin/activate
```

windows (virtualenv creates an activate.bat file in the Scripts subfolder of the virtual environment dir):
```
\path\to\env\Scripts\activate
```
If completed successfully, your command prompt should now have changed (begins with the virtual environment name in parentheses)

To exit the virtual environment at any time, use the deactivate command
```
deactivate
```



**3.  Install PortToggler to the Virtual Environment** 

There are a couple of ways to go about installing PortToggler to the virtual environment.

**Install Option 1**

One install option is to pull down the Setup.py file from this repo and use it to install PortToggler and all its dependencies.  If you choose this method, you can simply call PortToggler directly as a module (without calling Python first), i.e.:
```
PortToggler --api-key 123456789 --serialnumber A1B2C3D4 --switchport 5 --action=disable
```
For this install option, copy BOTH PortToggler.py and Setup.py to your virtual environment's root directory and type:

```
pip install --editable .
```
Note that you must have the virtual environment **active** for this to work correctly.  You can now call PortToggler while in the virtual environment by invoking:
```
PortToggler --help
```
**Install Option 2**

Another virtual environment install option is satisfy the module dependencies yourself using PIP and then to simply copy PortToggler.py to your virtual environment root folder.

With the virtual environment active, install the following modules:
```
pip install requests
pip install click
pip install click_config_file
```

Again, you must have the virtual environment **active** for this to work correctly.  You can now call PortToggler while in the virtual environment by invoking:
```
Python PortToggler.py --help
```

**Other Considerations**

If you wish for PortToggler to be available outside of your virtual environment, you can can call it by using your system default Python3 installation as long as the module dependencies are satisfied.  There are pros and cons to this which I encourage you to explore on your own.

As long as Python 3.5+ is installed (and PIP is installed), you can run the following commands:

```
pip install requests
pip install click
pip install click_config_file
python3 path/to/PortToggler.py --help
```

If you want PortToggler to be available without having to call Python first, make sure setup.py and PortToggler.py are in the same directory:
```
pip install --editable .
```

now you can call PortToggler from the command line by simply typing:

```
PortToggler
```

## Usage
Invoke PortToggler.py --help to get started.  You need an API key, the switch's serial number, and the switch port.

Primary options: --action=disable|enable|status

Examples:

    python PortToggler.py --api-key 123456789 --serialnumber A1B2C3D4 --switchport 5 --action=disable
    
    python PortToggler.py -A 123456789 -SN A1B2C3D4 -SP 5 --action=disable
    
    python PortToggler.py --config /path/to/file/api.cfg --serialnumber A1B2C3D4 --switchport 5 --action=disable

    python PortToggler.py --config api.cfg --serialnumber A1B2C3D4 --switchport 5 --action=disable

    If used, the api config file should contain one line similar to the following (single quotes required) e.g.
    api_key = '123456789'

## Credit
Credit to Shiyue Cheng for error functions, saved me much time while I wrote this on a flight from SJC.


