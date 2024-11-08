from flask import Blueprint, request, jsonify
from ultralytics import YOLO
import io
from PIL import Image
import ultralytics.engine.results

classifier_service = Blueprint("classifier", __name__)
model = YOLO("yolo11n-cls.pt")

@classifier_service.route("/classify", methods=["POST"])
def classify():
    file = request.files["image"]
    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    results: list[ultralytics.engine.results.Results] = model(img)

    formatted_results = []
    for r in results:
        name = r.names
        probs = r.probs
        top_probs = probs.top5

        formatted_result = {
            "top_classes": [
                {"name": name[top_probs[i]], "probability": float(probs.top5conf[i])}
                for i in range(5)
            ]
        }
        formatted_results.append(formatted_result)

    return jsonify(formatted_results)
