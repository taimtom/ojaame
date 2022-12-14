from django.shortcuts import render
from .models import Review

# Create your views here.
# API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ReviewSerializers



#Api Views-------------------------------------------------------------------------------------------------

class ApiReviewList(APIView):
    """
    List all reviews, or create a new review.
    """
    def get(self, request, format=None):
        reviews = Review.objects.all()
        serializer = ReviewSerializers(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReviewSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiReviewDetail(APIView):
    """
    Retrieve, update or delete a Review instance.
    """
    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        review = self.get_object(pk)
        serializer = ReviewSerializers(review)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        review = self.get_object(pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)