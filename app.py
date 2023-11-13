from flask import Flask, redirect, session, render_template

# Flask app setup
app = Flask(__name__, static_url_path='/')
app.secret_key = 'secret'

# Blueprints
from auth import auth_bp, login_manager
app.register_blueprint(auth_bp)

login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from books import books_bp
app.register_blueprint(books_bp)

# Routes
@app.route('/')
def home():
    return app.send_static_file('index.html')


def main():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
