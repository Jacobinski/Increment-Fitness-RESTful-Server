from flask import jsonify


class Response:
    @classmethod
    def success(cls, status, message, data):
        """ Sends a success response

        :param status: HTTP status code
        :param message: Success message.
        :param data: Data sent to the client.
        :return: A JSON object containing the params.
        """
        return jsonify(status=status,
                       message=message,
                       data=data)

    @classmethod
    def client_error(cls, status, message, data):
        """ Sends a client error response

        :param status: HTTP status code
        :param message: Error messages explaining client error.
        :param data: Echo the request that caused the error.
        :return: A JSON object containing the params.
        """
        return jsonify(status=status,
                       message=message,
                       data=data)

    @classmethod
    def server_error(cls, status, message):
        """ Sends a server error response

        :param status: HTTP status code
        :param message: Error message explaining server error.
        :return: A JSON object containing the params.
        """
        return jsonify(status=status,
                       message=message)
