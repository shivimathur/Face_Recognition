#imprting all the necessary libraries
import pickle
from urllib import response 
from flask import Flask, jsonify, render_template
from flask import request 
from imutils import paths
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import face_recognition
import os
import cv2 
from PIL import Image

#function to train our model
def model_train():
    image_paths=list(paths.list_images("images")) #path list of all the images
    encodings=[]
    names=[]
    for i, imagepath in enumerate(image_paths):
        name = imagepath.split(os.path.sep)[-2]
        image=cv2.imread(imagepath)
        to_rgb=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        box=face_recognition.face_locations(to_rgb)
        encode=face_recognition.face_encodings(to_rgb, box) #mathematical encodings of the faces
        boxsize1=[]
        boxsize2=[]
        for j,e in enumerate(encode): #if there are multiple faces, consider the largest face
            boxsize1.append((box[j][2]-box[j][0])*(box[j][1]-box[j][3]))
            boxsize2.append((box[j][2]-box[j][0])*(box[j][1]-box[j][3]))
        boxsize1.sort(reverse=True)
        for j,e in enumerate(encode):
            if(boxsize1[0]==boxsize2[j]):
                names.append(name)
                encodings.append(e)
    data={"encodings" : encodings, "names" : names} #dictionary to store the encodings and names 
    print(len(data))
    f = open("face_enc", "wb")
    f.write(pickle.dumps(data)) #write the dictionary in a file
    f.close()
    data = pickle.loads(open('face_enc', "rb").read())
    return data

#function to find if the video contains the person with given name or not
def model_test_video(data, name_input):
    cap=cv2.VideoCapture("test_video.mp4")
    flag=0
    while True:
        _, img = cap.read()
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        box=face_recognition.face_locations(rgb)
        encode=face_recognition.face_encodings(rgb)
        names = []
        for encoding in encode:
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                    name = max(counts, key=counts.get)
                    if(name==name_input): #if the name matches with the input name, return Yes.
                        flag=1
                        return("Yes")
                        break
            if(flag==1):
                break
        if(flag==1):
            break
            print(boxsize1) 
        k = cv2.waitKey(30) & 0xff  
        if k==27:  
            break  

    if(flag==0):
        return ("No") #If the name does not matches with the input name, return No.

#Function to find the name of the person in the picture
def model_test(image, data): 
    box=face_recognition.face_locations(image)
    encode=face_recognition.face_encodings(image)
    names = []
    for encoding in encode:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"
        if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                    name = max(counts, key=counts.get)
        names.append(name)

        boxsize1=[]
        boxsize2=[]
        for j,e in enumerate(encode):
            boxsize1.append((box[j][2]-box[j][0])*(box[j][1]-box[j][3]))
            boxsize2.append((box[j][2]-box[j][0])*(box[j][1]-box[j][3]))
        boxsize1.sort(reverse=True)
        for j,e in enumerate(encode):
            if(boxsize1[0]==boxsize2[j]):
                return names[0]

#list and dictionary containing information about authentication details
unique_number_list=['1','2','3']
login_dict={'1':'2312', '2':'3243', '3':'7128'}

app=Flask(__name__, static_url_path="/static" , static_folder="static" , template_folder="templates")
#route for login
@app.route("/login", methods=["GET","POST"])
def login():
    error=None
    if request.method=="POST":
        unique_number=request.form["unique_number"]
        pin=request.form["pin"]
        if(unique_number in unique_number_list):
            if(login_dict[unique_number] == pin):
                model_train()
                return render_template("index.html")
            else:
                error="Invalid Pin. Please Try Again." 
        else:
            error="Invalid Unique Identification Number. Please Try Again."
    return render_template("login.html", error=error)

#route for logout
@app.route("/index")
def logout():
    return render_template("login.html")

#route for search through picture
@app.route("/search_via_picture", methods=["GET","POST"])
def predict_image():
    if request.method=="POST":
        image_in=request.files["dataset"]
        image = np.asarray(Image.open(image_in))
        data = pickle.loads(open('face_enc', "rb").read())
        name=model_test(image, data)
        response={"Name of the person : " : name}
        return render_template("search_via_picture.html" , person_name=name)
    elif request.method=="GET":
        return render_template("search_via_picture.html" , person_name="No image uploaded")

#route for search through video
@app.route("/search_via_video", methods=["GET","POST"])
def predict_video():
    if request.method=="POST":
        name_in=request.form.get("names")
        video=request.files["video"]
        video.save("test_video.mp4")
        data = pickle.loads(open('face_enc', "rb").read())
        ans=model_test_video(data, name_in)
        response={"Video : " : ans}
        return render_template("search_via_video.html" , answer=ans)
    elif request.method=="GET":
        return render_template("search_via_video.html" , answer="No video uploaded")

#route for authentication page
@app.route("/" , methods=["GET"])
def home():
    return render_template("login.html")

#run the programme
if __name__ == '__main__':
    app.run(port=8000)

