import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import requests
import src.emailService.email_script as email
import pandas as pd


def test_emailfunction():
    r = requests.get("https://rickandmortyapi.com/api/episode")
    episodes = pd.json_normalize(r.json()["results"])
    assert email.email_new(episodes) == 200
