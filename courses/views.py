from rest_framework.generics import ( 
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView
)
from .models import Course
from .serializers import CoursesSerializer, CoursesSerializerPut
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAccountPermission
from contents.serializers import ContentSerializer
from contents.models import Content
from rest_framework import permissions
from rest_framework.exceptions import NotFound
from .permissions import ContentPermissions


class CourseView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountPermission]

    queryset = Course.objects.all()
    serializer_class = CoursesSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Course.objects.all()
        return Course.objects.filter(students=self.request.user)


class RetrieveUpdateDeleteCourseView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountPermission]

    queryset = Course.objects.all()
    serializer_class = CoursesSerializer
    lookup_url_kwarg = "course_id"


class RetrieveUpdateAPIViewStudentAddToCourse(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountPermission]

    queryset = Course.objects.all()
    serializer_class = CoursesSerializerPut
    lookup_url_kwarg = "course_id"


class CreateViewContents(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountPermission]

    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_url_kwarg = "course_id"

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs[self.lookup_url_kwarg])


class RetrieveUpdateAPIViewContent(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountPermission, ContentPermissions]

    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_url_kwarg = "content_id"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Content.objects.all()
        return Content.objects.filter(course__contents=self.kwargs[self.lookup_url_kwarg])

    def get_object(self):
        if permissions.SAFE_METHODS:
            object_course = Course.objects.filter(pk=self.kwargs["course_id"])
            object_content = Content.objects.filter(pk=self.kwargs["content_id"])
            if not object_course:
                raise NotFound({"detail": "course not found."})
            if not object_content:
                raise NotFound({"detail": "content not found."})
        return super().get_object()
