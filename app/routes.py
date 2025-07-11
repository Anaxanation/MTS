from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager
from app.models import User, CalendarEvent
from datetime import datetime
from app.caldav_utils import sync_with_yandex

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.calendar'))
        flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Это имя пользователя уже занято', 'danger')
            return redirect(url_for('auth.register'))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        flash('Регистрация успешна! Теперь вы можете войти', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@main_bp.route('/')
@login_required
def index():
    return redirect(url_for('main.calendar'))


@main_bp.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')
    
@main_bp.route('/api/events')
@login_required
def get_events():
    events = CalendarEvent.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'start': event.start.isoformat(),
        'end': event.end.isoformat(),
        'color': event.color,
        'description': event.description
    } for event in events])


@main_bp.route('/api/events', methods=['POST'])
@login_required
def create_event():
    data = request.get_json()
    event = CalendarEvent(
        title=data['title'],
        start=datetime.fromisoformat(data['start']),
        end=datetime.fromisoformat(data['end']),
        description=data.get('description', ''),
        color=data.get('color', '#3a87ad'),
        user_id=current_user.id
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'status': 'success', 'event_id': event.id})


@main_bp.route('/api/sync', methods=['POST'])
@login_required
def sync_events():
    try:
        sync_with_yandex(current_user)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@main_bp.app_errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template('errors/500.html'), 500
