import random

from django.db import models
from django.utils.text import slugify

from api.models import *
from utils.choices import LIKE_CHOICES


class ForumQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    upvotes = models.ManyToManyField(
        User, default=None, blank=True, related_name="upvotes"
    )
    date_posted = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_posted"]

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        num = range(100, 1000)
        ran = random.choice(num)
        self.slug = f"{(slugify(self.title))}-{ran}"
        super(ForumQuestion, self).save(*args, **kwargs)

    @property
    def short_description(self):
        return self.description[:150] + " ..."

    @property
    def number_of_upvotes(self):
        return self.upvotes.all().count()


class ForumAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forum_question = models.ForeignKey(ForumQuestion, on_delete=models.CASCADE)
    description = models.TextField()
    upvotes = models.ManyToManyField(User, default=None,blank=True, related_name='upvotes_answer')
    date_posted = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_posted"]

    def __str__(self):
        return f"{self.id}"

    @property
    def num_of_upvotes(self):
        return self.upvotes.all().count()


class Upvote(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_upvoted"
    )
    forum_question = models.ForeignKey(
        ForumQuestion, on_delete=models.CASCADE, related_name="forum_question"
    )
    value = models.CharField(max_length=10, choices=LIKE_CHOICES, default="Upvote")

    def __str__(self):
        return str(self.forum_question)

    class Meta:
        verbose_name = "Upvote"
        verbose_name_plural = "Upvotes"


class UpvoteAnswer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_upvoted_answer"
    )
    forum_answer = models.ForeignKey(
        ForumAnswer, on_delete=models.CASCADE, related_name="forum_answer"
    )
    value = models.CharField(max_length=10, choices=LIKE_CHOICES, default="Upvote")

    def __str__(self):
        return str(self.forum_question)

    class Meta:
        verbose_name = "Upvote Answer"
        verbose_name_plural = "Upvotes Answer"
