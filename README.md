# Prov Table Updater
 GUI tool to update provisioning tables DHCP options

 ## Requirements
 A few required packages (included in requirements.txt)
 Install with `pip install -r requirements.txt`
 * PyQt5
 * meraki 1.0.0b14

Also requires Python 3.8+

## API Key
Supply your own API key by creating a file called `creds.py`
Inside `creds.py`, create a dictionary called `creds` with a key of `api_key` and a value of your meraki API key

Example: `creds = {"api_key": "your_api_key_here"}`

## Run the Tool
### Command line
Windows: Run the command `python main.py` and the GUI should open up

Unix/MAC: Run the command `python3 main.py` and the GUI should open up

### Explorer
Double click the file `main.py` in your file explorer