from flask import Flask, jsonify, request, abort
from flask import render_template, redirect
import json
import io
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models

app = Flask(__name__)
@app.route('/', methods=[ 'POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return redirect(request.url)
        img_bytes = file.read()
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        class_name = format_class_name(class_name)
        return render_template('result.html', class_id=class_id, class_name=class_name)
    return render_template('index.html')

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
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

def format_class_name(class_name):
    class_name = class_name.replace('_', ' ')
    class_name = class_name.title()
    return class_name


def get_prediction(image_bytes):
    try:
        tensor = transform_image(image_bytes=image_bytes)
        model = get_model()
        outputs = model.forward(tensor)
    except Exception:
        return 0, 'Не удалось распознать картинку :('
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    imagenet_class_index = json.load(open('imagenet_class_index.json'))
    return imagenet_class_index[predicted_idx]


if __name__ == '__main__':
    app.run(port=5555, debug=True)
