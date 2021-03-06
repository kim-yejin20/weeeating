import json
import requests
import jwt_utils
import my_settings

from django.http import JsonResponse
from django.views import View
from .models import Board, BoardComment
from user.models import User

#깃
class BoardView(View):
    def get(self,request): 
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 5))

        total_board = len(Board.objects.all())

        if offset > total_board:
            return JsonResponse({'MESSAGE' : 'OFFSET_OUT_OF_RANGE'}, status=400)

        #recent_list = Board.objects.all().select_related('writer').prefetch_related('boardcomment_set')

        recent_list = Board.objects.all().select_related('writer').prefetch_related('boardcomment_set')


        #board_info = Board.objects.filter(id = board_id).select_related('writer').prefetch_related('boardcomment_set').all()

        board_list =[{
            'id' : board.id,
            'title' : board.title,
            'writer_id' : board.writer_id,
            'writer' : str(board.writer.number) + "기 " + str(board.writer.name),
            'created_at' : board.created_at.strftime("%Y-%m-%d"),
            'comments' : len([par.comment for par in board.boardcomment_set.filter(board_id = board.id)])
        } for board in recent_list[::-1]][offset:offset+limit]


        return JsonResponse({'board_list' : board_list, "total_board" : total_board}, status=200)

    @jwt_utils.login_decorator
    def post(self,request):
        user_id = request.user 
        data = json.loads(request.body)

        print(data)

        if user_id.name != None:
            new_board = Board.objects.create(
                writer_id = user_id.id,
                title = data['title'],
                content = data['content']
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
        return JsonResponse({'MESSAGE' : 'NEED_USER_NAME'}, status=200)


class BoardDetailView(View): #상세페이지 조회,수정,삭제
    def get(self,request,board_id):
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 5))

        board_info = Board.objects.filter(id = board_id).select_related('writer').prefetch_related('boardcomment_set').all()

        comments_list = list(BoardComment.objects.filter(board_id = board_id).select_related('writer'))

        board_detail =[{
            'title' : board.title,
            'writer_id' : board.writer.id,
            'writer' : board.writer.number + "기 " + board.writer.name,
            'content' : board.content,
            'created_at' : board.created_at.date()
        } for board in board_info]

        count_comments = len(comments_list)

        board_comments = [{
            'comment_id' : comment.id,
            'comment_writer' : comment.writer.number + "기 " + comment.writer.name,
            'comment_writer_id' : comment.writer.id,
            'comment_content' : comment.comment,
            'comment_created_at' : comment.created_at.strftime("%Y-%m-%d %H:%M")}
            for comment in comments_list][::-1][offset:offset+limit]

        return JsonResponse({'board_info':board_detail, 'count_comments':count_comments, 'board_comments':board_comments} , status=200)

    @jwt_utils.login_decorator
    def patch(self,request,board_id):
        user_id = request.user
        data = json.loads(request.body)
        print(data)

        board = Board.objects.get(id=board_id)

        if board.writer_id == user_id.id :
            Board.objects.filter(id=board_id).update(
                title = data['title'],
                content = data['content'])
            return JsonResponse({'MESSAGE' : 'UPDATE_SUCCESS'}, status=200)
        return JsonResponse({'MESSAGE' : 'ACCESS_DENIED'}, status=403)

    @jwt_utils.login_decorator
    def delete(self,request,board_id):
        user_id = request.user

        board = Board.objects.get(id=board_id)

        if board.writer_id == user_id.id :
            board.delete()
            return JsonResponse({'MESSAGE' : 'DELETE_SUCCESS'}, status=200)
        return JsonResponse({'MESSAGE' : 'ACCESS_DENIED'}, status=403)

class BoardCommentView(View): #게시글 댓글(생성,수정,삭제) -> CommentView로 수정하기

    @jwt_utils.login_decorator
    def post(self,request,board_id):
        user_id = request.user
        data = json.loads(request.body)

        print(data)

        if user_id.name != None :
            BoardComment.objects.create(
                board_id = board_id,
                writer_id = user_id.id,
                comment = data['comment']
            )
            return JsonResponse({'MESSAGE' : 'COMMENT_CREATE_SUCCESS'},status=201)
        return JsonResponse({'MESSAGE' : 'NEED_USER_NAME'}, status=200)

    @jwt_utils.login_decorator
    def patch(self,request,board_id,comment_id):
        user_id = request.user.id
        data = json.loads(request.body)
        comment_writer_id = BoardComment.objects.get(id = comment_id).writer_id

        if comment_writer_id == user_id :
            BoardComment.objects.filter(id=comment_id).update(
                comment = data['comment']
            )

            return JsonResponse({'MESSAGE' : 'UPDATE_SUCCESS'}, status=200)
        return JsonResponse({'MESSAGE' : 'ACCESS_DENIED'}, status=403)

    @jwt_utils.login_decorator
    def delete(self,request,board_id,comment_id):
        user_id = request.user.id

        comment = BoardComment.objects.get(id = comment_id)

        if comment.writer_id == user_id :
            comment.delete()

            return JsonResponse({'MESSAGE' : 'DELETE_SUCCESS'}, status=200)
        return JsonResponse({'MESSAGE' : 'ACCESS_DENIED'}, status=403)





