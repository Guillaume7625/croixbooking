from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from . import db
from .models import Floor, Room, Booking
import openai

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return redirect(url_for('main.access'))

@bp.route('/access', methods=['GET', 'POST'])
def access():
    if 'authenticated' not in session:
        session['authenticated'] = False
    if 'attempts' not in session:
        session['attempts'] = 0

    if request.method == 'POST':
        access_code = request.form['access_code']
        if session['attempts'] >= 3:
            error = "Trop de tentatives. Veuillez réessayer plus tard."
        elif access_code == '1812A':
            session['authenticated'] = True
            session['attempts'] = 0
            return redirect(url_for('main.calendar'))
        else:
            session['attempts'] += 1
            error = "Code incorrect"
            return render_template('access.html', error=error)
    return render_template('access.html')

@bp.route('/calendar')
def calendar():
    if not session.get('authenticated'):
        return redirect(url_for('main.access'))
    floors = Floor.query.all()
    current_date = datetime.now()
    return render_template('calendar.html', floors=floors, current_date=current_date)

@bp.route('/api/reservations')
def get_reservations():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    reservations = Booking.query.filter(Booking.date >= start_date, Booking.date <= end_date).all()
    return jsonify([{
        'room_name': r.room_name,
        'date': r.date,
        'initials': r.initials
    } for r in reservations])

@bp.route('/api/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    room = Room.query.filter_by(name=data['roomName']).first()
    if room:
        new_booking = Booking(
            room_name=room.name,
            floor=room.floor.number,
            date=data['date'],
            initials=data['initials']
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({"message": "Reservation successful"})
    return jsonify({"message": "Room not found"}), 404

@bp.route('/api/check_reservation', methods=['GET'])
def check_reservation():
    date = request.args.get('date')
    room_name = request.args.get('roomName')
    booking = Booking.query.filter_by(date=date, room_name=room_name).first()
    return jsonify({"isReserved": bool(booking)})

@bp.route('/api/floors', methods=['GET'])
def get_floors():
    floors = Floor.query.all()
    return jsonify([{"id": f.id, "number": f.number} for f in floors])

@bp.route('/api/rooms', methods=['GET'])
def get_rooms():
    floor_id = request.args.get('floor_id')
    if floor_id:
        rooms = Room.query.filter_by(floor_id=floor_id).all()
    else:
        rooms = Room.query.all()
    return jsonify([{"id": r.id, "name": r.name, "floor_id": r.floor_id} for r in rooms])

@bp.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    openai.api_key = current_app.config['OPENAI_API_KEY']
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=data['message'],
        max_tokens=150
    )
    return jsonify({'response': response['choices'][0]['text']})