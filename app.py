from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello buddy!'


if __name__ == '_main_':
    app.run(debug=True , port=5000)
