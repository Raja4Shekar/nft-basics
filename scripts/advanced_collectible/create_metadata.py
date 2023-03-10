from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests, json


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_filename = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_filename).exists():
            print(f"{metadata_filename} already exists! Delete it overwrite")
        else:
            print(f"Creating metadata file {metadata_filename}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            print(image_path)
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri
            print(collectible_metadata)
            with open(metadata_filename, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_filename)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        file_binary = fp.read()
    ipfs_url = "http://127.0.0.1:5001"
    endpoint = "/api/v0/add"
    response = requests.post(ipfs_url + endpoint, files={"file": file_binary})
    ipfs_hash = response.json()["Hash"]
    filename = filepath.split("/")[-1:][0]  # "./img/0-PUG.png" --> "0-PUG.png"
    file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
    print(file_uri)
    return file_uri
    # upload stuff...
