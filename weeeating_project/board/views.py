import json
import requests
#import jwt_utils
import my_settings

from django.http import JsonResponse
from django.views import View
from .models import Board, BoardComment
from user.models import User

class BoardView(View):
    #@decorator
    def get(self,request): 
        offset = int(request.GET.get('offset', 0))
        limit = int(reqeust.GET.get('limit', 5))

        total_board = len(Board.objects.all())

        if offset > total_board:
            return JsonResponse({'MESSAGE' : 'OFFSET_OUT_OF_RANGE'}, status=400)

        recent_list = list(Board.objects.all().select_related('writer').prefetch_related('boardcomment_set'))

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
    def post(self,request):
        #user_id = request.user.id 
        data = json.loads(request.body)

        new_board = Board.objects.create(
            writer_id = 1,
            #writer_id = User.objects.get(id=user_id).id,
            title = data['title'],
            content = data['content']
        )

        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)



class BoardDetailView(View): #상세페이지 조회,수정,삭제
    #@decorator
    def get(self,request,board_id):
        #user_id = request.user.id
        offset = int(request.GET.get('offset', 0))
        limit = int(reqeust.GET.get('limit', 5))

        board_info = Board.objects.filter(id = board_id).select_related('writer').prefetch_related('boardcomment_set').all()

        comments_list = BoardComment.objects.filter(board_id = board_id).select_related('writer')

        board_detail =[{
            'title' : board.title,
            'writer_id' : board.writer.id,
            'writer' : board.writer.name,
            'content' : board.content,
            'created_at' : board.created_at.date()
        } for board in board_info]

        count_comments = len(comments_list)

        board_comments = [{
            'comment_id' : comment.id,
            'comment_writer' : comment.writer.name,
            'comment_writer_id' : comment.writer.id,
            'comment_content' : comment.comment,
            'comment_created_at' : comment.created_at.strftime("%Y-%m-%d %I:%M")}
            for comment in comments_list][::-1][offset:offset+limit]

        return JsonResponse({'board_info':board_detail, 'count_comments':count_comments, 'board_comments':board_comments} , status=200)

    def patch(self,request,board_id):
        #user_id = request.user_id
        data = json.loads(request.body)
        user_id = 1

        board = Board.objects.get(id=board_id)

        if board.writer_id == user_id :
            Board.objects.filter(id=board_id).update(
                title = data['title'],
                content = data['content'])
            return JsonResponse({'MESSAGE' : 'UPDATE_SUCCESS'}, status=200)
        return JsonResponse({'MESSAGE' : 'ACCESS_DENIED'}, status=403)

    def delete(self,request,board_id):
        #user_id = request.user_id
        user_id = 1

        board = Board.objects.get(id=board_id)

        if board.writer_id == user_id :
            board.delete()
            return JsonResponse({'MESSAGE' : 'DELETE_SUCCESS'}, status=200)
        return JsonResponse({'MESSAGE' : 'ACCESS_DENIED'}, status=403)

class BoardCommentView(View): #게시글 댓글(생성,수정,삭제) -> CommentView로 수정하기

    #@decorator
    def post(self,request,board_id):
        #user_id = request.user.id
        user_id = 1
        data = json.loads(request.body)

        print(data)

        BoardComment.objects.create(
            board_id = board_id,
            writer_id = user_id,
            comment = data['comment']
        )

        return JsonResponse({'MESSAGE' : 'COMMENT_CREATE_SUCCESS'},status=201)

    #@decorator
    def patch(self,request,board_id,comment_id):
        #user_id = request.user.id
        user_id = 1
        data = json.loads(request.body)
        comment_writer_id = BoardComment.objects.get(id = comment_id).writer_id

        if comment_writer_id == user_id :
            BoardComment.objects.filter(id=comment_id).update(
                comment = data['comment']
            )

            return JsonResponse({'MESSAGE' : 'UPDATE_SUCCESS'}, status=200)
        return JsonResponse({'MESSAGE' : 'ACCESS_DENIED'}, status=403)

    def delete(self,request,board_id,comment_id):
        #user_id = request.user.id
        user_id = 1

        comment = BoardComment.objects.get(id = comment_id)

        if comment.writer_id == user_id :
            comment.delete()

            return JsonResponse({'MESSAGE' : 'DELETE_SUCCESS'}, status=200)
        return JsonResponse({'MESSAGE' : 'ACCESS_DENIED'}, status=403)





