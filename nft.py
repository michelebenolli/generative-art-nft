from PIL import Image
import numpy as np
import os
import csv
from os import path
from progressbar import progressbar
from config import CONFIG


# Parse the configuration file
def parse_config():
    for layer in CONFIG:
        # Get traits in sorted order from each layer
        directory = os.path.join("assets", layer["directory"])
        traits = sorted([x for x in os.listdir(directory) if x[0] != '.'])

        # If layer is not required, add None to the traits array
        if not layer["required"]:
            traits.append(None)

        # Generate final rarity weights
        if layer["rarity_weights"] is None:
            rarities = [1 for x in traits]
        elif type(layer["rarity_weights"] == "list") and len(traits) == len(layer["rarity_weights"]):
            rarities = layer["rarity_weights"]
        else:
            raise ValueError("Rarity weights is invalid")

        # Weight rarities and return a numpy array that sums up to 1
        layer["rarity_weights"] = np.array(rarities) / sum(rarities)
        layer["traits"] = traits


# Get total number of distinct possible combinations
def get_total_combinations():
    total = 1
    for layer in CONFIG:
        total = total * len(layer["traits"])
    return total


# Generate a single image given an array of layers
def generate_image(layers, name):
    # Treat the first layer as the background
    background = Image.open(path.join("assets", layers[0]))

    # Loop through layers 1 to n and stack them on top of another
    for layer in layers[1:]:
        image = Image.open(path.join("assets", layer))
        background.paste(image, (0, 0), image)

    # Save the final image
    background.save(name)


# Generate a trait combination based on rarity weights
def generate_data_item():
    result = []
    for layer in CONFIG:
        index = np.random.choice(range(len(layer["traits"])), p=layer["rarity_weights"])
        result.append(index)
    return result


# Generate the requested amount of unique samples
def generate_data(n):
    data = set()
    while len(data) < n:
        traits = generate_data_item()
        data.add(tuple(traits))
    return [list(x) for x in data]


# Generate metadata to describe the generated images
def generate_metadata(filepath, data):
    with open(filepath, "w", encoding="UTF8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([""] + [x["name"] for x in CONFIG])
        for n, item in enumerate(data):
            traits = [CONFIG[i]["traits"][x] for i, x in enumerate(item)]
            writer.writerow([n] + ["none" if x is None else path.splitext(x)[0] for x in traits])


# Get images paths for the given data item
def get_data_item_paths(item):
    paths = []
    for i, value in enumerate(item):
        trait = CONFIG[i]["traits"][value]
        if trait is not None:
            paths.append(path.join(CONFIG[i]["directory"], trait))
    return paths


# Generate the image set
def generate_images(name, number):

    # Create output directory if it does not exist
    output_path = path.join("output", name, "images")
    if not path.exists(output_path):
        os.makedirs(output_path)

    # Generate the images data
    data = generate_data(number)

    # Generate metadata to describe the images
    generate_metadata(os.path.join("output", name, "metadata.csv"), data)

    # Generate the images
    for i in progressbar(range(len(data))):
        paths = get_data_item_paths(data[i])
        generate_image(paths, path.join(output_path, f"{i}.png"))


def main():
    parse_config()

    combinations = get_total_combinations()
    print(f"\nYou can create {combinations} distinct images")
    print("How many images would you like to create? ")

    while True:
        num_avatars = int(input())
        if 0 < num_avatars <= combinations:
            break

    print("What is the name of the collection? ")
    name = input()
    generate_images(name, num_avatars)


if __name__ == "__main__":
    main()
