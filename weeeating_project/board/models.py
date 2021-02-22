from django.db import models
from django.utils import timezone

from user.models import User

class Board(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta():
        db_table = 'boards'

class BoardComment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    writer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta():
        db_table = 'board_comments'

class BoardAttachment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=200)

    class Meta():
        db_table = 'board_attachments'
