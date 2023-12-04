from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from .serializers import TicketSerializer
from .permissions import IsFRAssistant,IsDzAssistant
from authentification.models import CustomUser
from authentification.Serializers import CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import os
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.utils import timezone

class FRTicketCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsFRAssistant]

    def perform_create(self, serializer):
        # Set the created_by field to the current user
        serializer.save(created_by=self.request.user)

    def get(self, request, *args, **kwargs):
        # Get the list of Fr Assistant tickets
        if request.user.role=="DZ_ASSISTANT":
            tickets = Ticket.objects.filter(assigned_to=request.user)
        else : 
            tickets = Ticket.objects.filter(created_by=request.user)
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Ensure the request data includes the created_by field
        request_data = request.data.copy()
        request_data["created_by"] = request.user.id  # Assuming created_by is a ForeignKey to User
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TicketsListUnAssignedView(generics.ListAPIView):
    queryset=Ticket.objects.filter(assigned_to=None)
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

class DzAssistantListView(generics.ListAPIView):
    queryset=CustomUser.objects.filter(role="DZ_ASSISTANT")
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsFRAssistant]

class DZTicketAssignView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsDzAssistant]

    def perform_update(self, serializer):
        # Check if the ticket is not already assigned
        if not serializer.instance.assigned_to:
            serializer.save(assigned_to=self.request.user)

class DzTicketUpdateView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsDzAssistant]

    def perform_update(self, serializer):
        ticket = self.get_object()

        # Ensure that the DZ Assistant can only update tickets assigned to them
        if ticket.assigned_to != self.request.user:
            return Response({'error': 'You are not assigned to this ticket.'}, status=status.HTTP_403_FORBIDDEN)

        # Allow DZ assistant to update only notes and attachment
        serializer.save(notes=self.request.data.get('notes', ticket.notes),
                        attachment=self.request.data.get('attachment', ticket.attachment))
        
class FrTicketUpdateView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsFRAssistant]

    def perform_update(self, serializer):
        ticket = self.get_object()

        if ticket.created_by != self.request.user:
            return Response({'error': 'You are not allowed to modify this ticket.'}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(title=self.request.data.get('title', ticket.title),description=self.request.data.get('description', ticket.description),deadline=self.request.data.get('deadline', ticket.deadline))

class TicketFinishView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsDzAssistant]

    def perform_update(self, serializer):
        serializer.save(finished=True,completed_at=timezone.now())  # Assuming you have a completed_at field in your Ticket model

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


    
class DownloadAttachmentAPIView(APIView):
    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)

        if ticket.attachment:
            file_path = os.path.join(settings.MEDIA_ROOT, str(ticket.attachment))
            if os.path.exists(file_path):
                response = FileResponse(open(file_path, 'rb'))
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
            else:
                return Response({"detail": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Ticket does not have an attachment"}, status=status.HTTP_404_NOT_FOUND)