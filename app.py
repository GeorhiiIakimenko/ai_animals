import base64
import io
from flask import Flask, request, jsonify
from flasgger import Swagger
from PIL import Image
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
import torch

app = Flask(__name__)
swagger = Swagger(app)

# Load the model
model_id = "timbrooks/instruct-pix2pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
pipe.to(DEVICE)
pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)


def process_image(image, prompt):
    # Process the image using the model
    images = pipe(prompt, image=image, num_inference_steps=10, image_guidance_scale=1).images

    # Convert the resulting image to base64
    buffered = io.BytesIO()
    images[0].save(buffered, format="PNG", dpi=(3000, 3000))
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


@app.route('/process_image', methods=['POST'])
def upload_image():
    """
    Process an image with a given prompt.
    ---
    parameters:
      - name: image
        in: formData
        type: file
        required: true
        description: The image file to process.
      - name: prompt
        in: formData
        type: string
        required: true
        description: The prompt for image processing.
    responses:
        200:
            description: Processed image.
    """
    image_file = request.files['image']
    image = Image.open(image_file)
    prompt = request.form['prompt']

    result_image_base64 = process_image(image, prompt)
    return jsonify({'processed_image': result_image_base64})


if __name__ == '__main__':
    app.run(debug=True)
