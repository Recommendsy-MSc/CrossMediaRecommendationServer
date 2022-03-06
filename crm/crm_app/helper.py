from rest_framework.response import Response

def customResponse(success: bool, data = {}):
    return Response(
        {
            "success": success,
            "data": data,
        }
    )