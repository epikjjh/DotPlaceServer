import os
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from dotplace.models import User, Trip, Position,Article, ImageInArticle, Comment
from dotplace.process_image import create_thumbnail
#from rest_framework.views import APIView
#from rest_framework.response import Response


'''회원 정보 관련 api'''

#로그 아웃
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def sign_out(request):
    user = request.user
    Token.objects.get(user=user).delete()

    return JsonResponse({'code': '301'})

#회원 가입
@require_http_methods(['POST'])
def sign_up(request):
    user_name = request.POST.get('user name')
    phone_number = request.POST.get('phone number')
    pass_word = request.POST.get('pass word')
    email = request.POST.get('email')
    birthday = request.POST.get('birthday')
    gender = request.POST.get('gender')
    nation = request.POST.get('nation')
    profile_image = request.FILES.get('profile image')

    user = User.objects.create_user(user_name, phone_number, email, pass_word, birthday, gender,
                                    nation, profile_image)

    token = Token.objects.get(user=user)

    return JsonResponse({'id': str(user.pk), 'token': token.key, 'code': '301'})

#비밀 번호 수정
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def change_pw(request):
    new_pw = request.data['pass word']
    user = request.user
    user.set_password(new_pw)
    user.save()

    return JsonResponse({'code': '301'})

#회원 정보 수정
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def change_info(request):
    user = request.user

    birthday = request.data['birthday']
    gender = request.data['gender']
    nation = request.data['nation']
    profile_image = request.FILES.get('profile image')

    if birthday:
        user.birthday = birthday

    if gender:
        user.gender = gender

    if nation:
        user.nation = nation

    #기존 이미지 삭제 후 변경
    if profile_image:
        os.remove('user/profile_image_{profile_id}.jpeg'.format(profile_id=user.user_name))
        os.remove('user/profile_image_{profile_id}_thumbnail.jpeg'.format(profile_id=user.user_name))
        user.profile_image = profile_image

    user.save()

    if profile_image:
        create_thumbnail('user/profile_image_{profile_id}.jpeg'.format(profile_id=user.user_name), (400, 300))

    return JsonResponse({'code': '301'})

#회원 탈퇴
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def withdrawal(request):
    user = request.user
    user.delete()

    return JsonResponse({'code': '301'})

#회원 정보 탐색
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search_user_by_id(request):
    target_profile = request.user

    user_name = target_profile.user_name
    email = target_profile.email
    phone_number = target_profile.phone_number
    birthday = target_profile.birthday
    gender = target_profile.gender
    nation = target_profile.nation

    return JsonResponse({'user name': user_name, 'email': email,
                        'phone number': phone_number, 'birthday': birthday, 'gender': gender, 'nation': nation})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_trip(request):
    owner = request.user
    title = request.POST.get('title')
    owner_index = request.POST.get('owner index')

    trip = Trip.objects.create(title=title, owner=owner, owner_index=owner_index)

    trip.save()

    return JsonResponse({'trip id': str(trip.pk),  'code': '301'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
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


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_article(request):
    content = request.POST.get('content')
    position_id = request.POST.get('position id')

    position = Position.objects.filter(pk=position_id).get()

    article = Article.objects.create(content=content, position=position)
    article.save()

    return JsonResponse({'article id': str(article.pk), 'code': '301'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_article_image(request):
    image = request.FILES['image']
    article_id = request.POST.get('article id')
    article = Article.objects.filter(pk=article_id).get()

    article_image = ImageInArticle(image=image, article=article)
    article_image.save()

    create_thumbnail('article/article_image_{article_id}/{id}.jpeg'.format(article_id=article_id, id=article_image.pk),
                     (800, 600))

    return JsonResponse({'article image id': str(article_image.pk), 'code': '301'})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search_article_by_radius(request):
    target_lat = float(request.GET.get('lat'))
    target_lng = float(request.GET.get('lng'))
    target_radius = float(request.GET.get('radius'))
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


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search_article_by_trip_id(request):
    trip_id = request.GET.get('trip_id')
    try:
        target_positions = list(Position.objects.filter(trip__pk=trip_id))

    except Position.DoesNotExist:
        return JsonResponse({'article id': '-1'})

    result = []

    for position in target_positions:
        if position.article_set.all():
            result_articles = list(position.article_set.all())
            for result_article in result_articles:
                result.append(result_article.pk)

    return JsonResponse({'article id': result})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search_article_by_id(request):
    article_id = request.GET.get('article_id')

    try:
        target_article = Article.objects.filter(pk=article_id).get()

    except Article.DoesNotExist:
        return JsonResponse({'user id': '-1'})

    content = target_article.content
    time = target_article.time
    owner_id = target_article.position.trip.owner.pk
    target_images = list(ImageInArticle.objects.filter(article__pk=article_id))
    image_ids = []
    for target_image in target_images:
        image_ids.append(target_image.pk)

    return JsonResponse({'user id': owner_id, 'time': time, 'content': content, 'image ids': image_ids})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
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
        content = target_article.content
        
        if image_id:
            result_id = image_id[0]
        else:
            result_id = 0

        # 스침 점수 : 향후 추가 할 것

        return JsonResponse({'thumbnail id': int(result_id), 'content': str(content), 'time': str(time), 'trip id': int(trip_id)})

    else:
        return JsonResponse({'trip id': '-1'})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def return_file(request):
    image_id = request.GET.get('image_id')
    dir_id = request.GET.get('dir_id')
    image_type = request.GET.get('type')

    # profile thumbnail
    if image_type == '0':
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'user')
        file_name = 'profile_image_' + str(image_id) + '_thumbnail.jpeg'

    # profile
    elif image_type == '1':
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'user')
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


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_comment(request):
    user = request.user
    article_id = request.POST.get('article id')
    content = request.POST.get('content')

    article = Article.objects.get(pk=article_id)
    comment = Comment(owner=user, article=article, content=content)
    comment.save()

    return JsonResponse({'code': 301})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search_comment_by_article_id(request):
    article_id = request.POST.get('article id')
    article = Article.objects.get(pk=article_id)

    comments = list(Comment.objects.filter(article=article))
    result = []

    for comment in comments:
        result.append(comment.pk)

    return JsonResponse({'article id': article_id, 'content ids': result})
# 1. 뉴스피드 정보 보내기(request : article id) : response : 썸네일(일단은 가장 첫 사진 -> 나중에 대표 사진 기능 추가 시 변경) + 시간 보내기 + 나중에 스침 점수 추가 시 스침 점수도 보낼 것
# 2. 확대 사진 정보 보내기(request : article id) : response : user id + article 정보 (content + time + 모든 이미지들)
# 3. User 정보 보내기(request : user id) : response : user 정보
# 현경이형한테 스침 생성 설명 요청
# 중복 검사하여 처리 해야함
