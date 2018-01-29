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
def login(request):
    print(request.GET.get('id'))

    return JsonResponse({'id': "test"})


@require_POST
def create_user(request):
    '''
    user_name = request.POST.get('user name')
    pass_word = request.POST.get('pass word')
    email = request.POST.get('email')

    user = User.objects.create_user(username=user_name, email=email, password=pass_word)
    user.save()

    birthday = request.POST.get('birthday')
    gender = request.POST.get('gender')
    nation = request.POST.get('nation')
    profile_image = request.POST.get('profile image')

    profile = Profile.objects.create(user=user, birthday=birthday, gender=gender, nation=nation, profile_image=profile_image)
    profile.save()

    if birthday == 'None' or gender == 'None' or nation == 'None':
        return JsonResponse({'id': '-1', 'code': '-1'})

    return JsonResponse({'id': str(profile.id), 'code': '301'})
    '''
    return

@require_POST
def create_trip_and_position(request):

    return


@require_POST
def create_article(request):

    return


@require_GET
def search_article_by_radius(request):
    #type 추가
    target_lat = float(request.GET.get('lat'))
    target_lng = float(request.GET.get('lng'))
    target_radius = int(request.GET.get('radius'))
    positions = list(Position.objects.all())
    result = []

    for position in positions:
        if position.type != 0:
            radius = ((target_lat - position.lat)**2 + (target_lng - position.lng)**2)**(1/2)
            if radius <= target_radius:
                if position.article_set.all():
                    result_article = position.article_set.all().get()
                    result.append(result_article.id)

    return JsonResponse({'article id': result})


@require_GET
def search_article_by_trip_id(request):
    trip_id = request.GET.get('trip_id')
    target_positions = list(Position.objects.filter(trip_id=trip_id))
    articles = list(Article.objects.all())
    result = []

    for position in target_positions:
        if position.article_set.all():
            result_artlce = position.article_set.all().get()
            result.append(result_artlce.id)

    return JsonResponse({'article id': result})