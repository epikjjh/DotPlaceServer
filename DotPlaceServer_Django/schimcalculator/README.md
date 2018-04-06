# DotPlaceServer

Schim server : celery + rabbitmq broker
=============================

1. stack
- celery
- sqlalchemy
- rabbitmq-server

2. task structure
- app name : schimcalculator
- broker user name : service / broker user pass word : dotplace1234
- virtual host name : schim
- command : celery -A schimcalculator worker --loglevel=info (manage.py가 위치한 디렉토리에서 실행할 것)
- task
  - number of task : 2  
  - calculator: 스침 점수 계산  
  - collector: 오래 된 dotplace 삭제  

3. caution
- rabbitmqctl 설정  
  1. broker user 설정  
  2. permission 설정  
  3. vhost 설정  

- 보안 설정
celery.py 내에 broker user name 및 password를 secret.py로 옮길 것
