import os
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from dotplace.models import User, Trip, Position, Article, ArticleImage, Comment
from dotplace.process_image import create_thumbnail


class UserView(APIView):
    permission_classes(IsAuthenticated,)

    def get(self, request):
        user = request.user

        user_name = user.user_name
        email = user.email
        phone_number = user.phone_number
        birthday = user.birthday
        gender = user.gender
        nation = user.nation

        return JsonResponse({'code': '0', 'user name': user_name, 'email': email, 'phone number': phone_number,
                             'birthday': birthday, 'gender': gender, 'nation': nation})

    def put(self, request):
        user = request.user

        user_name = request.data.get('user name')
        birthday = request.data.get('birthday')
        gender = request.data.get('gender')
        nation = request.data.get('nation')
        profile_image = request.FILES.get('profile image')

        if user_name:
            user.user_name = user_name

        if birthday:
            user.birthday = birthday

        if gender:
            user.gender = gender

        if nation:
            user.nation = nation

        # 기존 이미지 삭제 후 변경
        if profile_image:
            if user.profile_image:
                try:
                    os.remove('user/profile_image_{profile_id}.jpeg'.format(profile_id=user.pk))
                    os.remove('user/profile_image_{profile_id}_thumbnail.jpeg'.format(profile_id=user.pk))

                except FileNotFoundError:
                    user.profile_image = profile_image

            user.profile_image = profile_image

        user.save()

        if profile_image:
            create_thumbnail('user/profile_image_{profile_id}.jpeg'.format(profile_id=user.pk), (400, 300))

        return JsonResponse({'code': '0'})

    def delete(self, request):
        user = request.user
        code = user.delete()

        return JsonResponse({'code': str(code)})


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

    user, code = User.objects.create_user(user_name, phone_number, email, pass_word,
                                          birthday, gender, nation, profile_image)

    try:
        token = Token.objects.get(user=user)
    except ObjectDoesNotExist:
        return JsonResponse({'code': ''})

    return JsonResponse({'code': str(code), 'id': str(user.pk), 'token': token.key})


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def sign_out(request):
    user = request.user
    Token.objects.get(user=user).delete()

    return JsonResponse({'code': '0'})


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def change_pw(request):
    new_pw = request.data.get('pass word')
    user = request.user
    user.set_password(new_pw)
    user.save()

    return JsonResponse({'code': '0'})


class ArticleView(APIView):
    permission_classes(IsAuthenticated, )

    def get(self, request):
        article_id = request.GET.get('article_id')

        try:
            target_article = Article.objects.filter(pk=article_id).get()

        except Article.DoesNotExist:
            return JsonResponse({'user id': '-1'})

        content = target_article.content
        time = target_article.time
        owner_id = target_article.position.trip.owner.pk
        target_images = list(ArticleImage.objects.filter(article__pk=article_id))
        image_ids = []
        for target_image in target_images:
            image_ids.append(target_image.pk)

        return JsonResponse({'user id': owner_id, 'time': time, 'content': content, 'image ids': image_ids})

    def post(self, request):
        content = request.POST.get('content')
        position_id = request.POST.get('position id')

        position = Position.objects.get(pk=position_id)

        article = Article.objects.create(content=content, position=position)
        article.save()

        return JsonResponse({'article id': str(article.pk), 'code': '0'})

    def put(self, request):
        article_id = request.data.get('article id')
        content = request.data.get('content')
        position_id = request.data.get('position id')

        article = Article.objects.get(pk=article_id)

        if content:
            article.content = content

        if position_id:
            position = Position.objects.get(pk=position_id)
            article.position = position

        article.save()

        return JsonResponse({'article id': str(article.pk), 'code': '0'})

    def delete(self, request):
        article_id = request.data.get('article id')
        article = Article.objects.get(pk=article_id)
        article.delete()

        return JsonResponse({'code': '0'})


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
def news_feed(request):
    article_id = request.GET.get('article_id')

    target_article = Article.objects.filter(pk=article_id).get()

    if target_article:
        # 최상단 이미지만 보냄
        target_images = list(ArticleImage.objects.filter(article__pk=article_id))
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

        return JsonResponse({'thumbnail id': int(result_id), 'content': str(content), 'time': str(time),
                             'trip id': int(trip_id)})

    else:
        return JsonResponse({'trip id': '-1'})


class CommentView(APIView):
    permission_classes(IsAuthenticated, )

    def get(self, request):
        comment_id = request.GET.get('comment_id')
        comment = Comment.objects.get(pk=comment_id)
        article_id = comment.article.pk
        owner_id = comment.owner.pk
        content = comment.content
        time = comment.time

        return JsonResponse({'owner id': str(owner_id), 'article id': str(article_id),
                             'content': str(content), 'time': str(time)})

    def post(self, request):
        user = request.user
        article_id = request.POST.get('article id')
        content = request.POST.get('content')

        article = Article.objects.get(pk=article_id)
        comment = Comment(owner=user, article=article, content=content)
        comment.save()

        return JsonResponse({'code': '0'})

    def put(self, request):
        comment_id = request.data.get('comment id')
        article_id = request.data.get('article id')
        owner_id = request.data.get('owner id')
        content = request.data.get('content')

        comment = Comment.objects.get(pk=comment_id)
        article = Article.objects.get(pk=article_id)
        owner = User.objects.get(pk=owner_id)

        if article:
            comment.article = article
        if owner:
            comment.owner = owner
        if content:
            comment.content = content

        comment.save()

        return JsonResponse({'code': '0'})

    def delete(self, request):
        comment_id = request.data.get('comment id')
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()

        return JsonResponse({'code': '0'})


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


