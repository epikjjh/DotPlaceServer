from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from dotplace.models import Profile
from dotplace.models import Trip
from dotplace.models import Position
from dotplace.models import Article
from dotplace.models import ImageInArticle


def main_page(request):
    return render(request, 'index.html')


def show_article(request):
    objects = Article.objects.all()
    context = {'articles': objects}
    return render(request, 'articlelist.html', context)


def show_trip(request):
    objects = Trip.objects.all()
    context = {'trips': objects}

    return render(request, 'triplist.html', context)


def show_position(request):
    objects = Position.objects.all()
    context = {'positions': objects}

    return render(request, 'positionlist.html', context)


def show_user(request):
    objects = Profile.objects.all()
    context = {'profiles': objects}

    return render(request, 'userlist.html', context)


@require_GET
def sign_in(request):
    return JsonResponse({'id': "test"})

#페이스북 연동 추가
@require_POST
def sign_up(request):
    user_name = request.POST.get('user name')
    nick_name = request.POST.get('nick name')
    phone_number = request.POST.get('phone number')
    pass_word = request.POST.get('pass word')
    email = request.POST.get('email')
    birthday = request.POST.get('birthday')
    gender = request.POST.get('gender')
    nation = request.POST.get('nation')
    profile_image = request.POST.get('profile image')

    user = User.objects.create_user(user_name, email, pass_word)

    profile = Profile.objects.filter(user_id=user.id).get()
    profile.nick_name = nick_name
    profile.phone_number = phone_number
    profile.birthday = birthday
    profile.gender = gender
    profile.nation = nation
    profile.profile_image = profile_image
    profile.save()

    return JsonResponse({'id': str(profile.id), 'code': '301'})


@require_POST
def create_trip(request):
    #multipart?
    title = request.POST.get('title')
    owner_index = request.POST.get('owner index')
    owner_id = request.POST.get('owner id')

    owner = Profile.objects.filter(id=owner_id).get()
    trip = Trip.objects.create(title=title, owner=owner, owner_index=owner_index)

    trip.save()

    return JsonResponse({'trip id': str(trip.id),  'code': '301'})


@require_POST
def create_position(request):
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    type = request.POST.get('type')
    duration = request.POST.get('duration')
    trip_id = request.POST.get('trip id')

    trip = Trip.objects.filter(id=trip_id).get()
    position = Position.objects.create(lat=lat, lng=lng, type=type, duration=duration, trip=trip)

    position.save()

    return JsonResponse({'position id': str(position.id), 'code': '301'})
#썸네일 기능 추가

@require_POST
def create_article(request):
    content = request.POST.get('content')
    position_id = request.POST.get('position id')

    position = Position.objects.filter(id=position_id).get()

    article = Article.objects.create(content=content, position=position)
    article.save()

    return JsonResponse({'id': str(article.id), 'code': '301'})


@require_GET
def search_article_by_radius(request):
    target_lat = float(request.GET.get('lat'))
    target_lng = float(request.GET.get('lng'))
    target_radius = int(request.GET.get('radius'))
    positions = list(Position.objects.exclude(type=0))
    result = []

    for position in positions:
        radius = ((target_lat - position.lat)**2 + (target_lng - position.lng)**2)**(1/2)
        if radius <= target_radius:
            if position.article_set.all():
                result_articles = list(position.article_set.all())
                for result_article in result_articles:
                    result.append(result_article.id)

    return JsonResponse({'article id': result})


@require_GET
def search_article_by_trip_id(request):
    trip_id = request.GET.get('trip_id')
    target_positions = list(Position.objects.filter(trip_id=trip_id))
    result = []

    for position in target_positions:
        if position.article_set.all():
            result_articles = list(position.article_set.all())
            for result_article in result_articles:
                result.append(result_article.id)

    return JsonResponse({'article id': result})