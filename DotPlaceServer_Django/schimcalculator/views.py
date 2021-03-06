from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
from schimcalculator.models import Area, DotPlace


class DotPlaceView(APIView):
    permission_classes(IsAuthenticated,)

    # django range query에서는 end point가 포함 되어 조정함
    _lat_standard = 0.00003749
    _lng_standard = 0.0000749

    def post(self, request):
        user = request.user
        lat = float(request.POST.get('lat'))
        lng = float(request.POST.get('lng'))
        is_dot = request.POST.get('is dot')

        if not lat or not lng or not is_dot:
            return JsonResponse({'code': '31'})

        is_dot = True if is_dot is '1' else False

        try:
            area = Area.objects.filter(lat__range=(lat, lat+DotPlaceView._lat_standard),
                                       lng__range=(lng, lng+DotPlaceView._lng_standard)).get()
            area.numofdots += 1
            area.save()

        except Area.DoesNotExist:
            return JsonResponse({'code': '32'})

        except Area.MultipleObjectsReturned:
            return JsonResponse({'code': '33'})

        total_dots = DotPlace.objects.count()
        ticket = (area.numofdots / total_dots) if total_dots else 1
        dotplace = DotPlace.objects.create(area=area, owner=user, ticket=ticket, is_dot=is_dot)
        dotplace.save()

        return JsonResponse({'code': '0'})


def set_seoul_area():
    lat_standard = 0.0000375
    lng_standard = 0.000075

    seoul_west = 126.768532
    seoul_east = 127.180581
    seoul_south = 37.427542
    seoul_north = 37.701052

    x = seoul_west

    while x < seoul_east:
        y = seoul_south
        while y < seoul_north:
            Area(lat=y, lng=x).save()
            y += lat_standard
        x += lng_standard
