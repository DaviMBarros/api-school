from rest_framework import serializers
from .models import Course
from contents.serializers import ContentSerializer
from students_courses.serializers import StudentsCoursesSerializer
from accounts.models import Account


class CoursesSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(read_only=True, many=True)
    students_courses = StudentsCoursesSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
            "instructor",
            "contents",
            "students_courses",
        ]


class CoursesSerializerPut(serializers.ModelSerializer):
    students_courses = StudentsCoursesSerializer(many=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "students_courses",
        ]
        extra_kwargs = {"name": {"read_only": True}}

    def update(self, instance, validated_data):
        students = []
        no_students = []
        for student_course in validated_data["students_courses"]:
            student = student_course["student"]
            found_student = Account.objects.filter(email=student["email"]).first()
            if found_student:
                students.append(found_student)
            else:
                no_students.append(student["email"])

        if no_students:
            raise serializers.ValidationError({
                "detail": f"No active accounts was found: {', '.join(no_students)}."
            })

        instance.students.add(*students)

        return instance
