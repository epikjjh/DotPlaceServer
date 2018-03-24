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
code|string
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

- response

Name|Type
---|---
code|string
user id|string

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
-1|File not found
0|success
401|unauthorized

**File not found code : user profile & thumbnail image를 삭제하려 하였지만 이미 지워져 있을 때 발생(정상 삭제이나 code로 구분 함)**

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

**썸네일 생성 실패 시 원본 이미지 삭제**

-----------------------------

5. 로그인
- url: /sign_in
- method : POST
- request

Data|Description|Type
---|---|---
username|required|string
password|required|string

**여기서의 username은 phone number를 의미**

- response : token & status code

- status code

Code|Description
---|---
0|success
-1|already signed in(return existing token)
400|Bad Request:unable to log in with provided credentials

-----------------------------

6. 로그아웃
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

7. 비밀번호 변경
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

8. article 검색
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

9. article 생성
- url: /article
- method : POST
- request

Data|Description|Type
---|---|---
content|required|string
position id|required|string

- response

Name|Type
---|---
code|string
article id|string

- status code

Code|Description
---|---
0|success
7|해당 position을 찾을 수 없음
401|unauthorized

-----------------------------

10. article 수정
- url: /article
- method : PUT
- request

Data|Description|Type
---|---|---
article id|required|string
content|optional|string
position id|optional|string

- response

Name|Type
---|---
code|string
article id|string

- status code

Code|Description
---|---
0|success
8|해당 article을 찾을 수 없음
9|해당 position을 찾을 수 없음
401|unauthorized

-----------------------------

11. article 삭제
- url: /article
- method : DELETE
- request

Data|Description|Type
---|---|---
article id|required|string

- response

Name|Type
---|---
code|string
article id|string

- status code

Code|Description
---|---
0|success
10|해당 article을 찾을 수 없음
401|unauthorized

-----------------------------

12. article 검색 : radius
- url: /article/search/radius
- method : GET
- request

Data|Description|Type
---|---|---
lat|required|float
lng|required|float
radius|required|float

- response

Name|Type
---|---
code|string
article ids|list

- status code

Code|Description
---|---
0|success
401|unauthorized

-----------------------------

13. article 검색 : trip id
- url: /article/search/trip_id
- method : GET
- request

Data|Description|Type
---|---|---
trip_id|required|string

- response

Name|Type
---|---
code|string
article ids|list

- status code

Code|Description
---|---
0|success
401|unauthorized

-----------------------------

14. news feed
- url: /news_feed
- method : GET
- request

Data|Description|Type
---|---|---
article_id|required|string

- response

Name|Type
---|---
code|string
thumbnail id|integer
content|string
time|string
trip id|int

**thumbnail id의 경우 존재 하지 않으면 0을 반환**

- status code

Code|Description
---|---
0|success
11|해당 article을 찾을 수 없음
401|unauthorized

-----------------------------

15. comment 검색
- url: /comment
- method : GET
- request

Data|Description|Type
---|---|---
comment_id|required|string

- response

Name|Type
---|---
code|string
owner id|string
article id|string
content|string
time|string

- status code

Code|Description
---|---
0|success
12|해당 comment를 찾을 수 없음
401|unauthorized

-----------------------------

16. comment 생성
- url: /comment
- method : POST
- request

Data|Description|Type
---|---|---
article id|required|string
content|required|string

- response

Name|Type
---|---
code|string
comment id|string

- status code

Code|Description
---|---
0|success
13|해당 article을 찾을 수 없음
401|unauthorized

-----------------------------

17. comment 수정
- url: /comment
- method : PUT
- request

Data|Description|Type
---|---|---
comment id|required|string
article id|optional|string
content|optional|string

- response

Name|Type
---|---
code|string
comment id|string

- status code

Code|Description
---|---
0|success
14|해당 comment를 찾을 수 없음
15|해당 article을 찾을 수 없음
401|unauthorized

-----------------------------

18. comment 삭제
- url: /comment
- method : DELETE
- request

Data|Description|Type
---|---|---
comment id|required|string

- response : status code

- status code

Code|Description
---|---
0|success
16|해당 comment를 찾을 수 없음
401|unauthorized

-----------------------------

19. comment 검색 : article id
- url: comment/search/article_id
- method : GET
- request

Data|Description|Type
---|---|---
article id|required|string

- response

Name|Type
---|---
code|string
article id|string
comment ids|list

- status code

Code|Description
---|---
0|success
401|unauthorized

-----------------------------

20. trip 검색
- url: trip
- method : GET
- request

Data|Description|Type
---|---|---
trip_id|required|string

- response

Name|Type
---|---
code|string
owner id|string
owner index|string
title|string

- status code

Code|Description
---|---
0|success
17|해당 trip을 찾을 수 없음
401|unauthorized

