from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from . import db
from .models import Booking
import openai

bp = Blueprint('main', __name__)

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
    return render_template('calendar.html')

@bp.route('/api/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    new_booking = Booking(
        room_name=data['roomName'],
        floor=data['floor'],
        date=data['date'],
        initials=data['initials']
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"message": "Reservation successful"})

@bp.route('/api/check_reservation', methods=['GET'])
def check_reservation():
    date = request.args.get('date')
    room_name = request.args.get('roomName')
    floor = request.args.get('floor')
    booking = Booking.query.filter_by(date=date, room_name=room_name, floor=floor).first()
    return jsonify({"isReserved": bool(booking)})

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
