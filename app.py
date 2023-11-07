from flask import Flask, redirect, session, render_template

# Flask app setup
app = Flask(__name__)
app.secret_key

# Blueprints
from auth import auth_bp
app.register_blueprint(auth_bp)
from books import books_bp
app.register_blueprint(books_bp)

# Routes
@app.route('/')
def home():
    if 'user' in session:
        return redirect('/home')
    else:
        return redirect('/login')
    

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
