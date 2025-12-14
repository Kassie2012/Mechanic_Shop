from app.extensions import ma
from app.models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True
        load_instance = True

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)