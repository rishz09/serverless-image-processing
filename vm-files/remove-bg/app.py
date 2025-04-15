from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

@app.route('/remove_bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return "No image uploaded", 400

    image = request.files['image']
    input_path = 'input.png' 
    output_path = 'output.png'  

    image.save(input_path)

    img = Image.open(input_path).convert("RGB")

    output = remove(img)

    white_bg = Image.new("RGB", output.size, (255, 255, 255))
    visible_output = Image.alpha_composite(white_bg.convert("RGBA"), output.convert("RGBA"))

    output_array = np.array(visible_output)

    buffer = io.BytesIO()
    Image.fromarray(output_array).save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)