from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit

# 10 requests/minute for authenticated users
# 5 requests/minute for anonymous users

@csrf_exempt
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponse("Welcome back, you're authenticated.")
    else:
        return HttpResponse("Login attempt or anonymous access.")
