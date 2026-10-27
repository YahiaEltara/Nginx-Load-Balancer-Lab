import os
import socket
import time

from flask import Flask, jsonify, request

app = Flask(__name__)

INSTANCE_ID = os.getenv(
    "INSTANCE_ID",
    socket.gethostname(),
)


@app.get("/")
def home():
    return jsonify({
        "message": "Load Balancing Lab",
        "instance": INSTANCE_ID,
    })


@app.get("/api/whoami")
def whoami():
    return jsonify({
        "instance": INSTANCE_ID,
        "hostname": socket.gethostname(),
        "message": "Request processed successfully",
    })


@app.get("/health/live")
def liveness():
    return jsonify({
        "status": "alive",
        "instance": INSTANCE_ID,
    }), 200


@app.get("/health/ready")
def readiness():
    return jsonify({
        "status": "ready",
        "instance": INSTANCE_ID,
    }), 200


@app.get("/api/work")
def do_work():
    try:
        seconds = float(request.args.get("seconds", 1))
    except ValueError:
        return jsonify({"error": "seconds must be a number"}), 400

    if not 0 <= seconds <= 10:
        return jsonify({
            "error": "seconds must be between 0 and 10"
        }), 400

    time.sleep(seconds)

    return jsonify({
        "instance": INSTANCE_ID,
        "duration_seconds": seconds,
        "message": "Work completed",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)