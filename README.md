# Django throttle handle

## Name
Login rate throttle

## Description
this util use for Django throttle handele on login APIs

## Usage
for example in your views.py you can use this util as blow:

views.py:
```
email = request.data.get("email", None)
password = request.data.get("password", None)
if not login_rate_throttle(request, email):
    res = {"error": "you can try after 10 minutes later"}
    return Response(res, status.HTTP_429_TOO_MANY_REQUESTS)
```

nginx:
```
location @proxy_api {
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header X-Url-Scheme $scheme;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_redirect off;
    proxy_pass   http://127.0.0.1:8080;
}

location ~ ^/api {
    try_files $uri @proxy_api;
}
```
