import json
import jwt
import requests

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured

from user.models            import User
from my_settings            import SECRET_KEY, ALGORITHM

"""
def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):

        if "Authorization" not in request.headers :
            request.user = None

        else :
            access_token = request.headers.get('Authorization')
            print(access_token)
            data = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            print(data)
            user = User.objects.get(id=data['id']) 
            request.user = user


        return func(self, request, *args, **kwargs)

    return wrapper

"""
def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):

#        if "Authorization" not in request.headers:
#            return JsonResponse({"Message": "TOKEN_DOES_NOT_EXIST"}, status=401)

        access_token = request.headers.get('Authorization', None)

        #access_token = request.headers

        print("login_decorator:",access_token)

        try:
            if access_token != None :
                data = jwt.decode(access_token, SECRET_KEY, ALGORITHM)

                print(data)
                user = User.objects.get(id=data['id']) 
                request.user = user

            else :
                request.user = None
                print(request.user)
#
#        except jwt.DecodeError:
#            return JsonResponse({"Error_code": "INVALID TOKEN"}, status=403)

        except User.DoesNotExist:
            return JsonResponse({"Error_code": "UNKNOWN USER"}, status=401)

        return func(self, request, *args, **kwargs)

    return wrapper


