from PIL import Image
import numpy as np
import math

def generate_replay_from_scale(coords, x,  params):
    scale = params["max_height"] - params["min_height"]
    height = math.ceil((x / 255 * scale) + params["min_height"])
    print(height)
    posx = params["start_x"] + coords[0]*params["spacing"]
    posy = params["start_y"] + coords[1]*params["spacing"]
    command = f"spawnloc --p=DevGround1 --position={posx},{height},{posy}\n"

    return command


def process_image(params):

    image = Image.open(params["file_path"]).convert('L')
    image = image.resize((params["width"], params["length"]), Image.Resampling.LANCZOS)
    scale_array = np.array(image)

    commandlist = [f"teleto {params['start_x']} {params['min_height']} {params['start_y']}\n"]
    for idx, x in np.ndenumerate(scale_array):
         commandlist.append(generate_replay_from_scale(idx, x, params))

    return commandlist

