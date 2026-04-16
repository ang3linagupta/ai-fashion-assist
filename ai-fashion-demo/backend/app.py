# import os
# import base64
# import requests
# from datetime import datetime
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv

# # ----------------------------
# # Load environment variables
# # ----------------------------
# load_dotenv()

# HF_TOKEN = os.getenv("HF_TOKEN")
# PORT = int(os.getenv("PORT", 5000))

# # ----------------------------
# # Flask setup
# # ----------------------------
# app = Flask(__name__)
# CORS(app)

# # Hugging Face Stable Diffusion model
# HF_MODEL_URL = (
#     "https://api-inference.huggingface.co/models/"
#     "stabilityai/stable-diffusion-xl-base-1.0"
# )

# HEADERS = {
#     "Authorization": f"Bearer {HF_TOKEN}"
# }

# # ----------------------------
# # Helper functions
# # ----------------------------
# def build_prompt(color, fabric, outfit, notes):
#     """
#     Builds a clean prompt for fashion model image generation
#     """
#     prompt = f"""
#     A professional fashion model wearing a {color} {fabric} {outfit},
#     {notes},
#     full body view,
#     studio photoshoot,
#     clean plain background,
#     high quality fashion photography,
#     realistic lighting,
#     sharp focus, detailed fabric texture
#     """
#     return " ".join(prompt.split())


# def negative_prompt():
#     return (
#         "blurry, low quality, distorted, deformed, extra limbs, "
#         "bad anatomy, text, watermark, logo"
#     )


# def generate_image_from_hf(prompt):
#     """
#     Calls Hugging Face API and returns raw image bytes
#     """
#     if not HF_TOKEN:
#         raise Exception("HF_TOKEN not found. Check your .env file.")

#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "negative_prompt": negative_prompt(),
#             "num_inference_steps": 30,
#             "guidance_scale": 7.5
#         }
#     }

#     response = requests.post(
#         HF_MODEL_URL,
#         headers=HEADERS,
#         json=payload,
#         timeout=180
#     )

#     # Successful image response
#     if response.status_code == 200 and response.headers.get(
#         "content-type", ""
#     ).startswith("image"):
#         return response.content

#     # Otherwise return error details
#     try:
#         error_info = response.json()
#     except Exception:
#         error_info = response.text

#     raise Exception(f"Hugging Face error: {error_info}")


# def image_to_base64(image_bytes):
#     encoded = base64.b64encode(image_bytes).decode("utf-8")
#     return f"data:image/png;base64,{encoded}"


# # ----------------------------
# # Routes
# # ----------------------------
# @app.route("/health", methods=["GET"])
# def health():
#     return jsonify({
#         "ok": True,
#         "time": datetime.utcnow().isoformat()
#     })


# @app.route("/generate-image", methods=["POST"])
# def generate_image():
#     try:
#         data = request.get_json()

#         color = data.get("color", "Blue")
#         fabric = data.get("fabric", "Cotton")
#         outfit = data.get("outfit", "Kurti")
#         notes = data.get("notes", "minimal elegant design")

#         prompt = build_prompt(color, fabric, outfit, notes)
#         image_bytes = generate_image_from_hf(prompt)
#         image_base64 = image_to_base64(image_bytes)

#         return jsonify({
#             "prompt": prompt,
#             "image": image_base64
#         })

#     except Exception as e:
#         return jsonify({
#             "error": str(e)
#         }), 500


# # ----------------------------
# # Run server
# # ----------------------------
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=PORT, debug=True)

import os
import base64
from io import BytesIO
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
PORT = int(os.getenv("PORT", 5000))

app = Flask(__name__)
CORS(app)

def build_prompt(color, fabric, outfit, notes):
    prompt = f"""
    A professional fashion model wearing a {color} {fabric} {outfit},
    {notes},
    full body view, studio photoshoot, clean plain background,
    high quality fashion photography, realistic lighting,
    sharp focus, detailed fabric texture
    """
    return " ".join(prompt.split())

def pil_to_data_url(pil_img):
    buf = BytesIO()
    pil_img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"

# Use Hugging Face Inference Providers (recommended)
client = InferenceClient(
    provider="auto",          # auto-selects an available provider
    api_key=HF_TOKEN
)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "time": datetime.utcnow().isoformat()})

@app.route("/generate-image", methods=["POST"])
def generate_image():
    try:
        if not HF_TOKEN:
            return jsonify({"error": "HF_TOKEN missing in .env"}), 500

        data = request.get_json(force=True) or {}

        color = data.get("color", "Blue")
        fabric = data.get("fabric", "Cotton")
        outfit = data.get("outfit", "Kurti")
        notes = data.get("notes", "minimal elegant design")

        prompt = build_prompt(color, fabric, outfit, notes)

        # Text-to-image via Inference Providers
        # This model works with providers (example from HF docs is FLUX)
        pil_image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-schnell"
        )

        return jsonify({
            "prompt": prompt,
            "image": pil_to_data_url(pil_image)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=True)
