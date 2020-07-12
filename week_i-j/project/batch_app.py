from flask import Flask, jsonify, request, abort
from flask import render_template, redirect
import json
import io
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models
import numpy as np
import torch

app = Flask(__name__)
@app.route('/', methods=[ 'POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        try:
            files = request.files.getlist("file")
            if len(files) == 0:
                return 'Загрузите картинки...'
            img_bytes = []
            for file in files:
                img_bytes.append(file.read())
            res = get_prediction(image_bytes=img_bytes)
            if type(res) != type(list):
                return res
            else: 
                return jsonify({'result': res})
        except Exception:
            'Что-то пошло не так...'

def get_model():
    model = models.densenet121(pretrained=True)
    model.eval()
    return model

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    result = torch.zeros([len(image_bytes), 3, 224, 224])
    for i, image in enumerate(image_bytes):
        img = Image.open(io.BytesIO(image))
        result[i] = my_transforms(img)
    return result

def get_prediction(image_bytes):
    try:
        tensor = transform_image(image_bytes=image_bytes)
        model = get_model()
        outputs = model.forward(tensor)
    except Exception:
        return 'Proverte pravilnost vvoda dannih :('
    imagenet_class_index = json.load(open('imagenet_class_index.json'))
    results = []
    for pred in outputs:
        _, y_hat = pred.max(0)
        predicted_idx = str(y_hat.item())
        results.append(imagenet_class_index[predicted_idx])
    return results


if __name__ == '__main__':
    app.run(port=5555, debug=True)
