import os
import cv2
import base64
import supervision as sv
from ultralytics import YOLO
from flask import Flask, request, jsonify
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app, resources={r"*": {"origins": "*", "methods": ["OPTIONS", "GET", "POST"]}})

  # Enable CORS for all origins
modelWtsPath = r"C:\\Users\\aksha\\Downloads\\carton_counter\\weights\\best.pt"
model = YOLO(modelWtsPath)

# ... Your existing code ...

#Decodes Base64 String to Image
def decodeString(string):
  #Savepath for Image
  savePath = "out.jpg"
  
  #Writing Image to File
  res = open(savePath, "wb")
  res.write(base64.b64decode((string)))
  res.close()
  
  #Returning the path of the saved file
  return savePath

#Encodes the image into base64 string 
def encodeString(result):
  #Savepath for Annonated Image
  savePath = "input.jpg"
  #Saving Annonated Image
  cv2.imwrite(savePath, result.plot())
  #Encoding Image to Base64 String
  return base64.b64encode(open(savePath,"rb").read()).decode('utf-8')

#Generate results from the Model
def getInference(savePath):
  # Load Custom Trained YOLOv8 Model Weights
  # model = YOLO(modelWtsPath)

  # Predict with the Model
  results = model(savePath)  # Predict on an Image
  return results


#Return the Class and Class Count from the Results
def getClassCount(results, class_):
  #Define Product Classes and Class Code 
  #Class Code based on YOLO Training
  classes = {'carton': 0}

  #Selecting and Extracting Classes from Results
  detections = sv.Detections.from_ultralytics(results[0])
  res_class = detections[detections.class_id == classes[class_]]
  return len(res_class)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/carton_counter', methods=["POST"])
def cartonCounter():
  #Path to Model Weights
  # modelWtsPath = "/home/ashish/Desktop/API_Carton_Counter/weights/best.pt"
  # modelWtsPath = r"E:\\Projects\\carton_counter\\weights\\best.pt"
  
  try:
    #Getting Data from Client Request
    data = request.get_json()
    base64String = data.get('base64') #String 
    class_ = data.get('class_') #String

    #Getting Image Saved Path from Base64 String
    savePath = decodeString(base64String)
    #Getting Model Results
    results = getInference(savePath)
    #Getting Annonated Image
    resString = encodeString(results[0])
    #Getting Class Counts for specified Class
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
  
if __name__ =='__main__':
  app.run(debug=True)