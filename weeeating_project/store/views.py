import json
import requests
import random
import jwt_utils
import my_settings

from django.http import JsonResponse
from django.db.models import Count
from django.views import View
from .models import Store, StoreTag, StoreImage, StoreComment, StoreLike


class LikeStoreView(View): # 음식점 좋아요/안좋아요 
    @jwt_utils.login_decorator
    def post(self,request,store_id):
        user_id = request.user

        store = StoreLike.objects.filter(store_id=store_id, user_id=user_id.id)

        if user_id.name != None:
            if store.exists() :
                store.delete()

                return JsonResponse({'MESSAGE' :'UNLIKE_SUCCESS'}, status=200)

            StoreLike.objects.create(
                store_id = store_id,
                user_id = user_id.id
            )

            return JsonResponse({'MESSAGE' : 'LIKE_SUCCESS'}, status=201)

        return JsonResponse({'MESSAGE' : 'NEED_USER_NAME'}, status=200)


#class LikeRankView(View):
#    def get(self,request):
#        user_id = 1
#        stores = Store.objects.prefetch_related('storeimage_set','storelike_set','storetage_set')
#
#        test = Store.objects.annotate(count=Count('storelike__store_id')).order_by('-count')
#
#        info = [{
#            "id" : store.id,
#            "image" : store.storeimage_set.first().image,
#            "name" : store.name,
#            "like_count" : store.storelike_set.count(),
#            "like_state" : store.storelike_set.filter(user_id=user_id).exists()
#        } for store in utest][:5]
#
#
#        return JsonResponse({'ranking' : info}, status=200)
#



class StoreListView(View):
    @jwt_utils.login_decorator
    def get(self,request):
        user_id = request.user

        print("user_id:", user_id)

#        if user_id != None :
#            user_id = request.user.id
#
#        else :
#           # user_id = non_login_user
#            non_login_user = user_id 

        tag = request.GET.get('tag', None)
        sort = request.GET.get('sort', None)
 
        def info_list(tag_filter):

            stores = Store.objects.prefetch_related('storeimage_set','storelike_set','storetag_set').all()

            if user_id == None:
                info = [{
                    "id" : store.id,
                    "image" : store.storeimage_set.first().image,
                    "name" : store.name,
                    "like_count" : store.storelike_set.count(),
                    "like_state" : False
                } for store in tag_filter]

            else :
                info = [{
                    "id" : store.id,
                    "image" : store.storeimage_set.first().image,
                    "name" : store.name,
                    "like_count" : store.storelike_set.count(),
                    "like_state" : store.storelike_set.filter(user_id=user_id).exists()
                } for store in tag_filter]

            return info

        stores = Store.objects.prefetch_related('storeimage_set','storelike_set','storetag_set').all()

        if tag == 'alcohol' :
            alcohol_list = {
                'soju' : info_list([store for store in stores if store.storetag_set.filter(tag='soju')]),
                'beer' : info_list([store for store in stores if store.storetag_set.filter(tag='beer')]),
                'makgeolli' : info_list([store for store in stores if store.storetag_set.filter(tag='makgeolli')])
            }

            store_list = alcohol_list

        elif tag == 'feather' :
            feather_list = {
                'feather' : info_list([store for store in stores if store.storetag_set.filter(tag='feather')])
            }

            store_list = feather_list

        elif sort == 'random' :
            random_info = {
                'random' : info_list([stores.order_by("?").first()])
            }
            store_list = random_info

 #like_ranking부분인데 수정필요함 
        elif sort == 'like' :
            like_rank = {
                'like' : info_list([store for store in stores.annotate(count=Count('storelike__store_id')).order_by('-count')][:5])}

            store_list = like_rank

        else :
            store_list = info_list(stores)

        return JsonResponse({'store_list' : store_list}, status=200)


class StoreDetailView(View):
    @jwt_utils.login_decorator
    def get(self,request,store_id):
        user_id = request.user

        print("user_id:",user_id)

        stores = Store.objects.filter(id = store_id).all()

        store_images = StoreImage.objects.filter(store_id = store_id)

        store_info = [{
            "name" : store.name,
            "description" : store.description,
            "delivery" : store.delivery,
            "address" : store.address
        } for store in stores]

        images = [image.image for image in store_images]

        like_count = len(StoreLike.objects.filter(store_id = store_id))

        if user_id != None : 
            like = StoreLike.objects.filter(user_id = user_id.id, store_id = store_id).exists()

        else :
            like = False

        return JsonResponse({'store_info' : store_info, 'like_count' : like_count, 'like' : like, 'store_images' : images}, status=200)


class StoreCommentView(View):
    @jwt_utils.login_decorator
    def post(self,request,store_id):
        user_id = request.user
        data = json.loads(request.body)

        if user_id.name != None:
            StoreComment.objects.create(
                comment = data['comment'],
                store_id = store_id,
                writer_id = user_id.id
            )
            return JsonResponse({'MESSAGE' : 'CREATE_SUCCESS'}, status=201)

        return JsonResponse({'MESSAGE' : 'NEED_USER_NAME'}, status=200)

    def get(self,request,store_id):
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 5))

        comments = StoreComment.objects.filter(store_id=store_id).select_related('writer').all()

        count_comments = comments.count()
        comment_list = [{
            "id" : comment.id,
            "comment" : comment.comment,
            "created_at" : comment.created_at.strftime("%Y-%m-%d %H:%M"),
            "writer_id" : comment.writer.id,
            "writer_name" : comment.writer.number + "기 " + comment.writer.name
        } for comment in comments][::-1][offset:offset+limit]

        return JsonResponse({'count_comments' : count_comments,'comment_list' : comment_list},status=200)

    @jwt_utils.login_decorator
    def patch(self,request,store_id,comment_id):
        user_id = request.user
        data = json.loads(request.body)
        comment = StoreComment.objects.get(id = comment_id)

        if comment.writer_id == user_id.id :
            StoreComment.objects.filter(id=comment_id).update(
                comment = data['comment']
            )
            return JsonResponse({'MESSAGE' : 'UPDATE_SUCCESS'},status =200)
        return JsonResponse({'MESSAGE' : 'ACCESS_DENIED'}, status=403)

    @jwt_utils.login_decorator
    def delete(self,request,store_id,comment_id):
        user_id = request.user

        comment = StoreComment.objects.get(id = comment_id)

        if comment.writer_id == user_id.id : 
            comment.delete()

            return JsonResponse({'MESSAGE' : 'DELETE_SUCCESS'},status=200)
        return JSonResponse({'MESSAGE' : 'ACCESS_DENIDE'}, status=403)









