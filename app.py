from flask import Flask, render_template, request, jsonify
import base64
import openai
from dotenv import load_dotenv
import os
from PIL import Image as PILImage
from io import BytesIO

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        prompt = request.json.get('prompt')
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt is required'}), 400

        data = {
            "prompt": prompt,
            "n": 1,
            "model": "dall-e-2",
            "size": "1024x1024",
        }
        response = openai.Image.create(**data)
        generated_image_urls = [variation.url for variation in response.data]
        return jsonify({'success': True, 'data': generated_image_urls})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/generate-edit', methods=['POST'])
def generate_edit():
    try:
        prompt = request.form.get('prompt')
        image_file = request.files['image']
        mask_file = request.files.get('mask')

        if not prompt or not image_file:
            return jsonify({'success': False, 'error': 'Prompt and image are required'}), 400

        image_content = PILImage.open(image_file).convert('RGBA')
        image_io = BytesIO()
        image_content.save(image_io, 'PNG')
        image_io.seek(0)

        mask_io = None
        if mask_file:
            mask_content = PILImage.open(mask_file).convert('RGBA')
            mask_io = BytesIO()
            mask_content.save(mask_io, 'PNG')
            mask_io.seek(0)

        data = {
            "image": image_io,
            "mask": mask_io,
            "prompt": prompt,
            "n": 1,
            "size": "512x512",
        }
        response = openai.Image.create_edit(**data)
        generated_image_edit_urls = [variation.url for variation in response.data]
        return jsonify({'success': True, 'data': generated_image_edit_urls})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/generate-variation', methods=['POST'])
def generate_variation():
    try:
        image_file = request.files['image']
        if not image_file:
            return jsonify({'success': False, 'error': 'Image is required'}), 400

        image_content = PILImage.open(image_file).convert('RGBA')
        image_io = BytesIO()
        image_content.save(image_io, 'PNG')
        image_io.seek(0)

        data = {
            "image": image_io,
            "n": 1,
            "size": "1024x1024",
        }
        response = openai.Image.create_variation(**data)
        generated_image_urls = [variation.url for variation in response.data]
        return jsonify({'success': True, 'data': generated_image_urls})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
