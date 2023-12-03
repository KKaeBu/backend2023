# 실행환경

memo.py 는 Python3 Flask 로 되어있습니다.

# 필요 패키지 설치

필요한 패키지 목록은 `requirements.txt` 에 있습니다. `pip` 을 이용해 필요 패키지를 설치합니다.
(필요시 `virtualenv` 환경을 이용하세요.)

```
$ pip install -r requirements.txt
```

# 실행 예시

## Local 접근

local 환경에서 접근하려면 다음과 같이 app을 실행시킵니다.
```
$ flask --app memo run --port 포트 번호
```
또는
```
$ python3 memo.py
```
이후 브라우저의 url상에
```
http://localhost:8000
```
로 접근하면 확인이 가능합니다.

## AWS ELB 접근

AWS의 ELB를 사용해 확인하려면
```
http://60172216-lb-358060437.ap-northeast-2.elb.amazonaws.com/memo/
```
로 접근하면 확인이 가능합니다.

# 코드 설명

## `@app.route('/')`

```
    if userId:
        if rdb.exists(f'user:{userId}'):
            print(rdb.get(f'user:{userId}'))
            user_json = rdb.get(f'user:{userId}')
            user = dict(json.loads(user_json))
            name = user['name']
```
쿠키를 통해 이전에 사용자의 방문 여부를 확인하고 DB에 사용자 데이터를 유무를 검색합니다.
만일 있다면 DB에 저장된 사용자 이름으로 name 값을 지정합니다.

## `@app.route('/oauth2')`

사용된 Redirect URI는 다음과 같습니다.

* `Redirect URI` : `http://localhost:8000/oauth2` (in local)
* `Redirect URI` : `http://<ec2 instance public ip>:8000/memo/oauth2` (in aws ec2)


1. `state & code` : naver api로부터 authorization 정보를 받아온다.
  ```
    code = request.args.get('code')
    state = request.args.get('state')
  ```

2. `access token` : naver api로부터 access token을 받아온다. (state, code 필요)
  ```
    token_params={
        'grant_type': 'authorization_code',
        'client_id': naver_client_id,
        'client_secret': naver_client_secret,
        'code': code,
        'state': state,
    }
    urlencoded = urllib.parse.urlencode(token_params)
    token_url = f"https://nid.naver.com/oauth2.0/token?{urlencoded}"
    token_resp = requests.get(token_url)
    ...
    access_token = token_resp.json()['access_token']
  ```
  
  3. `profile` : access token을 사용해 유저 데이터를 받아온다. (유저의 이름을 포함)
  ```
    profile_headers = {
        'Authorization': f'Bearer {access_token}'    
    }
    profile_url = "https://openapi.naver.com/v1/nid/me"
    profile_resp = requests.get(profile_url, headers=profile_headers)
    ...
    profile = profile_resp.json()['response']
  ```

  4. `DB save` : user 고유 id와 이름(name)을 저장합니다. (json 으로 저장, redis 사용)
  ```
  user = {
      'id': user_id,
      'name': user_name    
}
  #db저장
  user_serialized_json = json.dumps(user).encode('utf-8')
  rdb.set(f'user:{user_id}', user_serialized_json)
  ```

  주의. `redirect 설정` : 위 과정을 마친 후 돌아가는 redirect 주소 설정 (local -> '/', ec2 -> '/memo')
  ```
  response = redirect('/') # in local
  response = redirect('/memo') # in aws elb ec2
  ```

## `@app.route('/memo', methods=['GET'])`

  주의. `redirect 설정` : 비 로그인시 첫 페이지로 이동
  ```
  if not userId:
    return redirect('/') # in local
    return redirect('/memo') # in aws elb ec2
  ```
  
  DB에서 해당하는 user의 메모를 불러옵니다. (결과를 result에 저장)
  ```
    if rdb.exists(f'user:{userId}:memos'):
        memo_list = rdb.lrange(f'user:{userId}:memos', 0, -1)
        for memo in memo_list:
            m = dict(json.loads(memo))
            result.insert(0, m)
  ```
  lrange를 사용해서 redis에 value에 list로 저장되있는 데이터를 꺼내옵니다.

  ## `@app.route('/memo', methods=['POST'])`

  주의. `redirect 설정` : 비 로그인시 첫 페이지로 이동
  ```
    if not userId:
        return redirect('/') # in local
        return redirect('/memo') # in aws elb ec2
  ```
  
  클라이언트에게 받은 JSON 데이터속 메모 데이터를 추출 후 DB에 저장.
  ```
    m = json.dumps(dict(request.json)).encode('utf-8')

    rdb.rpush(f'user:{userId}:memos', m)
  ```
  해당하는 userId의 의 데이터에 새로운 메모를 list형태로 추가. (list요소는 JSON)


## 네이버 Redirct URI 리스트

* `http://localhost:8000/oauth2`
* `http://3.35.219.88:8000/memo/oauth2` ec2: 60172216-1
* `http://13.125.197.68:8000/memo/oauth2` ec2: 60172216-2


# DB 사용

DB는 AWS의 EC2중 60172216-db 인스턴스에 Docker를 설치하여 Redis image를 다운받아 container를 실행시켰습니다.

* `port` : `6379:6379`
* `container name` : `memo_redis`
* `version` : `lastest`

# 문제 해결

만일 elb주소를 통해 접근시 서버 에러 혹은 런타임 에러가 발생한다면
DB용 EC2인 60172216-db 인스턴스를 실행시켜 다음 명령어를 실행해봅니다.

* `sudo docker ps -a` : 현재 실행 혹은 중지중인 container 확인

만일 memo_redis 라는 redis conatiner가 중지중일시 해당 container를 재실행시켜줍니다.

* `sudo docker start memo_redis` : memo_redis 라는 이름을 가진 container를 실행시킵니다.