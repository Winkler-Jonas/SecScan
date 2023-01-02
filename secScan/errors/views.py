from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Error
from .serializers import ErrorSerializer


class ErrorList(ListCreateAPIView):
    queryset = Error.objects.all()
    serializer_class = ErrorSerializer


class ErrorDetail(RetrieveUpdateDestroyAPIView):
    queryset = Error.objects.all()
    serializer_class = ErrorSerializer