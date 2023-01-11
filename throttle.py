from django.core.cache import cache
from rest_framework.settings import api_settings


def get_ident(request):
    """
    Identify the machine making the request by parsing HTTP_X_FORWARDED_FOR
    if present and number of proxies is > 0. If not use all of
    HTTP_X_FORWARDED_FOR if it is available, if not use REMOTE_ADDR.
    """
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    remote_addr = request.META.get("REMOTE_ADDR")
    num_proxies = api_settings.NUM_PROXIES

    if num_proxies is not None:
        if num_proxies == 0 or xff is None:
            return remote_addr
        addrs = xff.split(",")
        client_addr = addrs[-min(num_proxies, len(addrs))]
        return client_addr.strip()

    return "".join(xff.split()) if xff else remote_addr


def login_rate_throttle(request, primary_user_key):
    indent = get_ident(request)
    cache_key = f"login_{primary_user_key}_{indent}"
    cache_value = cache.get(key=cache_key)
    cache_ttl = cache.ttl(key=cache_key)
    timeout = 600

    if cache_value and cache_value >= 5:
        return False

    if cache_value:
        cache.set(key=cache_key, value=cache_value + 1, timeout=cache_ttl)
    else:
        cache.set(key=cache_key, value=1, timeout=timeout)

    return True
