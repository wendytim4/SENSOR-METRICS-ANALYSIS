from pathlib import Path
from dotenv import load_dotenv
import shutil
from tqdm.auto import tqdm
import os
import requests

load_dotenv()

path = Path('data/sensor_metrics.csv')
DATA_URL = os.getenv("DATA_URL")

if not path.is_file():
    with requests.get(DATA_URL, stream=True) as r:
        total_length = int(r.headers.get('Content-Length'))

        with tqdm.wrapattr(r.raw, "read", total=total_length, desc="") as raw:
            with open('data1/sensor_metrics.csv', "wb") as output:
                shutil.copyfileobj(raw, output)
