import json
import requests
#import jwt_utils
import my_settings

from django.http import JsonResponse
from django.views import View
from .models import Board, BoardComment

#깃
class BoardMainView(View):
    #@decorator
    def get(self, request):
        recent_list = list(Board.objects.all().select_related('writer').prefetch_related('boardcomment_set'))[-5:]
        #user_id = request.user.id

        board_list =[{
            'id' : board.id,
            'title' : board.title,
            'writer' : board.writer.name,
            'created_at' : board.created_at,
            'comments' : len([par.comment for par in board.boardcomment_set.filter(board_id = board.id)])
        } for board in recent_list]

        return JsonResponse({'board_list' : board_list}, status=200)


class BoardPostView(View):
    #로그인 한 유저만 작성 가능(조건문 추가해야함)
    #@decorator
    def post(self, request):
        #user_id = request.user.id
        offset = 0
        limit = 5
        data = json.loads(request.body)

        new_board = Board.objects.create(
            writer_id = 1,
            #writer = User.objects.get(id=user_id),
            title = data['title'],
            content = data['content']
        )

        recent_list = list(Board.objects.all().select_related('writer').prefetch_related('boardcomment_set__comment'))

        print(recent_list)

        new_list = [{
            'id' : board.id,
            'title' : board.title,
            'writer_id' : board.writer_id,
            'writer' : board.writer.name,
            'created_at' : board.created_at.strftime("%Y-%m-%d %I:%M:%S"),
            'comments' : len([par.comment for par in board.boardcomment_set.filter(board_id = board.id)])
        } for board in recent_list][offset:offset+limit]

        return JsonResponse({'new_list' : new_list}, status=201)


