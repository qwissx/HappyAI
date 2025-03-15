import base64
from PIL import Image


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

def reduce_image_quality(image_path):
    img = Image.open(image_path)
    img = img.resize((img.size[0] // 2, img.size[1] // 2))
    img.save(image_path)
