from http import HTTPStatus
from flask import Flask, request, make_response


app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    resp = make_response("잘못된 요청입니다.", HTTPStatus.BAD_REQUEST)

    req = {
        "arg1": request.get_json().get("arg1", "No arg1"),
        "op": request.get_json().get("op", "No op"),
        "arg2": request.get_json().get("arg2", "No arg2"),
    }

    result = None
    if req["arg1"] != "No arg1" and req["arg2"] != "No arg2" and req["op"] != "No op":
        num1 = int(req["arg1"])
        num2 = int(req["arg2"])
        op = req["op"]
        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2

    if result:
        resp = make_response(f"결과는: {result}", HTTPStatus.OK)

    return resp


@app.route("/<num1>/<operator>/<num2>")
def cal(num1, operator, num2):
    resp = make_response("잘못된 요청입니다.", HTTPStatus.BAD_REQUEST)

    result = None
    try:
        if operator == "+":
            result = int(num1) + int(num2)
        elif operator == "-":
            result = int(num1) - int(num2)
        elif operator == "*":
            result = int(num1) * int(num2)

        if result:
            resp = make_response(f"{num1} {operator} {num2} = {result}", HTTPStatus.OK)
    except:
        pass

    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=19140)
