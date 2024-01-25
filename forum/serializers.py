from rest_framework import serializers

from api.models import *
from api.serializers import UserSerializer

from .models import *


class PostForumQuestionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    course_id = serializers.IntegerField()
    upvotes = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ForumQuestion
        fields = [
            "id",
            "user_id",
            "course_id",
            "title",
            "slug",
            "short_description",
            "description",
            "upvotes",
            "number_of_upvotes",
            "date_posted",
            "date_changed",
        ]
        read_only_fields = ["slug"]

    def validate_course_id(self, value):
        if not Courses.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid course id")
        return value

    # def create(self, validated_data):
    #     user_id = self.context["user_id"]
    #     course_id = validated_data["course_id"]
    #     title = validated_data["title"]
    #     description = validated_data["description"]

    #     return ForumQuestion.objects.create(
    #         user_id=user_id,
    #         course_id=course_id,
    #         title=title,
    #         description=description,
    #         **validated_data,
    #     )

    def save(self, **kwargs):
        user_id = self.context["user_id"]
        course_id = self.validated_data["course_id"]
        title = self.validated_data["title"]
        description = self.validated_data["description"]

        try:
            num = range(100, 1000)
            ran = random.choice(num)
            slug = f"{(slugify(title))}-{ran}"
            forum_question = ForumQuestion.objects.create(
                user_id=user_id,
                slug=slug,
                course_id=course_id,
                title=title,
                description=description,
            )
            return forum_question

        except Exception as e:
            print("error: ", e)


class ForumAnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    forum_question_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ForumAnswer
        fields = [
            "id",
            "user_id",
            "forum_question_id",
            "num_of_upvotes",
            "description",
            "date_posted",
            "date_changed",
        ]
        # read_only_fields = ['user_id','forum_question_id']

    # def create(self, validated_data):
    #     user_id = self.context["user_id"]
    #     forum_question_id = self.context["forum_question_id"]
    #     description = validated_data["description"]
    #     forum_answer_instance = ForumAnswer.objects.filter(
    #         user_id=user_id,
    #         forum_question_id=forum_question_id
    #     ).first()
    #     if forum_answer_instance:
    #         for attr, value in validated_data.items():
    #             setattr(forum_answer_instance, attr, value)
    #         forum_answer_instance.save()
    #         return forum_answer_instance
    #     else:
    #         return ForumAnswer.objects.create(
    #             user_id=user_id,
    #             forum_question_id=forum_question_id,
    #             description=description,
    #             **validated_data,
    #         )

    def save(self, **kwargs):
        user_id = self.context["user_id"]
        forum_question_id = self.context["forum_question_id"]
        description = self.validated_data["description"]
        try:
            forum_answer = ForumAnswer.objects.create(
                user_id=user_id,
                forum_question_id=forum_question_id,
                description=description,
            )
            return forum_answer
        except Exception as e:
            print("Error creating forum answer : ", e)


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = ["value"]


class UpvoteAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpvoteAnswer
        fields = ["value"]
