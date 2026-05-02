from rest_framework.response import Response

def error_response(message, status_code=400):
    return Response({"status": "error", "message": message}, status=status_code)


def validation_error_response(errors, status_code=400):
    return Response({"status": "error", "errors": errors}, status=status_code)


def success_response(data=None, status_code=200):
    return Response({"status": "ok", "data": data}, status=status_code)


def message_response(message, status_code=200):
    return Response({"status": "ok", "message": message}, status=status_code)

