from datetime import datetime
from rest_framework import serializers

from api.models import Instructor, Student
from .models import *
from utils.validators import validate_id
from .emails import *
from rest_framework.validators import UniqueTogetherValidator
from django.utils import timezone
from performance.models import UserQuizPerformance


class QuestionCategorySerializer(serializers.ModelSerializer):
    instructor_id = serializers.IntegerField()

    class Meta:
        model = QuestionCategory
        fields = ("id", "instructor_id", "name")

    def validate_instructor_id(self, value):
        if not Instructor.objects.filter(id=value).exists():
            raise serializers.ValidationError("the given intructor id is not valid")
        return value


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    quiz = serializers.StringRelatedField()
    class Meta:
        ref_name = "Question quiz"
        model = Question
        fields = [
            "id",
            "instructor",
            "course",
            "quiz",
            "title",
            "technique",
            "difficulty",
            "date_created",
            "date_updated",
            "is_active",
        ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "Answer question"
        model = Answer
        fields = "__all__"


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    assignment_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    class Meta:
        model = AssignmentSubmission
        fields = (
            "id",
            "user_id",
            "assignment_id",
            "assignment_submission_doc",
            "submission_context",
            "is_completed",
            "points",
            "date_submitted",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=AssignmentSubmission.objects.all(),
                fields=['user_id', 'assignment_id'],
                message='You already submitted this assignment'
            )
        ]
        read_only_fields = ('is_completed','points')

    def validate_assignment_id(self, value):
        return validate_id(Assignment, value )
    
    def validate_user_id(self, value):
        return validate_id( User, value)
    
    def save(self, **kwargs):
        user_id = self.validated_data['user_id']
        assignment_id = self.validated_data['assignment_id']
        assignment_submission_doc = self.validated_data['assignment_submission_doc']
        submission_context = self.validated_data['submission_context']
        try: 
            assignment_submissions = AssignmentSubmission.objects.create(assignment_id=assignment_id, user_id=user_id,
            assignment_submission_doc=assignment_submission_doc,submission_context=submission_context)
            assignment_submissions.save()
            with transaction.atomic():            
                try:
                    # using the grading criteria
                    # 1. Beyond the due date
                    today_date = datetime.now(timezone.utc)
                    if assignment_submissions.assignment.date_to_be_submitted > today_date:
                        try:
                            user_performance = UserPerformance.objects.get(
                                user_id=assignment_submissions.user.id
                            )
                            if user_performance.progress_percentage <= 39:
                                create_point = (
                                    PointForEachAssignmentSubmission.objects.create(
                                        user_id=assignment_submissions.user.id
                                    )
                                )
                                create_point.assignment_submission_id = assignment_submissions.id
                                create_point.counter += 1
                                create_point.save()
                        except Exception as error:
                            raise serializers.ValidationError(
                                {"error": str(error)}
                            )
                    # 2. within the due date
                    else:
                        try:
                            user_performance = UserPerformance.objects.get(
                                user_id=assignment_submissions.user.id
                            )
                            if 40 <= user_performance.progress_percentage <= 69:
                                create_point = (
                                    PointForEachAssignmentSubmission.objects.create(
                                        user_id=assignment_submissions.user.id
                                    )
                                )
                                create_point.assignment_submission_id = assignment_submissions.id
                                create_point.counter = 10
                                create_point.save()
                                # then create the gems here
                        except Exception as error:
                            raise serializers.ValidationError(
                                {"error": str(error)})
                except Exception as error:
                    raise serializers.ValidationError(
                        {"error": str(error)}
                    )
                

            send_assignment_submissions_email(assignment_id,submission_context)

            return assignment_submissions
        except Exception as e:
            print("Error while sending email to the instructor: ", e)

class UpdateAssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'update_assignment_submission'
        model = AssignmentSubmission
        fields = ('id','is_completed')

    
    def update(self, instance, validated_data):
        instance.is_completed = validated_data["is_completed"]
        send_assignment_submission_completion_email(instance.is_completed)
        return super(UpdateAssignmentSubmissionSerializer, self).update(
            instance, validated_data
        )

