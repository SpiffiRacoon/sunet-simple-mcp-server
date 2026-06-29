# sunet-simple-mcp-server
simple nexclout mcp server for testing filter / policy
<img width="692" height="497" alt="image" src="https://github.com/user-attachments/assets/40bbd229-e0a1-4e30-993b-4ba174b0a274" />

## Requirements:
See Requirements.txt

## Installation
#### Clone the git repo:

```git clone git@github.com:SpiffiRacoon/sunet-simple-mcp-server.git```

#### Create an environment file:
```touch .env```

Varibles you will need:
```
HOSTNAME=https://sunet.drive.sunet.se
SHARED_TOKEN=###############
```

#### Create a virtual environment and install required packages:
```
python -m venv .venv
source .venv/bin/activate
```

#### Install required packages
```pip install -r requirements.txt```
                                                                                                                                                   
#### Run the server or cli:
```python mcp_server.py```
or
```python cli.py```
