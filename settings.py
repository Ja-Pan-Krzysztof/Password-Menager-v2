from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_DIR = f'{BASE_DIR}/.env'
CONFIG_DIR = f'{BASE_DIR}/config/'

# Config file
PLATFORM_FILE = f'{BASE_DIR}/startup.yaml'
