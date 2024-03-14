import pathlib
import re
import sys
import tomllib
from pprint import pprint

import requests
import subprocess

config_file = pathlib.Path(f"~/.openai-config.toml").expanduser()
with open(config_file, "rb") as f:
    config = tomllib.load(f)


def hal():
    prompt = " ".join(sys.argv[1:])
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "when asked to generate code, output only the code and no explanation"},
            {"role": "user", "content": f"{prompt}"}
        ],
        "temperature": 0.7,
        "response_format": {"type": "text"}
    }
    contents = openai_post(f"{config['api']['url']}/chat/completions", body)

    if not "choices" in contents:
        print("Unexpected Response")
        print("Raw response was")
        pprint(contents)
    print(contents['choices'][0]['message']['content'])


def dali():
    prompt = " ".join(sys.argv[1:])
    body = {
        "prompt": f"{prompt}",
        "model": "dall-e-3",
        "n": 1,
        "size": "1792x1024",
        "style": "natural"
    }
    contents = openai_post(f"{config['api']['url']}/images/generations", body)

    file_path = download_generated_image(contents["data"][0]["url"], prompt)

    subprocess.call(["open", "-R", file_path])
    print(file_path)


def openai_post(url, body):
    headers = {
        "Authorization": f"Bearer {config['api']['token']}"
    }
    response = requests.post(url, json=body, headers=headers)
    contents = response.json()
    return contents


def download_generated_image(image_url, prompt):
    filename = re.sub("[^a-z_]+", "", re.sub(" ", "_", prompt.lower())) + ".png"
    r = requests.get(image_url, stream=True)
    file_path = pathlib.Path(f"~/Downloads/{filename}").expanduser()
    with open(file_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=8192):
            fd.write(chunk)
    return file_path
