from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.db import DatabaseError
from django.core.cache import cache
from .models import RequestLog, BlockedIP
import requests

class IPLoggingMiddleware(MiddlewareMixin):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_geo_info(self, ip):
        """جلب بيانات الموقع الجغرافي من الكاش أو من API"""
        cache_key = f"geo:{ip}"
        data = cache.get(cache_key)

        if data:
            return data  # من الكاش

        try:
            # 🗺️ نستخدم ip-api.com لأنها مجانية ولا تحتاج مفتاح
            url = f"http://ip-api.com/json/{ip}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    country = result.get("country", "")
                    city = result.get("city", "")
                    data = {"country": country, "city": city}
                    cache.set(cache_key, data, 60 * 60 * 24)  # 24 ساعة
                    return data
        except Exception:
            pass

        return {"country": "", "city": ""}

    def process_request(self, request):
        ip = self.get_client_ip(request)

        # 🧱 التحقق من الحظر
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # 🌍 جلب بيانات الجغرافيا
        geo_data = self.get_geo_info(ip)
        country = geo_data.get("country", "")
        city = geo_data.get("city", "")

        # 📝 تسجيل الطلب
        path = request.path
        timestamp = timezone.now()

        try:
            RequestLog.objects.create(
                ip_address=ip,
                path=path,
                timestamp=timestamp,
                country=country,
                city=city
            )
        except DatabaseError:
            pass
