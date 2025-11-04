from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.db import DatabaseError
from .models import RequestLog, BlockedIP

class IPLoggingMiddleware(MiddlewareMixin):
    def get_client_ip(self, request):
        """تحصل على IP المستخدم حتى لو خلف Proxy"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_request(self, request):
        """تتحقق أولاً من إذا كان الـ IP محظور، ثم تسجّل الطلب"""
        ip = self.get_client_ip(request)

        # 🧱 التحقق من الحظر
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # 📝 تسجيل الطلب
        path = request.path
        timestamp = timezone.now()

        try:
            RequestLog.objects.create(
                ip_address=ip,
                path=path,
                timestamp=timestamp
            )
        except DatabaseError:
            pass
