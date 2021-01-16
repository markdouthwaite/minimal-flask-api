from flask import Flask, Response

from .errors import errors


app = Flask(__name__)
app.register_blueprint(errors)


@app.route("/")
def index():
    return Response("Hello, world!", status=200)


@app.route("/health")
def health():
    return Response("OK", status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
