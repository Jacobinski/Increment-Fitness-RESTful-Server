from flask_socketio import *

# Define global SOCKET_IO variable
SOCKET_IO = None


def init(socketio):
    """ Initialize the notification system

    :param socketio: The socketio object for the application.
    :return: None
    """
    global SOCKET_IO

    SOCKET_IO = socketio


def send_data_notification(message):
    """ Send a message to socket listeners

    We require init() is called prior to this function.

    :param message: (str) Message to send to socket listeners
    :return: Nothing
    """
    global SOCKET_IO
    assert SOCKET_IO, "The notification system has not been initialized."

    SOCKET_IO.emit(message)
