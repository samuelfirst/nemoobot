import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .tasks import save_subscription_model
from .utils import is_request_verified, process_event


@csrf_exempt
def follows_webhook(request, twitch_user_id):
    if is_request_verified(request):
        data = json.loads(request.body.decode('utf-8'))
        token = data.get('challenge')
        if token:
            subscription_data = data.get('subscription')
            save_subscription_model.apply_async((subscription_data, twitch_user_id))
            return HttpResponse(token, content_type="text/plain", status=200)
        process_event(data.get('event'), 'new_follow')
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)
