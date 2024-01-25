from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, response, viewsets
from rest_framework.decorators import action

from forum.paginations import BasePagination

from .filters import *
from .models import *
from .serializers import *


class ForumQuestionViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ForumQuestionFilter
    search_fields = ["title", "description"]

    def get_queryset(self):
        return ForumQuestion.objects.prefetch_related("forumanswer_set").all()

    def get_serializer_class(self):
        if self.action == "upvotes":
            return UpvoteSerializer
        return PostForumQuestionSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    @action(
        methods=["post"], detail=True, permission_classes=[permissions.IsAuthenticated]
    )
    def upvotes(self, request, pk):
        try:
            if not request.user.is_authenticated:
                return response.Response(
                    {"detail": "User not authenticated"}, status=401
                )

            user = request.user
            forum_question_obj = self.get_object()

            if user in forum_question_obj.upvotes.all():
                forum_question_obj.upvotes.remove(user)
            else:
                forum_question_obj.upvotes.add(user)

            upvote, created = Upvote.objects.get_or_create(
                user=user, forum_question=forum_question_obj
            )

            if not created:
                upvote.value = "Downvote" if upvote.value == "Upvote" else "Upvote"

            upvote.save()

            data = {
                "value": upvote.value,
                "upvotes": forum_question_obj.upvotes.count(),
                "upvote_data": UpvoteSerializer(upvote).data,
            }

            return response.Response(data)

        except Exception as e:
            print(e)
            return response.Response({"detail": "An error occurred"}, status=500)

    # @method_decorator(cache_page(60 * 2))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


class ForumAnswerViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["forum_question__title", "description"]
    search_fields = ["forum_question__title", "description"]

    def get_queryset(self):
        return (
            ForumAnswer.objects.filter(
                forum_question_id=self.kwargs.get("forum_question_pk")
            )
            .select_related("forum_question")
            .all()
        )

    def get_serializer_context(self):
        return {
            "user_id": self.request.user.id,
            "forum_question_id": self.kwargs.get("forum_question_pk"),
        }

    def get_serializer_class(self):
        if self.action == "upvote_answers":
            return UpvoteAnswerSerializer
        return ForumAnswerSerializer

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path="upvotes",
        url_name="upvotes",
    )
    def upvote_answers(self, request, forum_question_pk=None, pk=None):
        try:
            if not request.user.is_authenticated:
                return response.Response(
                    {"detail": "User not authenticated"}, status=401
                )

            user = request.user
            forum_answer_obj = self.get_object()

            if user in forum_answer_obj.upvotes.all():
                forum_answer_obj.upvotes.remove(user)
            else:
                forum_answer_obj.upvotes.add(user)

            upvote_answer, created = UpvoteAnswer.objects.get_or_create(
                user=user, forum_answer=forum_answer_obj
            )

            if not created:
                upvote_answer.value = (
                    "Downvote" if upvote_answer.value == "Upvote" else "Upvote"
                )

            upvote_answer.save()

            data = {
                "value": upvote_answer.value,
                "upvotes": forum_answer_obj.upvotes.count(),
                "upvote_data": UpvoteAnswerSerializer(upvote_answer).data,
            }

            return response.Response(data)

        except Exception as e:
            print("Error in the Forum answer views: ", e)
            return response.Response({"detail": "An error occurred"}, status=500)
