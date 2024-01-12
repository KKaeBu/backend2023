from http import HTTPStatus
from flask import Flask, make_response


app = Flask(__name__)


@app.route("/<greeting>/<name>")
def greet(greeting, name):
    resp = make_response(f"{greeting}, {name}!", HTTPStatus.NOT_FOUND)
    resp.headers["MY_HEADER"] = 1234
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=19140)
