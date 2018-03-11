# DotPlaceServer

API
=============================

**회원가입을 제외하고는 request를 보낼 때 Header에 Token을 보내야함.**

Headers
- Key : Authorization
- Value : Token [Actual token info]

ex) curl command  
curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

-----------------------------

1. user 검색
- url: /user
- method : GET
- request : None

- response

Name|Type
---|---
user name|string
email|string
nick name|string
phone number|string
birthday|string
gender|string
nation|string

- status code

Code|Description
---|---
0|success
401|unauthorized

-----------------------------

2.user 정보 수정
- url: /user
- method : PUT
- request

Name|Description|Type
---|---|---
user name|optional|string
birthday|optional|string
gender|optional|string
nation|optional|string

- response : status code

- status code

Code|Description
---|---
0|success
401|unauthorized

-----------------------------

3. 회원탈퇴
- url: /user
- method : DELETE
- request : None
- response : status code

- status code

Code|Description
---|---
0|success
401|unauthorized

-----------------------------

4. 회원가입
- url: /sign_up
- method : POST
- request

Data|Description|Type
---|---|---
user name|required|string
nick name|required|string
phone number|required|string
pass word|required|string
email|required|string
birthday|required|string
gender|required|string
nation|required|string
profile image|optional|file

- response

Name|Type
---|---
code|string
id|string
token|string

- status code

Code|Description
---|---
0|success
1|필수 입력 값 미입력
2|Email or Phone number 중복
3|해당 유저의 프로필 사진을 찾을 수 없음(썸네일 생성 시)
4|해당 유저의 토큰을 찾을 수 없음
401|unauthorized

-----------------------------

5. 로그아웃
- url: /sign_out
- method : DELETE
- request : None

- response : status code

- status code

Code|Description
---|---
0|success
5|해당 유저의 토큰을 찾을 수 없음
401|unauthorized

-----------------------------

6. 비밀번호 변경
- url: /change_pw
- method : PUT
- request

Data|Description|Type
---|---|---
pass word|required|string

- response : status code

- status code

Code|Description
---|---
0|success
401|unauthorized

-----------------------------

7. article 검색
- url: /article
- method : GET
- request

Data|Description|Type
---|---|---
article_id|required|string

- response

Name|Type
---|---
code|string
user id|string
time|string
content|string
image ids|list

- status code

Code|Description
---|---
0|success
6|해당 article을 찾을 수 없음
401|unauthorized

-----------------------------

2. 로그인
- url: /sign_in
- method : POST
- request

Data|Description
---|---
user name|required
pass word|required

- response
{
	'code': '301'
}

- ErrorCode
{
	'code': '-1'
} 
-----------------------------
3. 로그아웃
- url: /sign_out
- method : GET
- request

Data|Description
---|---
user_name|required

- response
{
	'code': '301'
}

- ErrorCode
{
	'code': '-1'
} 
-----------------------------
4. trip 생성
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
5. position 생성
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
6. article 생성
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
7. article image 생성
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
8. article 탐색 : trip id
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
9. article 탐색 : radius
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
11. article 탐색 : article id
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
12. 뉴스피드 탐색
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
13. image 탐색
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
