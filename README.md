# DotPlaceServer

API
=============================

1. 회원가입
- url: /sign_up
- method : POST
- request

Data|Description
---|---
user name|required
nick name|required
phone number|required
pass word|required
email|required
birthday|required
gender|required
nation|required
profile image|optional

- response
{
	'id': profile.pk
	'code': '301'
}

- ErrorCode
없음
-----------------------------
2. 로그인
미구현
-----------------------------
3. trip 생성
- url: /trip/new
- method : POST
- request

Data|Description
---|---
title|required
owner index|required
owner id|required

- response
{
	'trip id': trip.pk
	'code': '301'
}

- ErrorCode
없음
-----------------------------
4. position 생성
- url: /position/new
- method : POST
- request

Data|Description
---|---
lat|required
lng|required
type|required
duration|required
trip id|required

- response
{
	'position id': position.pk
	'code': '301'
}

- ErrorCode
없음
-----------------------------
5. article 생성
- url: /article/new
- method : POST
- request

Data|Description
---|---
content|required
position id|required

- response
{
	'article id': article.pk
	'code': '301'
}

- ErrorCode
없음
-----------------------------
6. article image 생성
- url: /article_image/new
- method : POST
- request

Data|Description
---|---
image|required(FILE)
article id|required

- response
{
	'article image id': article_image.pk
	'code': '301'
}

- ErrorCode
없음
-----------------------------
7. article 탐색 : trip id
- url: /article/search/trip_id
- method : GET
- request

Data|Description
---|---
trip_id|required

- response
{
	'article id': result
}

- ErrorCode
없음
-----------------------------
8. article 탐색 : radius
- url: /article/search/radius
- method : GET
- request

Data|Description
---|---
lat|required
lng|required
radius|required

- response
{
	'article id': result
}

- ErrorCode
없음
-----------------------------
9. user 탐색 : user id
- url: /user/search/id
- method : GET
- request

Data|Description
---|---
user_id|required

- response
{
'user id': user_id,
'user name': user_name,
'email': email,
'nick name': nick_name,
'phone number': phone_number, 
'birthday': birthday, 
'gender': gender, 
'nation': nation
}

- ErrorCode
{
'user id': '-1'
}
-----------------------------
10. article 탐색 : article id
- url: /article/search/id
- method : GET
- request

Data|Description
---|---
article_id|required

- response
{
'user id': owner_id, 
'time': time, 
'content': content, 
'image ids': image_ids
}

- ErrorCode
{
'user id': '-1'
}
-----------------------------
11. 뉴스피드 탐색
- url: /news_feed/view
- method : GET
- request

Data|Description
---|---
article_id|required

- response
{
'trip id': trip_id,
'time': time,
'image id': image_id[0]
}

- ErrorCode
{
'trip id': '-1'
}
-----------------------------
12. image 탐색
- url: image/search/id
- method : GET
- request

Data|Description
---|---
image_id|required
dir_id|required(only for type 2, 3)
type|required

type 0: profile image thumbnail  
type 1: profile image  
type 2: article image thumbnail  
type 3: article image  

image_id: 각 경우에 있어 profile image pk와 article image pk를 의미함.  
dir_id: type 2, 3에 있어 article pk를 의미함.  

- response  
image file  

    File description
    - HttpResponse  
    - content_type="image/jpeg"  
    - response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)  


- ErrorCode
{
'code': '-1'
}
