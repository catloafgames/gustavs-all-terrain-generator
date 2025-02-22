from PIL import Image
import numpy as np
import argparse
startx = 4460
starty = 11400
max_height = 200
min_height = 60

def load_image_to_array(image_path):
    # Open image and convert to grayscale
    image = Image.open(image_path).convert('L')

    img_array = np.array(image)
    scaled_array = img_array / 255.0

    return scaled_array


def generate_replay_from_scale(coords, scale_factor, noise):
    height = (max_height * scale_factor)
    if height < min_height:
        height = min_height
    posx = startx + coords[0]*10 + ()
    posy = starty + coords[1]*10
    command = f"spawnloc --p=DevGround1 --position={posx},{height},{posy}"

    return command


def process_image(image_path, output_size=None):

    scale_array = load_image_to_array(image_path)

    if output_size:
        image = Image.open(image_path).convert('L')
        image = image.resize((32,32), Image.Resampling.LANCZOS)
        scale_array = np.array(image) / 255.0

    commandlist = [f"teleto {startx} {min_height} {starty}"]
    for idx, x in np.ndenumerate(scale_array):
         commandlist.append(generate_replay_from_scale(idx, x))

    return commandlist


def main():

    parser = argparse.ArgumentParser()
    
    args = parser.parse_args()

    image_path = "img.png"

    try:
        commandList = process_image(image_path, True)
        with open("output.txt", 'w') as f:
            for line in commandList:
                f.write(f"{line}\n")
    except Exception as e:
        print(f"Error processing image: {e}")


if __name__ == "__main__":
    main()