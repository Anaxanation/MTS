# MTS

Для запуска требуется перейти в .venv/Lib/site-packages/flask_login/utils.py и заменить from werkzeug.urls import url_decode и from werkzeug.urls import url_encode на from compat import url_decode, url_encode