-----------------------------

21. trip 생성
- url: trip
- method : POST
- request

Data|Description|Type
---|---|---
title|required|string
owner index|required|string

- response

Name|Type
---|---
code|string
trip id|string

- status code

Code|Description
---|---
0|success
401|unauthorized

-----------------------------

22. trip 수정
- url: trip
- method : PUT
- request

Data|Description|Type
---|---|---
trip id|required|string
title|optional|string
owner index|optional|string

- response

Name|Type
---|---
code|string
trip id|string

- status code

Code|Description
---|---
0|success
18|해당 trip을 찾을 수 없음
401|unauthorized

-----------------------------

23. trip 삭제
- url: trip
- method : DELETE
- request

Data|Description|Type
---|---|---
trip id|required|string

- response : status code

- status code

Code|Description
---|---
0|success
19|해당 trip을 찾을 수 없음
401|unauthorized

-----------------------------

24. position 검색
- url: position
- method : GET
- request

Data|Description|Type
---|---|---
position_id|required|string

- response

Name|Type
---|---
code|string
lat|float
lng|float
time|string
type|integer
duration|integer
trip id|string

- status code

Code|Description
---|---
0|success
20|해당 position을 찾을 수 없음
401|unauthorized

-----------------------------

25. position 생성
- url: position
- method : POST
- request

Data|Description|Type
---|---|---
lat|required|float
lng|required|float
type|required|integer
duration|required|integer
trip id|required|string

- response

Name|Type
---|---
code|string
position id|string

- status code

Code|Description
---|---
0|success
21|해당 trip을 찾을 수 없음
401|unauthorized

-----------------------------

26. position 삭제
- url: position
- method : DELETE
- request

Data|Description|Type
---|---|---
position id|required|string

- response : status code

- status code

Code|Description
---|---
0|success
22|해당 position을 찾을 수 없음
401|unauthorized

-----------------------------

27. article image 검색
- url: article_image
- method : GET
- request

Data|Description|Type
---|---|---
image_id|required|string
article_id|required|string

- response : image(jpeg) or status code

- status code

Code|Description
---|---
23|File not found : 해당 image를 찾을 수 없음
401|unauthorized

-----------------------------

28. article image 생성
- url: article_image
- method : POST
- request

Data|Description|Type
---|---|---
image|required|image
article id|required|string

- response

Name|Type
---|---
code|string
article image id|string

- status code

Code|Description
---|---
0|success
24|해당 article을 찾을 수 없음
25|File not found : 원본 image를 찾을 수 없음(thumbnail)
401|unauthorized

-----------------------------

29. article image 삭제
- url: article_image
- method : DELETE
- request

Data|Description|Type
---|---|---
image id|required|image

- response : status code

- status code

Code|Description
---|---
-1|File not found
0|success
26|해당 image를 찾을 수 없음(DB)
401|unauthorized

**File not found code : article image를 삭제하려 하였지만 이미 지워져 있을 때 발생(정상 삭제이나 code로 구분 함)**

-----------------------------

30. profile image 검색
- url: profile_image
- method : GET
- request : None

- response : image(jpeg) or status code

- status code

Code|Description
---|---
27|File not found : 해당 image를 찾을 수 없음
401|unauthorized

-----------------------------

31. profile image 수정
- url: article_image
- method : PUT
- request

Data|Description|Type
---|---|---
image|required|image

- response : status code

- status code

Code|Description
---|---
-1|File not found
0|success
28|해당 유저의 프로필 사진을 찾을 수 없음(썸네일 생성 시)

**썸네일 생성 실패 시 원본 이미지 삭제**
**File not found code : 기존 user profile & thumbnail image를 삭제하려 하였지만 이미 지워져 있을 때 발생(정상 수정이나 code로 구분 함)**

-----------------------------

32. profile image 삭제
- url: article_image
- method : DELETE
- request : None

- response : status code

- status code

Code|Description
---|---
-1|File not found
0|success

**File not found code : user profile & thumbnail image를 삭제하려 하였지만 이미 지워져 있을 때 발생(정상 삭제이나 code로 구분 함)**

-----------------------------

33. thumbnail image 검색 : profile image
- url: profile_image_thumbnail
- method : GET
- request : None

- response : image(jpeg) or status code

- status code

Code|Description
---|---
29|File not found : 해당 image를 찾을 수 없음
401|unauthorized

-----------------------------

34. thumbnail image 검색 : article image
- url: article_image_thumbnail
- method : GET
- request

Data|Description|Type
---|---|---
image_id|required|image
article_id|required|image

- response : image(jpeg) or status code

- status code

Code|Description
---|---
30|File not found : 해당 image를 찾을 수 없음
401|unauthorized

-----------------------------
