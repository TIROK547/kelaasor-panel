from ticket.models import Ticket, Message
from django.db.models import Value, CharField

def run(user):
    for ticket in Ticket.objects.filter(user=user):
        last_message = Message.objects.filter(ticket=ticket).order_by('-date_sended').first()

        if last_message:
            if last_message.user.is_staff:
                x = Ticket.objects.filter(id=ticket.id).annotate(
                    status=Value("answered", output_field=CharField())
                )
            else:
                x = Ticket.objects.filter(id=ticket.id).annotate(
                    status=Value("not answered", output_field=CharField())
                )
        else:
            x = Ticket.objects.filter(id=ticket.id).annotate(
                status=Value("no messages", output_field=CharField())
            )

        print(x[0].status)
