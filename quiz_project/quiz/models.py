from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class Result(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user.username} - {self.score}"
