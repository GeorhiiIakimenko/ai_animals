from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flasgger import Swagger
import torch
from diffusers import StableDiffusionXLPipeline

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app, template_file='swagger.yaml')


# Load Stable Diffusion model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = StableDiffusionXLPipeline.from_pretrained("segmind/SSD-1B").to(device)


class ProcessImage(Resource):
    def post(self):
        """
        Process Image.

        ---
        parameters:
          - name: image
            in: formData
            type: file
            required: true
            description: Pet image
          - name: prompt
            in: formData
            type: string
            required: true
            description: Text prompt
        responses:
          200:
            description: Processed image
        """
        # Get image data and text prompt from request
        image_data = request.files['image'].read()
        prompt = request.form['prompt']

        # Process image using Stable Diffusion model
        with torch.no_grad():
            # Your image processing code here
            processed_image = model(image_data, prompt)

        # Return processed image in JSON format
        return jsonify({'processed_image': processed_image})


api.add_resource(ProcessImage, '/api/main')
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=3000, host="127.0.0.1")
