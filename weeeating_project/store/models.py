from django.db      import models
from django.utils   import timezone

from user.models    import User

class Store(models.Model):
    name        = models.CharField(max_length=45)
    description = models.TextField()
    delivery    = models.BooleanField(null=True)
    address     = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'stores'

class StoreTag(models.Model):
    store   = models.ForeignKey(Store, on_delete=models.CASCADE)
    tag     = models.CharField(max_length=100, null=True)

    class Meta():
        db_table = 'store_tags'

class StoreImage(models.Model):
    store   = models.ForeignKey(Store, on_delete=models.CASCADE)
    image   = models.URLField(max_length=1000)

    class Meta():
        db_table = 'store_images'

class StoreLike(models.Model):
    store   = models.ForeignKey(Store, on_delete=models.CASCADE)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta():
        db_table = 'store_likes'

class StoreComment(models.Model):
    store       = models.ForeignKey(Store, on_delete=models.CASCADE)
    writer      = models.ForeignKey(User, on_delete=models.CASCADE)
    comment     = models.CharField(max_length=200)
    created_at  = models.DateTimeField(default=timezone.now)

    class Meta():
        db_table = 'store_comments'


