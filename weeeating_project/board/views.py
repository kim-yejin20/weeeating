import json
import requests
#import jwt_utils
import my_settings

from django.http import JsonResponse
from django.views import View
from .models import Board, BoardComment

#깃
class BoardView(View):
    #@decorator
    def get(self, request):
        offset = 0
        limit = 5
        recent_list = list(Board.objects.all().select_related('writer').prefetch_related('boardcomment_set'))
        #user_id = request.user.id

        total_board = len(Board.objects.all())

        board_list =[{
            'id' : board.id,
            'title' : board.title,
            'writer_id' : board.writer_id,
            'writer' : board.writer.name,
            'created_at' : board.created_at.strftime("%Y-%m-%d %I:%M:%S"),
            'comments' : len([par.comment for par in board.boardcomment_set.filter(board_id = board.id)])
        } for board in recent_list][::-1][offset:offset+limit]


        return JsonResponse({'board_list' : board_list, "total_board" : total_board}, status=200)

    #@decorator
    def post(self, request):
        #user_id = request.user.id
        offset = 0
        limit = 5
        data = json.loads(request.body)
        print(data)

        new_board = Board.objects.create(
            writer_id = 1,
            #writer = User.objects.get(id=user_id),
            title = data['title'],
            content = data['content']
        )

        #new_list = board_list()

#        board_list = list(Board.objects.all().select_related('writer').prefetch_related('boardcomment_set__comment'))
#        new_list = [{
#            'id' : board.id,
#            'title' : board.title,
#            'writer_id' : board.writer_id,
#            'writer' : board.writer.name,
#            'created_at' : board.created_at.strftime("%Y-%m-%d %I:%M:%S"),
#            'comments' : len([par.comment for par in board.boardcomment_set.filter(board_id = board.id)])
#        } for board in board_list]#[offset:offset+limit]

        return JsonResponse({'Message' : 'SUCCESS'}, status=201)



class BoardDetailView(View):
    #@decorator
    def get(sefl, request, board_id): #상세페이지 조회 
        #user_id = request.user.id

        board_info = Board.objects.filter(id = board_id).values()



        return JsonResponse({'board_info' : board_info} , status=200)

