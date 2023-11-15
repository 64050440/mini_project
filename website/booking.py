from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify,session
from . import db
from flask_login import login_required, current_user
import json
from datetime import datetime, timedelta
import locale
from sqlalchemy import and_,or_,func
from .models import User, Classroom, User, Booking
from flask import redirect, url_for
from flask import session

booking = Blueprint('booking', __name__)



@booking.route('/Table', methods=['GET', 'POST'])
@login_required
def room_page():
    all_bookings = Booking.query.all()
    room_number = request.args.get('room')
    
    if 'monday' not in session or 'friday' not in session:
        session['monday'] = datetime.now() - timedelta(days=datetime.now().weekday())
        session['friday'] = session['monday'] + timedelta(days=4)
    monday = session.get('monday')
    friday = monday+ timedelta(days=4)
    
    print(monday.strftime("%d/%m/%Y"))
    print(friday.strftime("%d/%m/%Y"))

    # Include updated monday and friday in the template rendering
    return render_template('Tablemain.html', bookings=all_bookings, room=room_number, user=current_user, monday=monday, friday=friday)








@booking.route('/booking', methods=['GET', 'POST'])
@login_required
def Booking_Page():
    room_value = request.args.get('room')
    all_bookings = Booking.query.all()
    if request.method == 'POST':
        start_time = request.form.get('startSelect')    
        end_time = request.form.get('endSelect')
        date_str = request.form.get('datePicker')
        weeks = int(request.form.get('weeks'))
        start_time = int(float(start_time))
        end_time = int(float(end_time))
        

        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d')
        day = date.weekday()
        weeks=weeks-1
        
        # Calculate the end date by adding weeks*7 days to the selected date
        
        if day in range(0, 5):

            classroom = Classroom.query.filter_by(room_number=room_value).first()
            if classroom:
                enddate = date + timedelta(days=weeks*7)
                
                existing_booking = Booking.query.filter(
                and_(
                    Booking.user_id == current_user.id,
                    Booking.classroom_id == classroom.id,
                    func.strftime('%w', Booking.start_date) == str(day),  # Same day of the week
                    or_(
                        and_(Booking.start_date <= date, Booking.end_date >= date),
                        and_(Booking.start_date <= enddate, Booking.end_date >= enddate),
                        and_(Booking.start_date >= date, Booking.end_date <= enddate),
                    ),
                    or_(
                        and_(Booking.end_time >= start_time, Booking.start_time <= end_time),
                        and_(Booking.start_time <= start_time, Booking.end_time >= end_time),
                    ),
                ),
            ).first()
                if existing_booking:
                    flash('Booking conflict! Another booking exists at the same time.', category='error')
                else:
                    new_booking = Booking(
                        start_time=start_time,
                        end_time=end_time,
                        start_date=date,
                        end_date=enddate,
                        user_id=current_user.id,
                        classroom_id=classroom.id
                    )

                    # add booking to the database
                    db.session.add(new_booking)
                    db.session.commit()

                    flash('Booking Successful!', category='success')
                # redirect to home in views.py
                return redirect(url_for('booking.Booking_Page', user=current_user, room=room_value, bookings=all_bookings))
            else:
                flash("Please select a weekday (Mon-Fri).", category="error")
        else:
            flash("No classroom found"+room_value, category="error")

    return render_template("booking.html", user=current_user, room=room_value, bookings=all_bookings)


@booking.route('/add_classroom', methods=['GET', 'POST'])
@login_required
def add_classroom():
    classrooms = Classroom.query.all()
    if request.method == 'POST':

        room_number = request.form['classroom']

        # Check if the room_number already exists
        existing_classroom = Classroom.query.filter_by(
            room_number=room_number).first()
        if existing_classroom:
            flash('Classroom with this Name already exists.', category='error')
        else:

            new_classroom = Classroom(room_number=room_number)
            db.session.add(new_classroom)
            db.session.commit()
            flash('Classroom added', category='success')
            return redirect(url_for('booking.add_classroom'))


    return render_template('add_classroom.html', user=current_user, classrooms=classrooms)

@booking.route('/History')
@login_required
def History():
    return render_template('History.html', user=current_user)

@booking.route('/delete-classroom', methods=['POST'])
def delete_classroom():

    # this function expects a JSON from the INDEX.js file
    data = json.loads(request.data)  # take data(string)
    classroom_id = data['classroomId']
    classroom = Classroom.query.get(classroom_id)
    if classroom:
        db.session.delete(classroom)
        db.session.commit()

    return jsonify({})

@booking.route('/delete-booking', methods=['POST'])
def delete_booking():

    # this function expects a JSON from the INDEX.js file
    data = json.loads(request.data)  # take data(string)
    booking_id = data['bookingId']
    booking = Booking.query.get(booking_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()

    return jsonify({})


@booking.route('/increase_monday', methods=['POST'])
def increase_monday():
    # Retrieve the current Monday from the session
    current_monday = session.get('monday')

    # Increase Monday by 7 days
    new_monday = current_monday + timedelta(days=7)

    # Update the session with the new Monday value
    session['monday'] = new_monday

    return redirect(url_for('booking.room_page'))



@booking.route('/decrease_monday', methods=['POST'])
def decrease_monday():
    # Retrieve the current Monday from the session
    current_monday = session.get('monday')
    # Increase Monday by 7 days
    new_monday = current_monday + timedelta(days=-7)

    # Update the session with the new Monday value
    session['monday'] = new_monday

    return redirect(url_for('booking.room_page'))
