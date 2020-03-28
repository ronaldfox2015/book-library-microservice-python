from flask import Response,json

"""
Custom Response Function
"""
class DtoResponse(Response):
    def __init__(self, res, status_code):

        Response(
            headers='',
            mimetype="application/json",
            response=json.dumps(res),
            status=status_code
        )