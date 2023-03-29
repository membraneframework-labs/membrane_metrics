# Membrane Metrics
This repo contains the backend system for retrieving and logging into MongoDB some community metrics related to Membrane Framework.

## Usage

1. Install packages listed in `requirements.txt` with `pip install -r requirements.txt`
2. Setup `config.toml` file in the project root directory with necessary configs specified in `config_example.toml`
3. If your DB host require IP addresses registration for connection, add your current IP address to `allowed IP addresses`. For `cloud.mongodb.com` with `Atlas DB` you can do this by entering `Network Access` page on `Security` section of you DB. 
![Add IP address to AtlasDB](assets/mongo_add_ip_address.png)
4. Run `python3 main.py`
