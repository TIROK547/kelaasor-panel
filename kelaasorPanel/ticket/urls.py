from django.urls import path
from .views import CreateTicketView, CreateMessageView, ListTicketView, TicketMessagesView

urlpatterns = [
    path("new-ticket/", CreateTicketView.as_view()),
    path("new-message/", CreateMessageView.as_view()),
    path("see-tickets/", ListTicketView.as_view()),
    path("see-messages/<int:ticket_id>/", TicketMessagesView.as_view()),
]