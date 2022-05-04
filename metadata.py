import pandas as pd
import os
from progressbar import progressbar
import json
from copy import deepcopy
import time


JSON = {
    "name": "Bean #",
    "description": "",
    "image": "ipfs://1234567890",
    "edition": 1,
    "date": int(time.time()),
    "attributes": [],
}


# Get metadata and JSON files path based on the collection name
def generate_paths(name):
    path = os.path.join("output", name)
    metadata_path = os.path.join(path, "metadata.csv")
    json_path = os.path.join(path, "json")
    return path, metadata_path, json_path


# Function to get attribute metadata
def get_attribute_metadata(metadata_path):
    df = pd.read_csv(metadata_path)
    df = df.drop("Unnamed: 0", axis=1)
    df.columns = [col for col in df.columns]
    return df


def main():
    print("Enter the edition you want to generate metadata for: ")
    name = input()
    path, metadata_path, json_path = generate_paths(name)

    if not os.path.exists(path):
        print("Oops! Looks like this collection doesn't exist!")
        return
    
    # Make json folder
    if not os.path.exists(json_path):
        os.makedirs(json_path)

    df = get_attribute_metadata(metadata_path)

    for index, row in progressbar(df.iterrows()):

        item_json = deepcopy(JSON)
        item_json["name"] += str(index)
        item_json["image"] += f"/{index}.png"

        # Add all existing traits to attributes dictionary
        attributes = dict(row)
        for attribute in attributes:
            if attributes[attribute] != "none":
                item_json['attributes'].append({"trait_type": attribute, "value": attributes[attribute]})
        
        # Write file to json folder
        item_json_path = os.path.join(json_path, str(index))
        with open(item_json_path, "w", encoding="utf-8") as file:
            json.dump(item_json, file, indent=4)


if __name__ == "__main__":
    main()