class AssignmentSerializer(serializers.ModelSerializer):
    instructor_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    class Meta:
        model = Assignment
        fields = ('id','instructor_id', 'course_id', 'assignment_title', 'assignment_description', 'assignment_doc','date_given','date_to_be_submitted', 'is_ended','date_created' )

    def validate_instructor_id(self, value):
        return validate_id(
            Instructor, value
        )
    
    def validate_course_id(self, value):
        return validate_id(
            Courses, value
        )

    def save(self, **kwargs):
        instructor_id = self.validated_data['instructor_id']
        course_id = self.validated_data['course_id']
        assignment_title = self.validated_data['assignment_title']
        assignment_description = self.validated_data['assignment_description']
        assignment_doc = self.validated_data['assignment_doc']
        date_given = self.validated_data['date_given']
        date_to_be_submitted = self.validated_data['date_to_be_submitted']
        is_ended = self.validated_data['is_ended']
        try:
            assignment = Assignment.objects.create(instructor_id=instructor_id, course_id=course_id, assignment_title=assignment_title, assignment_description=assignment_description, assignment_doc=assignment_doc, date_given=date_given, date_to_be_submitted=date_to_be_submitted, is_ended=is_ended)
            assignment.save()
            send_course_assignment_email(course_id,assignment_title,date_given,date_to_be_submitted)
            return assignment
        except Exception as e:
            print('Error while sending email when the assignment is created: ', e)



class AnswerTheQuestionSerializer(serializers.ModelSerializer):
    instructor_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    class Meta:
        ref_name = 'Answer_the_question'
        model = Answer
        fields = ('id','instructor_id','student_id','question_id','answer_text')

    def validate_question_id(self, value):
        return validate_id(
            Question, value
        )
    
    def validate_student_id(self, value):
        return validate_id(
            Student, value
        )
    
    def validate_instructor_id(self, value):
        return validate_id(
            Instructor, value
        )

class QuizSubmissionSerializer(serializers.ModelSerializer):
    are_answers = AnswerTheQuestionSerializer(many=True, required=False)
    instructor_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    question_id = serializers.IntegerField()

    class Meta:
        model = QuizSubmission
        fields = (
            "id",
            "instructor_id",
            "student_id",
            "question_id",
            "are_answers",
            "points_earned",
            "submitted_date",
        )    
        read_only_fields = ('points_earned',)

    def validate_question_id(self, value):
        return validate_id(
            Question, value
        )
    
    def validate_student_id(self, value):
        return validate_id(
            Student, value
        )
    
    def validate_instructor_id(self, value):
        return validate_id(
            Instructor, value
        )
    
    def save(self, **kwargs):
        user_id = self.validated_data['user_id']
        quiz_id = self.validated_data['quiz_id']
        quiz_submission_doc = self.validated_data['quiz_submission_doc']
        submission_context = self.validated_data['submission_context']
        try: 
            quiz_submission = QuizSubmission.objects.create(quiz_id=quiz_id, user_id=user_id,
            quiz_submission_doc=quiz_submission_doc,submission_context=submission_context)
            quiz_submission.save()
            with transaction.atomic():            
                try:
                    # using the grading criteria
                    # 1. Beyond the due date
                    today_date = datetime.now(timezone.utc)
                    if quiz_submission.submitted_date > today_date:
                        try:
                            user_performance = UserQuizPerformance.objects.get(
                                user_id=quiz_submission.user.id
                            )
                            if user_performance.progress_percentage <= 39:
                                create_point = (
                                    PointForEachQuizSubmission.objects.create(
                                        user_id=quiz_submission.user.id
                                    )
                                )
                                create_point.assignment_submission_id = quiz_submission.id
                                create_point.counter += 1
                                create_point.save()
                        except Exception as error:
                            raise serializers.ValidationError(
                                {"error": str(error)}
                            )
                    # 2. within the due date
                    else:
                        try:
                            user_performance = UserQuizPerformance.objects.get(
                                user_id=quiz_submission.user.id
                            )
                            if 40 <= user_performance.progress_percentage <= 69:
                                create_point = (
                                    PointForEachQuizSubmission.objects.create(
                                        user_id=quiz_submission.user.id
                                    )
                                )
                                create_point.assignment_submission_id = quiz_submission.id
                                create_point.counter = 10
                                create_point.save()
                                # then create the gems here
                        except Exception as error:
                            raise serializers.ValidationError(
                                {"error": str(error)})
                except Exception as error:
                    raise serializers.ValidationError(
                        {"error": str(error)}
                    )
                

            # send_quiz_submission_email(assignment_id,submission_context)

            return quiz_submission
        except Exception as e:
            print("Error while sending email to the instructor: ", e)


class AwardForAssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardForAssignmentSubmission
        fields = "__all__"


class AwardForQuizSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardForQuizSubmission
        fields = "__all__"
