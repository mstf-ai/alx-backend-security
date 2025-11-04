# ip_tracking/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

# paths حساسة نراقبها
SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def detect_suspicious_ips():
    """
    يكتشف IPs اللي عملوا أكثر من 100 request/ساعة
    أو وصلوا للـ paths الحساسة.
    """
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    # 🔹 جميع الـ requests خلال الساعة الأخيرة
    recent_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # 🔹 تعداد requests لكل IP
    ip_counts = {}
    for log in recent_logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

        # 🔹 تحقق من الوصول للـ paths الحساسة
        if log.path in SENSITIVE_PATHS:
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                reason=f"Accessed sensitive path {log.path}"
            )

    # 🔹 تحقق من الـ threshold للطلبات
    for ip, count in ip_counts.items():
        if count > 100:  # threshold: 100 requests/hour
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason=f"{count} requests in the last hour"
            )