class TripView(APIView):
    permission_classes(IsAuthenticated, )

    def get(self, request):
        trip_id = request.GET.get('trip_id')
        trip = Trip.objects.get(pk=trip_id)
        title = trip.title
        owner_id = trip.owner.pk
        owner_index = trip.owner_index

        return JsonResponse({'owner id': str(owner_id), 'owner index': str(owner_index), 'title': str(title)})

    def post(self, request):
        owner = request.user
        title = request.POST.get('title')
        owner_index = request.POST.get('owner index')

        trip = Trip.objects.create(title=title, owner=owner, owner_index=owner_index)

        trip.save()

        return JsonResponse({'trip id': str(trip.pk), 'code': '0'})

    def put(self, request):
        trip_id = request.data.get('trip id')
        title = request.data.get('title')
        owner_id = request.data.get('owner id')
        owner_index = request.data.get('owner index')

        trip = Trip.objects.get(pk=trip_id)
        owner = User.objects.get(pk=owner_id)

        trip.title = title
        trip.owner_index = owner_index
        trip.owner = owner
        trip.save()

        return JsonResponse({'trip id': str(trip.pk), 'code': '0'})

    def delete(self, request):
        trip_id = request.data.get('trip id')
        trip = Trip.objects.get(pk=trip_id)
        trip.delete()

        return JsonResponse({'code': '0'})


class PositionView(APIView):
    permission_classes(IsAuthenticated, )

    def get(self, request):
        position_id = request.GET.get('position_id')
        position = Position.objects.get(pk=position_id)

        lat = position.lat
        lng = position.lng
        time = position.time
        type = position.type
        duration = position.duration
        trip_id = position.trip.pk

        return JsonResponse({'lat': str(lat), 'lng': str(lng), 'time': str(time), 'type': str(type),
                             'duration': str(duration), 'trip_id': str(trip_id), 'code': '0'})

    def post(self, request):
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        type = request.POST.get('type')
        duration = request.POST.get('duration')
        trip_id = request.POST.get('trip id')

        trip = Trip.objects.filter(pk=trip_id).get()
        position = Position.objects.create(lat=lat, lng=lng, type=type, duration=duration, trip=trip)

        position.save()

        return JsonResponse({'position id': str(position.pk), 'code': '0'})

    def delete(self, request):
        position_id = request.data.get('position id')
        position = Position.objects.get(pk=position_id)
        position.delete()

        return JsonResponse({'code': '0'})


class ArticleImageView(APIView):
    permission_classes(IsAuthenticated, )

    def get(self, request):
        image_id = request.GET.get('image_id')
        article_id = request.GET.get('article_id')
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'article',
                            'article_image_{}'.format(article_id))
        file_name = str(image_id) + '.jpeg'

        file_path = os.path.join(path, file_name)

        try:
            with open(file_path, 'rb') as f:
                response = HttpResponse(f, content_type="image/jpeg")
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

        except FileNotFoundError:
            return JsonResponse({'code': ''})

        else:
            return response

    def post(self, request):
        image = request.FILES['image']
        article_id = request.POST.get('article id')
        article = Article.objects.filter(pk=article_id).get()

        article_image = ArticleImage(image=image, article=article)
        article_image.save()
        try:
            code = '0'
            create_thumbnail('article/article_image_{article_id}/{id}.jpeg'
                             .format(article_id=article_id, id=article_image.pk), (800, 600))
        except FileNotFoundError:
            code = ''

        return JsonResponse({'article image id': str(article_image.pk), 'code': str(code)})

    def delete(self, request):
        image_id = request.data.get('image id')
        image = ArticleImage.objects.get(pk=image_id)
        code = image.delete()

        return JsonResponse({'code': str(code)})


class ProfileImageView(APIView):
    permission_classes(IsAuthenticated, )

    def get(self, request):
        user = request.user
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'user')
        file_name = 'profile_image_' + str(user.pk) + '.jpeg'

        file_path = os.path.join(path, file_name)

        try:
            with open(file_path, 'rb') as f:
                response = HttpResponse(f, content_type="image/jpeg")
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

        except FileNotFoundError:
            return JsonResponse({'code': ''})

        else:
            return response

    def put(self, request):
        user = request.user
        profile_image = request.data.get('profile image')

        try:
            code = '0'
            os.remove('user/profile_image_{user_id}.jpeg'.format(user_id=user.pk))
            os.remove('user/profile_image_{user_id}_thumbnail.jpeg'.format(user_id=user.pk))
        except FileNotFoundError:
            code = ''

        user.profile_image = profile_image
        user.save()

        return JsonResponse({'code': str(code)})

    def delete(self, request):
        user = request.user
        user.profile_image = None
        try:
            code = '0'
            os.remove('user/profile_image_{user_id}.jpeg'.format(user_id=user.pk))
            os.remove('user/profile_image_{user_id}_thumbnail.jpeg'.format(user_id=user.pk))
        except FileNotFoundError:
            code = ''

        return JsonResponse({'code': str(code)})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def return_profile_image_thumbnail(request):
    user = request.user
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'user')
    file_name = 'profile_image_' + str(user.pk) + '_thumbnail.jpeg'

    file_path = os.path.join(path, file_name)

    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f, content_type="image/jpeg")
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

    except FileNotFoundError:
        return JsonResponse({'code': ''})

    else:
        return response


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def return_article_image_thumbnail(request):
    image_id = request.GET.get('image_id')
    article_id = request.GET.get('article_id')
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'article',
                        'article_image_{}'.format(article_id))
    file_name = str(image_id) + '_thumbnail.jpeg'

    file_path = os.path.join(path, file_name)

    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f, content_type="image/jpeg")
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

    except FileNotFoundError:
        return JsonResponse({'code': ''})

    else:
        return response