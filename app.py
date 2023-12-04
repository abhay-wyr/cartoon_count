import os
import cv2
import base64
import cloudinary
from cloudinary.uploader import upload
from ultralytics import YOLO
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path to the project directory
project_dir = "/home/ubuntu/cartoon_count"
weights_path = os.path.join(project_dir, "weights/best.pt")

# Enable CORS for all origins
model = YOLO(weights_path)

# Cloudinary configuration
cloudinary.config(
    cloud_name="dkotav2ow",
    api_key="427621935679874",
    api_secret="gBF6PQfsGPEPzXpAoeLKjo8aFRE"
)

# ... Your existing code ...

# Decodes Base64 String to Image
def decodeString(string):
    # Save path for Image
    savePath = os.path.join(project_dir, "out.jpg")

    # Writing Image to File
    res = open(savePath, "wb")
    res.write(base64.b64decode(string))
    res.close()

    # Returning the path of the saved file
    return savePath

# Uploads image to Cloudinary
def uploadToCloudinary(image_path, public_id):
    cloudinary.uploader.upload(image_path, public_id=public_id)

# Encodes the image into base64 string
def encodeString(result):
    # Save path for Annotated Image
    savePath = os.path.join(project_dir, "input.jpg")

    # Saving Annotated Image
    cv2.imwrite(savePath, result.plot())

    # Encoding Image to Base64 String
    return base64.b64encode(open(savePath, "rb").read()).decode('utf-8')

# Generate results from the Model
def getInference(savePath):
    # Predict with the Model
    results = model(savePath)  # Predict on an Image
    return results

# Return the Class and Class Count from the Results
def getClassCount(results, class_):
    # Define Product Classes and Class Code
    # Class Code based on YOLO Training
    classes = {'carton': 0}

    # Selecting and Extracting Classes from Results
    detections = sv.Detections.from_ultralytics(results[0])
    res_class = detections[detections.class_id == classes[class_]]
    return len(res_class)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/carton_counter', methods=["POST"])
def cartonCounter():
    try:
        # Getting Data from Client Request
        data = request.get_json()
        base64String = data.get('base64')  # String
        class_ = data.get('class_')  # String

        # Getting Image Saved Path from Base64 String
        savePath = decodeString(base64String)
        # Upload the image to Cloudinary
        uploadToCloudinary(savePath, public_id="uploaded_image")
        # Getting Model Results
        results = getInference(savePath)
        # Getting Annotated Image
        resString = encodeString(results[0])
        # Getting Class Counts for specified Class
        classCount = getClassCount(results, class_)

        return jsonify({
            "class_": class_,
            "count": classCount,
            "base64Str": resString
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
