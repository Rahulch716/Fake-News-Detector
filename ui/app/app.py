from flask import Flask, render_template, request, jsonify
import requests
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()
    text = data.get("text", "")
    use_ml = data.get("use_ml", True)
    use_rules = data.get("use_rules", True)
    use_llm = data.get("use_llm", False)

    try:
        response = requests.post(
            f"{API_BASE_URL}/detect",
            json={
                "text": text,
                "use_ml": use_ml,
                "use_rules": use_rules,
                "use_llm": use_llm,
            },
            timeout=30,
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/train", methods=["POST"])
def train():
    data = request.get_json()
    texts = data.get("texts", [])
    labels = data.get("labels", [])
    algorithm = data.get("algorithm", "logistic")

    try:
        response = requests.post(
            f"{API_BASE_URL}/train",
            json={"texts": texts, "labels": labels, "algorithm": algorithm},
            timeout=120,
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/batch-detect", methods=["POST"])
def batch_detect():
    data = request.get_json()
    texts = data.get("texts", [])

    try:
        response = requests.post(
            f"{API_BASE_URL}/batch-detect",
            json={"texts": texts},
            timeout=60,
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/extract-features", methods=["POST"])
def extract_features():
    data = request.get_json()
    text = data.get("text", "")

    try:
        response = requests.post(
            f"{API_BASE_URL}/extract-features",
            json={"text": text},
            timeout=30,
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/model-info")
def model_info():
    try:
        response = requests.get(f"{API_BASE_URL}/model-info", timeout=10)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route("/api-proxy/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def api_proxy(path):
    try:
        url = f"{API_BASE_URL}/{path}"
        if request.method == "GET":
            response = requests.get(url, timeout=30)
        elif request.method == "POST":
            response = requests.post(url, json=request.get_json(), timeout=30)
        elif request.method == "PUT":
            response = requests.put(url, json=request.get_json(), timeout=30)
        elif request.method == "DELETE":
            response = requests.delete(url, timeout=30)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
