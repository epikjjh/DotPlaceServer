from PIL import Image


def create_thumbnail(path, size):
    image = Image.open(path)
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(path+'.thumbnail', 'JPEG')