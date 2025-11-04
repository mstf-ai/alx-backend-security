# ip_tracking/middleware.py
from .models import RequestLog
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.db import DatabaseError

class IPLoggingMiddleware(MiddlewareMixin):
    def get_client_ip(self, request):
        """تحاول الحصول على IP المستخدم حتى لو خلف Proxy"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_request(self, request):
        """يسجل بيانات الطلب في قاعدة البيانات"""
        ip = self.get_client_ip(request)
        path = request.path
        timestamp = timezone.now()

        try:
            RequestLog.objects.create(
                ip_address=ip,
                path=path,
                timestamp=timestamp
            )
        except DatabaseError:
            # في حال قاعدة البيانات غير جاهزة (أثناء المايجريشن مثلاً)
            pass
