from werkzeug.datastructures import MultiDict
from urllib.parse import unquote


def url_decode(query_string, charset='utf-8', include_empty=True, errors='replace'):
    """Безопасная реализация url_decode"""
    if query_string is None:
        return MultiDict()

    if isinstance(query_string, bytes):
        query_string = query_string.decode(charset, errors)

    result = MultiDict()
    for pair in query_string.split('&'):
        if not pair:
            continue

        parts = pair.split('=', 1)  # Разбиваем только по первому '='
        if len(parts) == 1:
            if include_empty:
                result.add(unquote(parts[0]), '')
        else:
            result.add(unquote(parts[0]), unquote(parts[1]))

    return result


def url_encode(obj, charset='utf-8', sort=False, key=None):
    """Безопасная реализация url_encode"""
    from werkzeug.datastructures import iter_multi_items
    from urllib.parse import quote

    items = list(iter_multi_items(obj))
    if sort:
        items = sorted(items, key=key)

    return '&'.join(
        f"{quote(str(k), encoding=charset)}={quote(str(v), encoding=charset)}"
        for k, v in items
    )