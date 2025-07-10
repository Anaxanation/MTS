import flask_login_patcher
flask_login_patcher.patch_flask_login()

from app import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)