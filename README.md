# Django throttle handle

## Name
Login rate throttle

## Description
this util use for Django throttle handele on login APIs

## Usage
for example in your views.py you can use this util as blow:
```
email = request.data.get("email", None)
password = request.data.get("password", None)
if not login_rate_throttle(request, email):
    res = {"error": "you can try after 10 minutes later"}
    return Response(res, status.HTTP_429_TOO_MANY_REQUESTS)
```
