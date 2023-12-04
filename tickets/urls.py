from django.urls import path
from .views import DZTicketAssignView, DzTicketUpdateView,FrTicketUpdateView,FRTicketCreateView,TicketsListUnAssignedView,DzAssistantListView,TicketFinishView,DownloadAttachmentAPIView

urlpatterns = [
    path('', FRTicketCreateView.as_view(), name='ticket-create'),
    path('unassigned', TicketsListUnAssignedView.as_view(), name='ticket-list-unAssigned'),
    path('dz-update/<int:pk>', DzTicketUpdateView.as_view(), name='dz-ticket-update'),
    path('fr-update/<int:pk>', FrTicketUpdateView.as_view(), name='fr-ticket-update'),
    path('finish/<int:pk>', TicketFinishView.as_view(), name='ticket-finish'),    
    path('assign/<int:pk>', DZTicketAssignView.as_view(), name='ticket-assign'),
    path('dz-assistant', DzAssistantListView.as_view(), name='assistant-list'),
    path('download-attachment/<int:ticket_id>', DownloadAttachmentAPIView.as_view(), name='download-attachment'),
]