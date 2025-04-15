from flask import Flask, request, send_file
import tempfile
import os
import io
from sketch import sketchify

app = Flask(__name__)

@app.route('/sketch', methods=['POST'])
def generate_sketch():
    if 'image' not in request.files:
        return "No image uploaded", 400

    input_temp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    output_temp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)

    try:
        request.files['image'].save(input_temp.name)

        sketchify(input_temp.name, output_temp.name)

        with open(output_temp.name, 'rb') as f:
            img_bytes = io.BytesIO(f.read())
        img_bytes.seek(0)

        return send_file(
            img_bytes,
            mimetype='image/jpeg',
            as_attachment=True,
            download_name='result.jpg'
        )
    finally:
        input_temp.close()
        output_temp.close()
        try:
            os.remove(input_temp.name)
            os.remove(output_temp.name)
        except OSError:
            pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
