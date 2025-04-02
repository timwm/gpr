from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework.decorators import api_view #, throttle_classes
from .models import Attachment


# @throttle_classes([OncePerDayUserThrottle])
@api_view(['GET'])
def attachment(request, *args, **kwargs):
    a = get_object_or_404(Attachment, **kwargs)

    return FileResponse(a.file.open("rb"), as_attachment=True, filename=a.name)
