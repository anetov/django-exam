from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):  # Модель профиля User для его расширения
    user = models.OneToOneField(User, on_delete=models.CASCADE) # для связи с ним
    additional_info = models.TextField() # доп. инфо. для пользователя

    def __str__(self):  # метод класса для вывода в админ панеле
        return f'Profile of {self.user.username}' #
    
@receiver(post_save, sender=User)  #  сигнал создания пользователя
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Post(models.Model):  # модель для поста
    author = models.ForeignKey(User, on_delete=models.CASCADE) # поле модели для связи с автором поста
    title = models.CharField(max_length=155) # поле названия поста
    content = models.TextField() # поле для описания поста
    image = models.ImageField(upload_to='post_images/', blank=True, null=True) # поле для изображения
    created_at = models.DateTimeField(null=True, blank=True) # поле даты и времени создания поста

    def __str__(self):
        return self.title

class Comment(models.Model):  # модель для комментария 
    author = models.ForeignKey(User, on_delete=models.CASCADE) # поле связи коммента с его автором
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # поле связи коммента с постом
    content = models.TextField() # поле описания коммента
    created_at = models.DateTimeField(null=True, blank=True) # поле даты и времени коммента

    def __str__(self):
        return f'Comment by {self.author} on post {self.post}'
