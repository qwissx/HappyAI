from amplitude import BaseEvent

from dependency import amp, executer


def event_handler(event_name, user_id):
    event = BaseEvent(event_name, user_id)

    executer.submit(amp.track(event))
