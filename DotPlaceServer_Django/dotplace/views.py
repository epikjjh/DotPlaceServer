import os
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from dotplace.models import User, Trip, Position, Article, ArticleImage, Comment
from dotplace.helper import create_thumbnail, index_parser



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

        return JsonResponse({'code': '0', 'user name': str(user_name), 'email': str(email),
                             'phone number': str(phone_number), 'birthday': str(birthday),
                             'gender': str(gender), 'nation': str(nation)})

    def put(self, request):
        user = request.user

        user_name = request.data.get('user name')
        birthday = request.data.get('birthday')
        gender = request.data.get('gender')
        nation = request.data.get('nation')

        if user_name:
            user.user_name = user_name

        if birthday:
            user.birthday = birthday

        if gender:
            user.gender = gender

        if nation:
            user.nation = nation

        return JsonResponse({'code': '0'})

    def delete(self, request):
        user = request.user
        code = user.delete()

        return JsonResponse({'code': str(code), 'user id': str(user.pk)})


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

    try:
        user, code = User.objects.create_user(user_name, phone_number, email, pass_word,
                                              birthday, gender, nation, profile_image)
    except ValueError:
        return JsonResponse({'code': '1'})
    except IntegrityError:
        return JsonResponse({'code': '2'})

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        return JsonResponse({'code': '4'})

    return JsonResponse({'code': str(code), 'id': str(user.pk), 'token': str(token.key)})


