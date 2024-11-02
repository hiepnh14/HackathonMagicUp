from openaiAPI import getColors
from makeup import makeup
import os
def applyMakeup(image_path, userRequest):
    colors = getColors(image_path, userRequest)
    # colors = [[255, 192, 203], [255, 228, 225], [255, 105, 180], [255, 182, 193], [255, 105, 180], [0, 191, 255]]
    # colors = [[0, 0, 0], [255, 224, 189], [255, 153, 153], [255, 102, 102], [194, 178, 128], [0, 0, 255]]
    # colors = [[255, 0, 0], [200, 0, 0], [255, 255, 255], [30, 30, 30], [30, 30, 30]]
    makeup(image_path, colors)

def main(userRequest=None, image_path=None):
    if not image_path:
        image_path = "image.jpeg"
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir, image_path)
    if not userRequest:
        userRequest = "I want to have a feminine makeup look for halloween."
    applyMakeup(image_path, userRequest)

if __name__ == "__main__":
    main()