import base64
from io import BytesIO
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flasgger import Swagger
import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image
import torchvision.transforms as transforms

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app, template_file='swagger.yml')

# Load Stable Diffusion model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = StableDiffusionXLPipeline.from_pretrained("segmind/SSD-1B").to(device)


def preprocess_image(image_data):
    # Преобразование байтов изображения в объект PIL.Image
    image = Image.open(BytesIO(image_data))

    # Применение необходимых преобразований
    preprocess = transforms.Compose([
        transforms.Resize(256),  # Масштабирование изображения до 256x256
        transforms.CenterCrop(224),  # Обрезка изображения до 224x224 по центру
        transforms.ToTensor(),  # Преобразование изображения в тензор
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Нормализация значений пикселей
    ])

    # Применение преобразований к изображению
    return preprocess(image).unsqueeze(0)  # Добавление размерности пакета

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
        # Получаем данные изображения и текстовый промпт из запроса
        image_data = request.files['image'].read()
        prompt = request.form['prompt']

        # Преобразуем данные изображения в тензор
        image_tensor = preprocess_image(image_data).to(device)

        # Process image using Stable Diffusion model
        with torch.no_grad():
            # Обработка изображения с использованием модели
            processed_image = model(prompt=prompt, image=image_tensor).images[0]

        # Возвращение обработанного изображения в формате base64
        buffered = BytesIO()
        processed_image.save(buffered, format="JPEG")
        processed_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return jsonify({'processed_image': processed_image_base64})


api.add_resource(ProcessImage, '/api/main')

if __name__ == '__main__':
    app.run(debug=True, port=3000, host="127.0.0.1")
