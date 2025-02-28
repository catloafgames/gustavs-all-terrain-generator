from PIL import Image
import numpy as np
import argparse
startx = 4460
starty = 11400
max_height = 200
min_height = 60



def generate_replay_from_scale(coords, scale_factor):
    height = (max_height * scale_factor)
    if height < min_height:
        height = min_height
    posx = startx + coords[0]*10 + ()
    posy = starty + coords[1]*10
    command = f"spawnloc --p=DevGround1 --position={posx},{height},{posy}"

    return command


def process_image(params):

    image = Image.open(params["file_path"]).convert('L')
    image = image.resize((params["width"],params["height"]), Image.Resampling.LANCZOS)
    scale_array = np.array(image) / 255.0

    commandlist = [f"teleto {params.start_x} {min_height} {starty}"]
    for idx, x in np.ndenumerate(scale_array):
         commandlist.append(generate_replay_from_scale(idx, x))

    return commandlist




