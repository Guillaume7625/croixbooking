from app import create_app, db
from app.models import Floor, Room

app = create_app()

with app.app_context():
    def populate_rooms():
        room_names = [
            {'name': 'Chambre de Mamy', 'floor': 1},
            {'name': 'Chambre adulte plus un enfant', 'floor': 1},
            {'name': 'Chambre Oncle Louis', 'floor': 1},
            {'name': 'Chambre du fond à droite', 'floor': 1},
            {'name': 'Chambre du fond à gauche', 'floor': 1},
            {'name': 'Chambre Oncle François', 'floor': 2},
            {'name': 'Chambre avec 2 lits', 'floor': 2},
            {'name': 'Chambre avec un Lit et un Bureau', 'floor': 2}
        ]

        floors = {}
        for room in room_names:
            if room['floor'] not in floors:
                floor = Floor(number=room['floor'])
                db.session.add(floor)
                db.session.commit()
                floors[room['floor']] = floor
            floor = floors[room['floor']]
            new_room = Room(name=room['name'], floor=floor)
            db.session.add(new_room)

        db.session.commit()

    db.create_all()
    populate_rooms()