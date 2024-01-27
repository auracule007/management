from django.db import models
from api.models import Courses, User, ContentUpload

class CourseUserProgress(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Courses, on_delete=models.CASCADE)
  completed_content_upload_lessons = models.ManyToManyField(ContentUpload, blank=True)

  def __str__(self):
    return f'{self.course.name}'
  
  
  def course_progress_percentage(self):
    total_lessons = self.course.contentmanagement_set.count()
    completed_content_count = self.completed_content_upload_lessons.count()
    try:    
      if total_lessons == 0:
          return 0
      else:
          return (completed_content_count / total_lessons) * 100
    except Exception as e:
      print('Error while calculating the percentage: ', e)
