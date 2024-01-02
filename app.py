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

# # Get the list of available models
# models = openai.Model.list()
# for model in models['data']:
#     print(model)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get the prompt from the request data
        prompt = request.json.get('prompt')
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt is required'}), 400

        # Set up the data payload with the API key and the provided prompt
        data = {
            "prompt": prompt,
            "n": 1,
            "model": "dall-e-2",
            "size": "1024x1024",
        }

        # Make the API request to create image variations
        response = openai.Image.create(**data)
        # print(response)

        # Extract the URL of the generated image
        generated_image_urls = [variation.url for variation in response.data]

        return jsonify({'success': True, 'data': generated_image_urls})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/generate-edit', methods=['POST'])
def generate_edit():
    try:
        # Get the uploaded image files
        image_file = request.files['image']
        mask_file = request.files['mask']

        # Read the image content and convert to 'RGBA'
        image_content = PILImage.open(image_file)
        image_content = image_content.convert('RGBA')
        image_io = BytesIO()
        image_content.save(image_io, 'PNG')
        image_io.seek(0)

        # Read the mask content and convert to 'RGBA'
        mask_io = None
        if mask_file:
            mask_content = PILImage.open(mask_file)
            mask_content = mask_content.convert('RGBA')
            mask_io = BytesIO()
            mask_content.save(mask_io, 'PNG')
            mask_io.seek(0)

        # Set up the data payload for the OpenAI API request
        data = {
            "image": image_io,
            "mask": mask_io,
            "prompt": "Put a cute dog face on the mask image.",
            "n": 1,
            # "model": "dall-e-2",
            "size": "512x512",
        }

        # Make the API request to create image edit
        response = openai.Image.create_edit(**data)

        # Extract the URL of the generated image
        generated_image_edit_urls = [variation.url for variation in response.data]

        return jsonify({'success': True, 'data': generated_image_edit_urls})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/generate-variation', methods=['POST'])
def generate_variation():
    try:
        # Get the uploaded image file
        image_file = request.files['image']
        
        image_content = PILImage.open(image_file)
        image_content = image_content.convert('RGBA')
        image_io = BytesIO()
        image_content.save(image_io, 'PNG')
        image_io.seek(0)

        # # Read image file content
        # image_content = image_file.read()

        # # Encode image content as base64
        # encoded_image = base64.b64encode(image_content).decode('utf-8')

        # Set up the data payload with the API key
        data = {
            "image": image_io,
            "n": 1,
            "model": "dall-e-2",
            "size": "1024x1024",
        }

        # Make the API request to create image variations
        response = openai.Image.create_variation(**data)

        # Extract the URL of the generated image
        generated_image_urls = [variation.url for variation in response.data]

        return jsonify({'success': True, 'data': generated_image_urls})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
