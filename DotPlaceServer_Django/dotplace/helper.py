from PIL import Image


def create_thumbnail(path, size):
    image = Image.open(path)
    image.thumbnail(size, Image.ANTIALIAS)
    new_path = path.split('.jpeg')[0] + '_thumbnail.jpeg'
    image.save(new_path, 'JPEG')

#2018.03.22 14.30.00
def index_parser(string):
    date = 0
    time = 0
    owner_index = string.split()

    for coarse in owner_index[0].split('.'):
        date += int(coarse)

    for fine in owner_index[1].split('.'):
        time += int(fine)

    return (date*60) + time
