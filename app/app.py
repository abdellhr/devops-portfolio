"""
Petite API Flask servant de brique applicative pour la démo DevOps.
Expose :
  - GET /            -> message de bienvenue
  - GET /health      -> health check (utilisé par Docker/Ansible/monitoring)
  - GET /metrics     -> métriques au format Prometheus
"""
import time
import random

from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total", "Nombre total de requêtes reçues", ["endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Latence des requêtes", ["endpoint"]
)


@app.route("/")
def index():
    start = time.time()
    # Latence simulée pour rendre les graphes Grafana plus parlants
    time.sleep(random.uniform(0.01, 0.15))
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)
    REQUEST_COUNT.labels(endpoint="/", status="200").inc()
    return jsonify(message="Bienvenue sur l'API de démo DevOps", status="ok")


@app.route("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health", status="200").inc()
    return jsonify(status="healthy"), 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
