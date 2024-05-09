from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Thread, Message
from .serializers import ThreadSerializer, ThreadCreateSerializer, MessageSerializer, MessageCreateSerializer
from .pagination import AthletsAPIListPagination
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView


class ThreadViewSet(ViewSet):

    def create(self, request):
        serializer = ThreadCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        participant_id = serializer.validated_data.get('participant_id')

        if participant_id == request.user.id:
            return Response({"error": "participant_id should be another user, not you"}, status=status.HTTP_404_NOT_FOUND)


        # Query for thread with current user and participant_id
        thread = Thread.objects.filter(participants__id=request.user.id).filter(participants__id=participant_id)
        
        # If thread with this participant exists - return it
        if thread:
            thread_serializer = ThreadSerializer(thread.first())
            return Response(thread_serializer.data)
        
        # If thread with this participant does not exists - create a new one 
        else:
            new_thread = Thread.objects.create()
            new_thread.participants.add(request.user.id, participant_id)
            new_thread_serializer = ThreadSerializer(new_thread)
            return Response(new_thread_serializer.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, pk):
        # Query for thread with pk where current user is a participant
        thread = Thread.objects.filter(participants__id=request.user.id, id=pk).first()
        if not thread:
            return Response({"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND)
        thread.delete()
        return Response({"message": "Thread deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        # Query for all current user's threads
        threads = Thread.objects.filter(participants__id=request.user.id)
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)


class MessageCreateAPIView(CreateAPIView):
    pagination_class = AthletsAPIListPagination

    def create(self, request, thread_id):
        thread = Thread.objects.filter(id=thread_id)
        if not thread:
            return Response({"error": "thread does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MessageCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        text = serializer.validated_data.get('text')

        # Create message
        Message.objects.create(text=text, sender=request.user, thread_id=thread_id)
        
        # Query for filter all messages by this thread
        messages = Message.objects.filter(thread_id=thread_id)
        messages_serializer = MessageSerializer(messages, many=True)

        # Add Pagination
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        messages_serializer = MessageSerializer(messages, many=True)
        return Response(messages_serializer.data, status=status.HTTP_201_CREATED)


class MarkMessageAsRead(UpdateAPIView):
    def patch(self, request, thread_id, message_id):
        try:
            # Query for get message
            message = Message.objects.get(id=message_id, thread_id=thread_id)
        except Message.DoesNotExist:
            return Response(
                {"error": "Message does not exist"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        # Update message read status
        message.is_read = True
        message.save()

        serializer = MessageSerializer(message)
        return Response(serializer.data)


class UnreadMessagesCount(APIView):
    def get(self, request):
        unread_count = (
            Message.objects.filter(
                thread__participants=request.user, 
                is_read=False
            )
            .exclude(sender=request.user).count()
        )
        return Response({"unread_count": unread_count}, status=status.HTTP_200_OK)
