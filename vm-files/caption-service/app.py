from flask import Flask, request, jsonify
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import io
import threading

app = Flask(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
blip_model.eval()

model_lock = threading.Lock()

@app.route('/caption', methods=['POST'])
def generate_caption():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image = Image.open(file.stream).convert("RGB")

    inputs = blip_processor(images=image, return_tensors="pt").to(device)

    with model_lock:
        out = blip_model.generate(**inputs)
    caption = blip_processor.decode(out[0], skip_special_tokens=True)

    return jsonify({"caption": caption})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, threaded=True)
