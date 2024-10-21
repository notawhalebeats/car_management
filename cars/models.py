from django.db import models 
from django.contrib.auth.models import User

class Car(models.Model):
    make = models.CharField('Производитель',max_length=100)
    model = models.CharField('Модель',max_length=100)
    year = models.IntegerField('Год производства')
    description = models.TextField('Описание',)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, related_name="комментариев", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Комментарий {self.author} на {self.car}"

