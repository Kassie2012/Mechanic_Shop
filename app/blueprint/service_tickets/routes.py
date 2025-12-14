from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import tickets_bp
from .schema import ticket_schema, tickets_schema
from app.models import db, ServiceTicket, Customer, Mechanic

#create
@tickets_bp.route('/', methods= ['POST'])
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = ticket_schema.load(request.json)

    db.session.add(new_ticket)
    db.session.commit()

    return ticket_schema.jsonify(new_ticket), 201

#assign mechanic to ticket

@tickets_bp.route('/<int:ticket_id>/assign_mechanic/<int:mechanic_id>', methods=['PUT'])

def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket or not mechanic:
        return jsonify({"error": "Invalid ticket ID or mechanic ID"}), 400

    #avoiding duplicate 

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
    return ticket_schema.jsonify(ticket), 200

#remove mechanic from ticket

@tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket or not mechanic:
        return jsonify({"error": "Invalid ticket ID or mechanic ID"}), 400 

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)

    db.session.commit()
    return ticket_schema.jsonify(ticket), 200

#get all tickets

@tickets_bp.route('/', methods=['GET'])
def get_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()

    return tickets_schema.jsonify(tickets), 200