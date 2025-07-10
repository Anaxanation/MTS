from werkzeug.datastructures import MultiDict
from urllib.parse import quote, unquote
import flask_login.utils
import importlib


def url_decode(query_string, charset='utf-8', include_empty=True, errors='replace'):
    """Абсолютно надёжная замена url_decode"""
    result = MultiDict()

    if not query_string:
        return result

    if isinstance(query_string, bytes):
        query_string = query_string.decode(charset, errors)

    # Безопасная обработка каждой пары
    for item in query_string.split('&'):
        parts = item.split('=', 1)  # Разбиваем только по первому '='
        if len(parts) == 1 and include_empty:
            result.add(unquote(parts[0]), '')
        elif len(parts) == 2:
            result.add(unquote(parts[0]), unquote(parts[1]))

    return result


def url_encode(obj, charset='utf-8', sort=False, key=None):
    """Надёжная замена url_encode"""
    from werkzeug.datastructures import iter_multi_items
    items = list(iter_multi_items(obj))
    if sort:
        items = sorted(items, key=key)
    return '&'.join(
        f"{quote(str(k), encoding=charset)}={quote(str(v), encoding=charset)}"
        for k, v in items
    )


def patch_flask_login():
    """Патчим flask_login раз и навсегда"""
    flask_login.utils.url_decode = url_decode
    flask_login.utils.url_encode = url_encode
    importlib.reload(flask_login.utils)