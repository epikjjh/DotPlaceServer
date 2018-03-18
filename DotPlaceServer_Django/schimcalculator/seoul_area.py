from schimcalculator.models import Area

lat_standard = 0.0000375
lng_standard = 0.000075

seoul_west = 126.768532
seoul_east = 127.180581
seoul_south = 37.427542
seoul_north = 37.701052

x = seoul_west
sum = 0

while x < seoul_east:
    y = seoul_south
    while y < seoul_north:
        Area(lat=y, lng=x).save()
        y += lat_standard
    x += lng_standard