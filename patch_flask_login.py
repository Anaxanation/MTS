from werkzeug.datastructures import MultiDict
from urllib.parse import quote, unquote
import flask_login.utils
import importlib

def url_decode(query_string, charset='utf-8', include_empty=True, errors='replace'):
    """Replacement for werkzeug.urls.url_decode"""
    if isinstance(query_string, bytes):
        query_string = query_string.decode(charset, errors)
    return MultiDict(
        (unquote(k.split('=')[0]), unquote(k.split('=')[1]))
        for k in query_string.split('&') if '=' in k
    )

def url_encode(obj, charset='utf-8', sort=False, key=None):
    """Replacement for werkzeug.urls.url_encode"""
    from werkzeug.datastructures import iter_multi_items
    items = iter_multi_items(obj)
    if sort:
        items = sorted(items, key=key)
    return '&'.join(
        f"{quote(k, encoding=charset)}={quote(v, encoding=charset)}"
        for k, v in items
    )

def patch_flask_login():
    """Patch flask_login.utils with our replacement functions"""
    # Присваиваем функции, а не результат их вызова (убрали скобки)
    flask_login.utils.url_decode = url_decode
    flask_login.utils.url_encode = url_encode
    importlib.reload(flask_login.utils)