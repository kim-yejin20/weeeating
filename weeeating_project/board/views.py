import json
import requests
#import jwt_utils
import my_settings

from django.http import JsonResponse
from django.views import View
from .models import Board, BoardComment
from user.models import User

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

        new_board = Board.objects.create(
            writer_id = 1,
            #writer = User.objects.get(id=user_id),
            title = data['title'],
            content = data['content']
        )

        return JsonResponse({'Message' : 'SUCCESS'}, status=201)



class BoardDetailView(View):
    #@decorator
    def get(self, request, board_id): #상세페이지 조회 
        #user_id = request.user.id

        board_info = Board.objects.filter(id = board_id).select_related('writer').prefetch_related('boardcomment_set').all()
        comments_list = BoardComment.objects.filter(board_id = board_id).select_related('writer')

        print(comments_list)

        board_detail =[[{
            'title' : board.title,
            'writer_id' : board.writer.id,
            'writer' : board.writer.name,
            'content' : board.content,
            'create_at' : board.created_at.date()
        } for board in board_info],
        [{
            'count_comment' : len(comments_list),
            'comment_id' : comment.id,
            'comment_writer' : comment.writer.name,
            'comment_writer_id' : comment.writer.id,
            'comment_content' : comment.comment,
            'comment_created_at' : comment.created_at.strftime("%Y-%m-%d %I:%M:%S")}
            for comment in comments_list]]

        return JsonResponse({'board_info' : board_detail} , status=200)


class BoardCommentView(View):
    #@decorator
    def post(self,request,board_id):
        #user_id = request.user.id
        user_id = 1
        data = json.loads(request.body)

        BoardComment.objects.create(
            board_id = board_id,
            writer_id = user_id,
            comment = data['comment']
        )

        return JsonResponse({'MESSAGE' : "COMMENT_CREATE_SUCCESS"},status=201)

