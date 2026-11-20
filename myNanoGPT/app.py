import random
import subprocess
import sys

from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

OUT_DIR = "out_movies"
SEPARATOR = "---------------"


def clean_output(raw):
    lines = raw.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.startswith(("Overriding", "number of parameters", "Loading meta", "No meta.pkl")):
            start = i + 1
    text = "\n".join(lines[start:])
    text = text.split(SEPARATOR)[0]
    return text.strip()


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/generate")
def generate():
    seed = random.randint(0, 1_000_000)
    result = subprocess.run(
        [sys.executable, "sample.py", f"--out_dir={OUT_DIR}", f"--seed={seed}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        return jsonify({"error": "Generation failed. Check the terminal for details."}), 500
    return jsonify({"text": clean_output(result.stdout)})


if __name__ == "__main__":
    app.run(debug=True)
