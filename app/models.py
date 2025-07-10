from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from .extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # CalDAV интеграция
    caldav_username = db.Column(db.String(120))
    caldav_password = db.Column(db.String(200))
    last_sync = db.Column(db.DateTime)

    # Связи
    events = db.relationship('CalendarEvent', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('Пароль не доступен для чтения')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#3a87ad')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    yandex_event_id = db.Column(db.String(100))