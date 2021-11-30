import requests
import pickle
import os
from config import CABINET_API_TOKEN

file_path = os.path.dirname(__file__)


def get_projects() -> dict:
    try:
        with open(f"{file_path}/data/projects.pickle", "rb") as f:
            print("LOADING DATA")
            data = pickle.load(f)

    except:
        print("REQUESTING DATA")
        response = requests.get(
            f"https://cabinet.miem.hse.ru/api/projects",
            headers={"accept": "application/json", "X-Auth-Token": CABINET_API_TOKEN},
        )

        data = response.json()["data"]

        with open(f"{file_path}/data/projects.pickle", "wb") as f:
            pickle.dump(data, f)

    return data
