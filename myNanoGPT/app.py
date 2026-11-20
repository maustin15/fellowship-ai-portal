import os
import pickle
import random

import torch
from flask import Flask, jsonify, send_from_directory

from model import GPT, GPTConfig

app = Flask(__name__)

OUT_DIR = "out_movies"
META_PATH = os.path.join("data", "movies", "meta.pkl")
MAX_NEW_TOKENS = 500
TEMPERATURE = 0.8
TOP_K = 200

checkpoint = torch.load(os.path.join(OUT_DIR, "ckpt.pt"), map_location="cpu")
model = GPT(GPTConfig(**checkpoint["model_args"]))
state_dict = checkpoint["model"]
prefix = "_orig_mod."
for key in list(state_dict.keys()):
    if key.startswith(prefix):
        state_dict[key[len(prefix):]] = state_dict.pop(key)
model.load_state_dict(state_dict)
model.eval()

with open(META_PATH, "rb") as f:
    meta = pickle.load(f)
stoi, itos = meta["stoi"], meta["itos"]


def encode(text):
    return [stoi[c] for c in text]


def decode(ids):
    return "".join(itos[i] for i in ids)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/generate")
def generate():
    try:
        torch.manual_seed(random.randint(0, 1_000_000))
        start = torch.tensor([encode("\n")], dtype=torch.long)
        with torch.no_grad():
            output = model.generate(start, MAX_NEW_TOKENS, temperature=TEMPERATURE, top_k=TOP_K)
        return jsonify({"text": decode(output[0].tolist()).strip()})
    except Exception as error:
        print(error)
        return jsonify({"error": "Generation failed. Check the terminal for details."}), 500


if __name__ == "__main__":
    app.run()