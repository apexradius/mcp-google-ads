import time
from google.ads.googleads.errors import GoogleAdsException

_MAX_RETRIES = 5
_BASE_DELAY = 1.0
_RETRYABLE_CODES = {"RESOURCE_EXHAUSTED", "INTERNAL", "UNAVAILABLE"}


def with_retry(fn, *args, **kwargs):
    delay = _BASE_DELAY
    for attempt in range(_MAX_RETRIES):
        try:
            return fn(*args, **kwargs)
        except GoogleAdsException as e:
            code = e.error.code().name if e.error else "UNKNOWN"
            if code not in _RETRYABLE_CODES or attempt == _MAX_RETRIES - 1:
                raise _clean_error(e) from None
            time.sleep(delay)
            delay = min(delay * 2, 60)
    return None


def _clean_error(e: GoogleAdsException) -> RuntimeError:
    errors = []
    for err in e.failure.errors:
        msg = err.message
        if err.error_code:
            field = [f for f in err.error_code.DESCRIPTOR.fields_by_name if getattr(err.error_code, f, 0)]
            if field:
                msg = f"{field[0]}: {msg}"
        errors.append(msg)
    return RuntimeError("; ".join(errors) if errors else str(e))
