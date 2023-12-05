from django.urls import path
from .views import (
    CourseView,
    RetrieveUpdateDeleteCourseView,
    RetrieveUpdateAPIViewStudentAddToCourse,
    CreateViewContents,
    RetrieveUpdateAPIViewContent
)

urlpatterns = [
    path("courses/", CourseView.as_view()),
    path("courses/<course_id>/", RetrieveUpdateDeleteCourseView.as_view()),
    path(
        "courses/<course_id>/students/",
        RetrieveUpdateAPIViewStudentAddToCourse.as_view()
    ),
    path(
        "courses/<course_id>/contents/",
        CreateViewContents.as_view()
    ),
    path(
        "courses/<course_id>/contents/<content_id>/",
        RetrieveUpdateAPIViewContent.as_view()
    )
]
