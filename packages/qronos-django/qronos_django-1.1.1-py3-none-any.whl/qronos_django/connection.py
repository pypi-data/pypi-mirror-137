from django.core.cache import cache
from django.utils import timezone
from qronos import QRonosClient

from qronos_django.settings import QRONOS_HOST, QRONOS_USER, QRONOS_PASSWORD, QRONOS_TOKEN_CACHE_FRACTION, \
    QRONOS_TOKEN_CACHE_KEY, QRONOS_TIME_ZONE


def get_qronos_client():
    qronos_token = cache.get(QRONOS_TOKEN_CACHE_KEY)
    if qronos_token:
        return QRonosClient(host=QRONOS_HOST, token=qronos_token)
    qronos = QRonosClient(host=QRONOS_HOST)
    token, expiry = qronos.login(QRONOS_USER, QRONOS_PASSWORD)
    expiry = timezone.make_aware(expiry, timezone=timezone.pytz.timezone(QRONOS_TIME_ZONE))
    if QRONOS_TOKEN_CACHE_FRACTION:
        timeout = (expiry - timezone.now()).total_seconds() * QRONOS_TOKEN_CACHE_FRACTION
        cache.set(QRONOS_TOKEN_CACHE_KEY, token, timeout)
    return qronos
