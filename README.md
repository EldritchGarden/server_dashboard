# Eldritch Garden Dashboard
Server dashboard for pterodactyl servers in Eldritch Garden

## Requirements
- Python 3.11
- Flask
- py-dactyl

## Install
Clone and run `pip install -e .`

Pterodactyl API key in `dashboard/config/api_key`

For python to trust the CA cert, it must be added to:
`.venv/lib/python3.11/site-packages/certifi/cacert.pem`

### Flask Config
Looks for `config.py` in the (instance folder)[https://flask.palletsprojects.com/en/2.3.x/config/#instance-folders]

The config is not needed to run the dashboard.

## Running in Prod
- (Deploy)[https://flask.palletsprojects.com/en/2.3.x/tutorial/deploy/]
- (Deploying to Production)[https://flask.palletsprojects.com/en/2.3.x/deploying/]
