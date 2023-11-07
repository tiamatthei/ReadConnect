from flask import Flask
from auth import auth

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

app.register_blueprint(auth)

def main():
    app.run()

if __name__ == '__main__':
    main()