class SignIn(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        if created:
            return JsonResponse({'code': '0', 'token': token.key})

        else:
            return JsonResponse({'code': '-1', 'token': token.key})


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def sign_out(request):
    user = request.user
    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        return JsonResponse({'code': '5'})
    else:
        token.delete()

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
            article = Article.objects.get(pk=article_id)

        except Article.DoesNotExist:
            return JsonResponse({'code': '6'})

        content = article.content
        time = article.time
        owner_id = article.position.trip.owner.pk
        image_ids = list(ArticleImage.objects.filter(article__pk=article_id).values_list('pk', flat=True))

        liked = article.like.filter(user=request.user).count() > 0

        return JsonResponse({'code': '0', 'user id': str(owner_id), 'time': str(time), 'content': str(content),
                             'image ids': image_ids, 'liked': bool(liked)})

    def post(self, request):
        content = request.POST.get('content')
        position_id = request.POST.get('position id')

        try:
            position = Position.objects.get(pk=position_id)

        except Position.DoesNotExist:
            return JsonResponse({'code': '7'})

        if (Article.objects.filter(position=position).count() > 0):
            return JsonResponse({'code': '8'})

        article = Article.objects.create(content=content, position=position)
        article.save()

        return JsonResponse({'code': '0', 'article id': str(article.pk)})

    def put(self, request):
        article_id = request.data.get('article id')
        content = request.data.get('content')
        position_id = request.data.get('position id')

        try:
            article = Article.objects.get(pk=article_id)

        except Article.DoesNotExist:
            return JsonResponse({'code': '8'})

        if content:
            article.content = content

        if position_id:
            try:
                position = Position.objects.get(pk=position_id)

            except Position.DoesNotExist:
                return JsonResponse({'code': '9'})

            article.position = position

        article.save()

        return JsonResponse({ 'code': '0', 'article id': str(article.pk)})

    def delete(self, request):
        article_id = request.data.get('article id')
        try:
            article = Article.objects.get(pk=article_id)

        except Article.DoesNotExist:
            return JsonResponse({'code': '10'})

        article.delete()

        return JsonResponse({'code': '0'})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search_article_by_radius(request):
    lat = float(request.GET.get('lat'))
    lng = float(request.GET.get('lng'))
    target_radius = float(request.GET.get('radius'))
    positions = Position.objects.exclude(type=0)
    result = []

    for position in positions:
        radius = ((lat - position.lat)**2 + (lng - position.lng)**2)**(1/2)
        if radius <= target_radius:
            result += list(position.article_set.all().values_list('pk', flat=True))

    return JsonResponse({'code': '0', 'article ids': result})

# @api_view(['GET'])
# @permission_classes((IsAuthenticated,))
# def search_article_by_radius_with_offset(request):
#     lat = float(request.GET.get('lat'))
#     lng = float(request.GET.get('lng'))
#     target_radius = float(request.GET.get('radius'))
#     positions = Position.objects.exclude(type=0)
#     result = []




@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search_article_by_trip_id(request):
    trip_id = request.GET.get('trip_id')
    positions = Position.objects.filter(trip__pk=trip_id)
    result = []

    for position in positions:
        result += list(position.article_set.all().values_list('pk', flat=True))

    return JsonResponse({'code': '0', 'article ids': result})

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search_articles_of_followings(request):
    offset = request.GET.get('offset')
    try:
        offset = int(offset)
    except:
        return JsonResponse({'code': '35'})

    if offset < 0: return JsonResponse({'code': '36'})
    amount_to_get = 10
    user = request.user

    followings = list(user.following.all())
    articles = Article.objects.filter(position__trip__owner__in=followings)
    articles_count = articles.count()
    offsets = articles_count / amount_to_get

    begin = (offset - 1) * amount_to_get

    if begin > articles_count: return JsonResponse({'code': '36'})

    end = begin + amount_to_get
    total_index = offsets + 1 if offsets > int(offsets) else offsets

    if end < articles_count:
        ret = list(articles[begin:end])
    else: ret = list(articles[begin:])

    return JsonResponse({'code': '0', 'article_ids': ret, 'total': total_index})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def news_feed(request):
    article_id = request.GET.get('article_id')

    try:
        article = Article.objects.get(pk=article_id)

    except Article.DoesNotExist:
        return JsonResponse({'code': '11'})

    # 최상단 image id만 보냄
    image_ids = ArticleImage.objects.filter(article__pk=article_id).values_list('pk', flat=True)
    time = article.time
    trip_id = article.position.trip.pk
    content = article.content

    if image_ids:
       result_id = image_ids[0]
    else:
        result_id = 0

    # 스침 점수 : 향후 추가 할 것

    return JsonResponse({'code': '0', 'thumbnail id': int(result_id), 'content': str(content), 'time': str(time),
                             'trip id': int(trip_id)})


class CommentView(APIView):
    permission_classes(IsAuthenticated, )

    def get(self, request):
        comment_id = request.GET.get('comment_id')
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({'code': '12'})

        article_id = comment.article.pk
        owner_id = comment.owner.pk
        content = comment.content
        time = comment.time

        return JsonResponse({'code': '0', 'owner id': str(owner_id), 'article id': str(article_id),
                             'content': str(content), 'time': str(time)})

    def post(self, request):
        user = request.user
        article_id = request.POST.get('article id')
        content = request.POST.get('content')

        try:
            article = Article.objects.get(pk=article_id)

        except Article.DoesNotExist:
            return JsonResponse({'code': '13'})

        comment = Comment(owner=user, article=article, content=content)
        comment.save()

        return JsonResponse({'code': '0', 'comment id': str(comment.pk)})

    def put(self, request):
        comment_id = request.data.get('comment id')
        article_id = request.data.get('article id')
        content = request.data.get('content')

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({'code': '14'})

        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return JsonResponse({'code': '15'})

        if article:
            comment.article = article
        if content:
            comment.content = content

        comment.save()

        return JsonResponse({'code': '0', 'comment id': str(comment.pk)})

    def delete(self, request):
        comment_id = request.data.get('comment id')

        try:
            comment = Comment.objects.get(pk=comment_id)

        except Comment.DoesNotExist:
            return JsonResponse({'code': '16'})

        comment.delete()

        return JsonResponse({'code': '0'})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search_comment_by_article_id(request):
    article_id = request.GET.get('article id')

    comment_ids = list(Comment.objects.filter(article__pk=article_id).values_list('pk', flat=True))

    return JsonResponse({'code': '0', 'article id': article_id, 'comment ids': comment_ids})


class TripView(APIView):
    permission_classes(IsAuthenticated, )

    def get(self, request):
        trip_id = request.GET.get('trip_id')

        try:
            trip = Trip.objects.get(pk=trip_id)

        except Trip.DoesNotExist:
            return JsonResponse({'code': '17'})

        title = trip.title
        owner_id = trip.owner.pk
        owner_index = trip.owner_index

        return JsonResponse({'owner id': str(owner_id), 'owner index': str(owner_index), 'title': str(title)})

    def post(self, request):
        owner = request.user
        title = request.POST.get('title')
        owner_index = request.POST.get('owner index')

        trip = Trip.objects.create(title=title, owner=owner, owner_index=index_parser(owner_index))

        trip.save()

        return JsonResponse({'code': '0', 'trip id': str(trip.pk)})

    def put(self, request):
        trip_id = request.data.get('trip id')
        title = request.data.get('title')
        owner_index = request.data.get('owner index')

        try:
            trip = Trip.objects.get(pk=trip_id)

        except Trip.DoesNotExist:
            return JsonResponse({'code': '18'})

        if title:
            trip.title = title
        if owner_index:
            trip.owner_index = index_parser(owner_index)

        trip.save()

        return JsonResponse({'code': '0', 'trip id': str(trip.pk)})

    def delete(self, request):
        trip_id = request.data.get('trip id')

        try:
            trip = Trip.objects.get(pk=trip_id)

        except Trip.DoesNotExist:
            return JsonResponse({'code': '19'})

        trip.delete()

        return JsonResponse({'code': '0'})


class PositionView(APIView):
    permission_classes(IsAuthenticated, )

    def get(self, request):
        position_id = request.GET.get('position_id')

        try:
            position = Position.objects.get(pk=position_id)

        except Position.DoesNotExist:
            return JsonResponse({'code': '20'})

        lat = position.lat
        lng = position.lng
        time = position.time
        type = position.type
        duration = position.duration
        trip_id = position.trip.pk

        return JsonResponse({'code': '0', 'lat': float(lat), 'lng': float(lng), 'time': str(time), 'type': int(type),
                             'duration': int(duration), 'trip id': str(trip_id)})

    def post(self, request):
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        type = request.POST.get('type')
        duration = request.POST.get('duration')
        trip_id = request.POST.get('trip id')

        try:
            trip = Trip.objects.get(pk=trip_id)
        except Trip.DoesNotExist:
            return JsonResponse({'code': '21'})

        position = Position.objects.create(lat=lat, lng=lng, type=type, duration=duration, trip=trip)

        position.save()

        return JsonResponse({'code': '0', 'position id': str(position.pk)})

    def delete(self, request):
        position_id = request.data.get('position id')

        try:
            position = Position.objects.get(pk=position_id)

        except Position.DoesNotExist:
            return JsonResponse({'code': '22'})

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
            return JsonResponse({'code': '23'})

        else:
            return response

    def post(self, request):
        image = request.FILES['image']
        article_id = request.POST.get('article id')

        try:
            article = Article.objects.get(pk=article_id)

        except Article.DoesNotExist:
            return JsonResponse({'code': '24'})

        article_image = ArticleImage(image=image, article=article)
        article_image.save()

        try:
            create_thumbnail('article/article_image_{article_id}/{id}.jpeg'
                             .format(article_id=article_id, id=article_image.pk), (800, 600))
        except FileNotFoundError:
            return JsonResponse({'code': '25'})

        return JsonResponse({'code': '0', 'article image id': str(article_image.pk)})

    def delete(self, request):
        image_id = request.data.get('image id')
        try:
            image = ArticleImage.objects.get(pk=image_id)
        except ArticleImage.DoesNotExist:
            return JsonResponse({'code': '26'})

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
            return JsonResponse({'code': '27'})

        else:
            return response

    def put(self, request):
        user = request.user
        profile_image = request.data.get('image')

        try:
            code = '0'
            os.remove('user/profile_image_{user_id}.jpeg'.format(user_id=user.pk))
            os.remove('user/profile_image_{user_id}_thumbnail.jpeg'.format(user_id=user.pk))
        except FileNotFoundError:
            code = '-1'

        user.profile_image = profile_image
        user.save()

        try:
            create_thumbnail('user/profile_image_{profile_id}.jpeg'.format(profile_id=user.pk), (400, 300))
        except FileNotFoundError:
            user.profile_image = None
            user.save()
            return JsonResponse({'code': '28'})

        return JsonResponse({'code': str(code)})

    def delete(self, request):
        user = request.user
        user.profile_image = None
        try:
            code = '0'
            os.remove('user/profile_image_{user_id}.jpeg'.format(user_id=user.pk))
            os.remove('user/profile_image_{user_id}_thumbnail.jpeg'.format(user_id=user.pk))
        except FileNotFoundError:
            code = '-1'

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
        return JsonResponse({'code': '29'})

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
        return JsonResponse({'code': '30'})

    else:
        return response


class FollowView(APIView):
    permission_classes((IsAuthenticated,))

    def put(self, request):
        following_id = request.data.get('user_id')
        user = request.user

        try:
            following = User.objects.get(pk=following_id)

        except User.DoesNotExist:
            return JsonResponse({'code': '31'})

        user.following.add(following)

        return JsonResponse({'code': '0'})

    def delete(self, request):
        following_id = request.data.get('user_id')
        user = request.user

        try:
            following = User.objects.get(pk=following_id)

        except User.DoesNotExist:
            return JsonResponse({'code': '31'})

        user.following.remove(following)

        return JsonResponse({'code': '0'})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_other_user(request):
    user_id = request.GET.get('user_id')

    try:
        user = User.objects.get(pk=user_id)

    except User.DoesNotExist:
        return JsonResponse({'code': '32'})

    user_name = user.user_name
    email = user.email
    birthday = user.birthday
    gender = user.gender
    nation = user.nation

    return JsonResponse({'code': '0', 'user name': str(user_name), 'email': str(email),'birthday': str(birthday),
                         'gender': str(gender), 'nation': str(nation)})


class LikeView(APIView):
    permission_classes((IsAuthenticated,))

    def put(self, request):
        article_id = request.data.get('article_id')
        user = request.user

        try:
            article = Article.objects.get(pk=article_id)

        except Article.DoesNotExist:
            return JsonResponse({'code': '33'})

        article.like.add(user)
        num_of_likes = int(User.objects.filter(article=article).count())
        return JsonResponse({'code': '0', 'count': num_of_likes})

    def delete(self, request):
        article_id = request.data.get('article_id')
        user = request.user

        try:
            article = Article.objects.get(pk=article_id)

        except Article.DoesNotExist:
            return JsonResponse({'code': '33'})

        article.like.remove(user)

        num_of_likes = int(User.objects.filter(article=article).count())
        return JsonResponse({'code': '0', 'count': num_of_likes})

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_following_by_id(request):
    user_id = request.GET.get('user_id')

    try:
        user = User.objects.get(pk=user_id)

    except User.DoesNotExist:
        return JsonResponse({'code': '32'})

    return JsonResponse({'ids': list(user.following.all())})

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_follower_by_id(request):
    user_id = request.GET.get('user_id')

    try:
        user = User.objects.get(pk=user_id)

    except User.DoesNotExist:
        return JsonResponse({'code': '32'})

    return JsonResponse({'ids': list(user.following_set.all())})

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_profile_image_thumbnail_by_user_id(request):
    user_id = request.GET.get('user_id')

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'code':'32'})

    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'user')
    file_name = 'profile_image_' + str(user.pk) + '_thumbnail.jpeg'

    file_path = os.path.join(path, file_name)

    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f, content_type="image/jpeg")
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

    except FileNotFoundError:
        return JsonResponse({'code': '29'})

    else:
        return response
