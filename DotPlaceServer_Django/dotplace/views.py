import os
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from dotplace.models import Profile
from dotplace.models import Trip
from dotplace.models import Position
from dotplace.models import Article
from dotplace.models import ImageInArticle
from dotplace.process_image import create_thumbnail


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

    profile_image = request.FILES.get('profile image')

    user = User.objects.create_user(user_name, email, pass_word)

    profile = Profile.objects.filter(user__pk=user.pk).get()
    profile.nick_name = nick_name
    profile.phone_number = phone_number
    profile.birthday = birthday
    profile.gender = gender
    profile.nation = nation

    if profile_image:
        profile.profile_image = profile_image

    profile.save()

    if profile_image:
        create_thumbnail('profile/profile_image_{profile_id}.jpeg'.format(profile_id=profile.pk), (400, 300))

    return JsonResponse({'id': str(profile.pk), 'code': '301'})


@require_POST
def create_trip(request):
    title = request.POST.get('title')
    owner_index = request.POST.get('owner index')
    owner_id = request.POST.get('owner id')

    owner = Profile.objects.filter(pk=owner_id).get()
    trip = Trip.objects.create(title=title, owner=owner, owner_index=owner_index)

    trip.save()

    return JsonResponse({'trip id': str(trip.pk),  'code': '301'})


@require_POST
def create_position(request):
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    type = request.POST.get('type')
    duration = request.POST.get('duration')
    trip_id = request.POST.get('trip id')

    trip = Trip.objects.filter(pk=trip_id).get()
    position = Position.objects.create(lat=lat, lng=lng, type=type, duration=duration, trip=trip)

    position.save()

    return JsonResponse({'position id': str(position.pk), 'code': '301'})


@require_POST
def create_article(request):
    content = request.POST.get('content')
    position_id = request.POST.get('position id')

    position = Position.objects.filter(pk=position_id).get()

    article = Article.objects.create(content=content, position=position)
    article.save()

    return JsonResponse({'article id': str(article.pk), 'code': '301'})


@require_POST
def create_article_image(request):
    image = request.FILES['image']
    article_id = request.POST.get('article id')
    article = Article.objects.filter(pk=article_id).get()

    article_image = ImageInArticle(image=image, article=article)
    article_image.save()

    create_thumbnail('article/article_image_{article_id}/{id}.jpeg'.format(article_id=article_id, id=article_image.pk),
                     (800, 600))

    return JsonResponse({'article image id': str(article_image.pk), 'code': '301'})


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
                    result.append(result_article.pk)

    return JsonResponse({'article id': result})


@require_GET
def search_article_by_trip_id(request):
    trip_id = request.GET.get('trip_id')
    target_positions = list(Position.objects.filter(trip__pk=trip_id))
    result = []

    for position in target_positions:
        if position.article_set.all():
            result_articles = list(position.article_set.all())
            for result_article in result_articles:
                result.append(result_article.pk)

    return JsonResponse({'article id': result})


@require_GET
def search_user_by_id(request):
    user_id = request.GET.get('user_id')
    target_profile = Profile.objects.filter(pk=user_id).get()

    if target_profile:
        user_name = target_profile.user.username
        email = target_profile.user.email
        nick_name = target_profile.nick_name
        phone_number = target_profile.phone_number
        birthday = target_profile.birthday
        gender = target_profile.gender
        nation = target_profile.nation

        return JsonResponse({'user id': user_id, 'user name': user_name, 'email': email, 'nick name': nick_name,
                             'phone number': phone_number, 'birthday': birthday, 'gender': gender, 'nation': nation})

    else:
        return JsonResponse({'user id': '-1'})


@require_GET
def search_article_by_id(request):
    article_id = request.GET.get('article_id')
    target_article = Article.objects.filter(pk=article_id).get()

    if target_article:
        content = target_article.content
        time = target_article.time
        owner_id = target_article.position.trip.owner.pk
        target_images = list(ImageInArticle.objects.filter(article__pk=article_id))
        image_ids = []
        for target_image in target_images:
            image_ids.append(target_image.pk)

        return JsonResponse({'user id': owner_id, 'time': time, 'content': content, 'image ids': image_ids})

    else:
        return JsonResponse({'user id': '-1'})


@require_GET
def news_feed(request):
    article_id = request.GET.get('article_id')
    target_article = Article.objects.filter(pk=article_id).get()

    if target_article:
        # 최상단 이미지만 보냄
        target_images = list(ImageInArticle.objects.filter(article__pk=article_id))
        image_id = []
        for target_image in target_images:
            image_id.append(target_image.pk)

        time = target_article.time
        trip_id = target_article.position.trip.pk
        
        if image_id:
            result_id = image_id[0]
        else:
            result_id = []

        # 스침 점수 : 향후 추가 할 것

        return JsonResponse({'trip id': trip_id, 'time': time, 'image id': result_id})

    else:
        return JsonResponse({'trip id': '-1'})


@require_GET
def return_file(request):
    image_id = request.GET.get('image_id')
    dir_id = request.GET.get('dir_id')
    image_type = request.GET.get('type')

    # profile thumbnail
    if image_type == '0':
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'profile')
        file_name = 'profile_image_' + str(image_id) + '_thumbnail.jpeg'

    # profile
    elif image_type == '1':
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'profile')
        file_name = 'profile_image_' + str(image_id) + '.jpeg'

    # article thumbnail
    elif image_type == '2':
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'article', 'article_image_{}'.format(dir_id))
        file_name = str(image_id) + '_thumbnail.jpeg'

    # article
    elif image_type == '3':
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'article', 'article_image_{}'.format(dir_id))
        file_name = str(image_id) + '.jpeg'

    # error
    else:
        return JsonResponse({'code': '-1'})

    file_path = os.path.join(path, file_name)

    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f, content_type="image/jpeg")
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

    except FileNotFoundError:
        return JsonResponse({'code': '-1'})

    else:
        return response
# 1. 뉴스피드 정보 보내기(request : article id) : response : 썸네일(일단은 가장 첫 사진 -> 나중에 대표 사진 기능 추가 시 변경) + 시간 보내기 + 나중에 스침 점수 추가 시 스침 점수도 보낼 것
# 2. 확대 사진 정보 보내기(request : article id) : response : user id + article 정보 (content + time + 모든 이미지들)
# 3. User 정보 보내기(request : user id) : response : user 정보
# 현경이형한테 스침 생성 설명 요청
# 중복 검사하여 처리 해야함
