import json
import requests
#import jwt_utils
import my_settings

from django.http import JsonResponse
from django.views import View
from .models import Store, StoreTag, StoreImage, StoreComment, StoreLike


class LikeStore(View):
    #@decorator
    def post(self,request,store_id):
        #user_id = request.user.id
        user_id = 1

        data = json.loads(request.body)

        StoreLike.objects.create(
            store_id = store_id,
            user_id = user_id
        )

        return JsonResponse({'MESSAGE' : 'Like_SUCCESS'}, status=201)

"""
class LikeRanking(View):
    #@decorator
    def get(self, requsest):
        #user_id = request.user.id
        user_id = 1



class StoreList(View):
    #@decorator
"""








