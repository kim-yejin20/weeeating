import json
import re
import bcrypt
import jwt
import requests
import urllib3
import sys
import jwt_utils

from django.http import JsonResponse
from django.views import View
from .models import User

from my_settings import SECRET_KEY, ALGORITHM



class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)

        print(data)

        email_test      ='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        password_test   ='^[A-Za-z0-9]{6,}$'

        try :
            if re.match(email_test, data['email']) == None :
                return JsonResponse({'MESSAGE' : 'EMAIL_ERORR'}, status = 401)

            elif re.match(password_test, data['password']) == None :
                return JsonResponse({'MESSAGE' : 'PASSWORD_ERROR'}, status = 401)

            elif User.objects.filter(email = data['email']).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL_ALREADY_EXISTS'}, status = 404)

            else :
                User.objects.create(
                    number      = data['number'],
                    name        = data['name'],
                    email       = data['email'],
                    password    = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))

                db_email = User.objects.get(email=data['email'])

                token = jwt.encode({'id' : db_email.id},SECRET_KEY,ALGORITHM)
                user_id = db_email.id

                return JsonResponse({'MESSAGE' : 'USER_SIGNUP_SUCCESS', 'Authorization' : token, 'user_id' :user_id}, status = 201)

        except KeyErro as e:
            return JsonResponse({'MESSAGE' : f'KEY_ERROR:{e}'}, status = 400)


class LoginView(View):
    def post(self,request):
        data = json.loads(request.body)

        print(data)

        try :
            if User.objects.filter(email=data['email']).exists():

                db_email= User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'),db_email.password.encode('utf-8')) == True:

                    print(jwt)
                    print(sys.version)
                    token = jwt.encode({'id' : db_email.id},SECRET_KEY,ALGORITHM)
                    user_id = db_email.id
                    print(user_id)
                    print(token)
                    print(type(token))

                    return JsonResponse({'MESSAGE' : 'SUCCESS', 'Authorization' : token, 'user_id' : user_id}, status=200)
                else :
                    return JsonResponse({'MESSAGE' : 'EMAIL_OR_PASSWORD_ERROR'}, status=400)
            else :
                return JsonResponse({'MESSAGE' : 'EMAIL_DOES_NOT_EXIST'}, status=400)

        except KeyError as e:
            return JsonResponse({'MESSAGE' : f'KEY_ERROR{e}'}, status=400)


"""
class SocialLoginView(View):
    def get(self,request):
        try:
            access_token = request.headers['Authorization']
            google_header = {'Authorization':f'Bearer {access_token}'}

            url          = 'https://www.googleapis.com/userinfo/v2/me'
            response     = requests.get(url, headers=google_header)
            user         = response.json()

            if user['kakao_account']['profile'].get('profile_image_url'):
                image = user['kakao_account']['profile']['profile_image_url']
            else:
                image = None

            if user.get('id'):
                user = User.objects.get_or_create(
                    social_login_id = user.get('id'),
                    name            = user['kakao_account']['profile']['nickname'],
                    social          = SocialPlatform.objects.get(platform='kakao'),
                    image_url       = image
                    )[0]
                access_token = jwt.encode({'id': user.id},SECRET_KEY,algorithm= ALGORITHM)

                return JsonResponse({"access_token": access_token}, status=200)

            return JsonResponse({"Message": "INVALID_TOKEN"}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f"{e}"}, status=400)

class SocialLoginView(View):
    def post(self,request):
        api_url = 'https://www.googleapis.com/userinfo/v2/me'
        google_token = request.headers.get('AUTHORIZATION', None)
        token_type = 'Bearer'

        if not google_token :
            return JsonResponse({'MESSAGE' : 'TOKEN_REQUIRED'}, status=400)

        response = requests.get(
            api_url,
            headers = {
                'AUTHORIZATION' : '{} {}'.format(token_type, google_token)
            }
        ).json()

        if not 'email' in response:
            return JsonRepsonse({'MESSAGE' : 'EMAIL_REQUIRED'}, status=405)

        user = User.objects.get_or_create(email=response['email'])
        access_token = generate_token(user)

        return JsonResponse({'access_token' : access_token}, status=200)

"""

class SocialLoginView(View):
    def post(self, request):
        urllib3.disable_warnings()
        access_token    = request.headers['Authorization']
        headers         = {"Authorization": f"Bearer {access_token}"}
        url             = 'https://www.googleapis.com/userinfo/v2/me'
        response        = requests.get(url, headers=headers, verify=False)
        user            = response.json()

        print(response.text)
        print(response.status_code)

        if user.get('id'):
            user = User.objects.get_or_create(social_id = user.get('id'), email = user.get('email'))[0]

            #db_email= User.objects.get(email=data['email'])
            #user         = User.objects.get_or_create(social_id=user.get('id'))[0]
            access_token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)
            user_id = user.id

            if user.name == None : 
                first_visit = True
            else :
                first_visit = False

            return JsonResponse({"Authorization": access_token, "user_id" : user_id, "FRIST_VISIT" : first_visit}, status=200)

        return JsonResponse({"Message": "INVALID_TOKEN"}, status=401)

class GoogleInfoView(View):
    @jwt_utils.login_decorator
    def post(self,request):
        data = json.loads(request.body)

        user_id = request.user

        print(user_id)

        User.objects.filter(id = user_id.id).update(
            number = data['number'],
            name = data['name']
        )

        return JsonResponse({'MESSAGE' : 'UPDATE_SUCCESS'}, status=201)





"""
    def get(self,request):
        urllib3.disable_warnings()
        access_token = request.header['Authorization']
        headers = 
        data = json.loads(request.body)
        id_token = request.headers.get('Authorization')
        user_request = requests.get('https://www.googleapis.com/userinfo/v2/me')

        #user_request = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
        user_info    = user_request.json()
        google_email = user_info.get('email')
        google_name  = user_info.get('name')

        if User.objects.filter(email = google_email).exists():
            user       = User.objects.get(email = google_email)
            token      = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm = ALGORITHM)
            return_key = token.decode('utf-8') #'uuid' : user.uuid}}

            return JsonResponse({'return_key' : return_key}, status = 200)

        user = User.objects.create(
            socail_id = google_email,
            name  = google_name,
            number = data['number'],
            #uuid  = str(uuid.uuid3(uuid.NAMESPACE_DNS, google_email).hex)
        )

        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

"""
#        token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm = ALGORITHM)
#        user_uuid  = user.uuid
#        return_key = {'user' : {'token' : token.decode('utf-8'), 'uuid' : user_uuid}}
#







