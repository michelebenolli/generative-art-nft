# This file MUST be configured in order for the code to run properly

# Make sure you put all your input images into the 'assets' folder.
# Each layer (or category) of images must be put in a folder of its own.

# CONFIG is an array of objects where each object represents a layer
# THESE LAYERS MUST BE ORDERED.

# Each layer needs to specify the following
# 1. id: A number representing a particular layer
# 2. name: The name of the layer.
# 3. directory: The folder inside assets_old that contain traits for the particular layer
# 4. required: If the particular layer is required (True) or optional (False). The first layer must always be true.
# 5. rarity_weights: Denotes the rarity distribution of traits. It can take on two types of values.
#       - None: This makes all the traits defined in the layer equally rare (or common)
#       - array: An array of numbers where each number represents a weight.

CONFIG = [
    {
        'id': 1,
        'name': 'background',
        'directory': '7_Sfondo',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 2,
        'name': 'body',
        'directory': '6_Corpo',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 3,
        'name': 'clothes',
        'directory': '5_Vestito',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 4,
        'name': 'hat',
        'directory': '4_Copricapo',
        'required': False,
        'rarity_weights': None,
    },
    {
        'id': 5,
        'name': 'shoulder',
        'directory': '3_SopraSpalla',
        'required': False,
        'rarity_weights': [0.1, 0.1, 0.1, 1],
    },
    {
        'id': 6,
        'name': 'expression',
        'directory': '2_Espressione',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 7,
        'name': 'accessories',
        'directory': '1_Accessori',
        'required': False,
        'rarity_weights': [1, 1, 1, 1, 1, 0.1, 1, 0.1, 1, 1, 1],
    }
]
