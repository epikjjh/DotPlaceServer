from PIL import Image


def create_thumbnail(path, size):
    image = Image.open(path)
    image.thumbnail(size, Image.ANTIALIAS)
    new_path = path.split('.jpeg')[0] + '_thumbnail.jpeg'
    image.save(new_path, 'JPEG')