import os
import io
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
MODEL_ID = "runwayml/stable-diffusion-v1-5"  # You can change this to other models
OUTPUT_DIR = "generated_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global variable for the pipeline
pipe = None

# Load the model
def initialize_model():
    global pipe
    if pipe is None:
        pipe = StableDiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )

        # Move to GPU if available
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        print(f"Model loaded: {MODEL_ID}")
# Generate image endpoint
@app.route('/generate', methods=['POST'])
def generate_image():
    global pipe
    # Initialize model if not already loaded
    initialize_model()

    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        negative_prompt = data.get('negative_prompt', None)
        height = data.get('height', 512)
        width = data.get('width', 512)
        num_inference_steps = data.get('steps', 30)
        guidance_scale = data.get('guidance_scale', 7.5)

        # Validate inputs
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # --- Image Generation Section (Wrap in try...except) ---
        try:
            # Generate the image
            image = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                height=height,
                width=width,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale
            ).images[0]

            # Create a safe filename
            safe_prompt = ''.join(c if c.isalnum() else '_' for c in prompt[:20])
            filename = f"{safe_prompt}_{torch.rand(1).item():.3f}.png"
            filepath = os.path.join(OUTPUT_DIR, filename)
            image.save(filepath)

            # Convert to base64 for sending in response
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            return jsonify({
                "success": True,
                "image": img_str,
                "filepath": filepath
            })
        except Exception as e_generate:
            print(f"Error during image generation: {e_generate}")
            return jsonify({"error": f"Image generation failed on the server: {str(e_generate)}"}), 500

    except Exception as e_request:
        print(f"Error processing request: {e_request}")
        return jsonify({"error": f"Error processing request: {str(e_request)}"}), 500
# Get previously generated images
@app.route('/images', methods=['GET'])
def get_images():
    try:
        images = []
        if not os.path.exists(OUTPUT_DIR):
            return jsonify({"images": []})

        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(OUTPUT_DIR, filename)
                with open(filepath, "rb") as img_file:
                    img_str = base64.b64encode(img_file.read()).decode('utf-8')
                    images.append({
                        "filename": filename,
                        "filepath": filepath,
                        "image": img_str
                    })

        return jsonify({"images": images})

    except Exception as e:
        print(f"Error getting images: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "model": MODEL_ID})

if __name__ == "__main__":
    # For development only - use a proper WSGI server in production
    try:
        print(f"Starting Flask server on port 5000")
        print(f"Image output directory: {os.path.abspath(OUTPUT_DIR)}")
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        print(f"Error starting server: {str(e)}")