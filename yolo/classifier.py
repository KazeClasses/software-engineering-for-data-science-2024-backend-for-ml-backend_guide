from flask import Blueprint, request, jsonify, current_app
from ultralytics import YOLO
import ultralytics
import io
from PIL import Image
import ultralytics.engine
import ultralytics.engine.results

classifier_service = Blueprint("classifier", __name__)

model = YOLO("yolo11n-cls.pt")

@classifier_service.route("/classify", methods=["POST"])
def classify():
    file = request.files["image"]
    # Read the file into a bytes object
    img_bytes = file.read()
    # Create a PIL Image object from the bytes
    img = Image.open(io.BytesIO(img_bytes))
    
    # Run inference
    results: list[ultralytics.engine.results.Results]  = model(img)
    
    # Extract relevant information from the results
    formatted_results= []
    for r in results:
        name = r.names
        probs = r.probs  # Get the probabilities
        top_probs = probs.top5  # Get top 5 probabilities
        
        formatted_result = {
            "top_classes": [
                {"name": name[top_probs[i]], "probability": float(probs.top5conf[i])}
                for i in range(5)
            ]
        }
        formatted_results.append(formatted_result)
    
    return jsonify(formatted_results)
