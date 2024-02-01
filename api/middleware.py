from django.urls import resolve

from .models import CourseViewCount


class CourseViewCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        view = resolve(request.path_info)
        if view.url_name == "courses":
            course_id = view.kwargs.get("courses_pk")

            try:
                view_count = CourseViewCount.objects.get(course_id=course_id)
                view_count.count += 1
                view_count.save()
            except CourseViewCount.DoesNotExist:
                CourseViewCount.objects.create(course_id=course_id, count=1)

        response = self.get_response(request)
        return response
