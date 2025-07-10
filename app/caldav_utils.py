from caldav import DAVClient
from ics import Calendar
from app.models import CalendarEvent, db
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sync_with_yandex(user):
    if not user.caldav_username or not user.caldav_password:
        raise ValueError("Yandex credentials not configured")

    with DAVClient(
            url='https://caldav.yandex.ru',
            username=user.caldav_username,
            password=user.caldav_password,
            ssl_verify_cert=False
    ) as client:
        principal = client.principal()
        calendars = principal.calendars()

        if not calendars:
            raise Exception("No calendars found in Yandex account")

        calendar = calendars[0]
        yandex_events = calendar.events()

        # Синхронизация событий
        for yandex_event in yandex_events:
            ical = Calendar(yandex_event.data)
            for event in ical.events:
                existing = CalendarEvent.query.filter_by(yandex_event_id=event.uid).first()
                if not existing:
                    new_event = CalendarEvent(
                        title=event.name,
                        start=event.begin.datetime,
                        end=event.end.datetime,
                        description=event.description,
                        yandex_event_id=event.uid,
                        user_id=user.id
                    )
                    db.session.add(new_event)

        db.session.commit()