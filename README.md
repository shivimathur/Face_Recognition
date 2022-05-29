# Face_Recognition
An ML project to identify missing people using images and videos using face_recognition, open cv and flask.

Description 
There are two main features in this project. 
(i) Recognize through an image : If we upload an image of a person, and that person's information is present in the dataset, the system will give the name of the person as the output. So this helps us to find an unknown person in an image.
(ii) Recognize through a video : On uploading a video and giving a name as an input, this feature will give the output as "Yes" if the person is present in the video and "No" if the person is not present. This is useful when we have cctv videos of public places and we have to find if a particular person who is missing appeared in that video or not. 

Authentication:
There are no sign and login options, rather this project has an authentication page. This is because such applications are mostly used by police and so every police station can be given a unique identification number and a pin corresponding to that. On entering the correct credentials, it will take the user to the next page. 
For now, only three identication numbers and pins corresponding to them have been added in the project, but that can be changed later. 
The three credentials for authentication are as follows:
login_dict={'1':'2312', '2':'3243', '3':'7128'}

How to run the project:
Download the code in your local ide. In the terminal, write "python app.py" (without quotes). A link will be generated. Copy the link on your browser. This will take you to the authentication page. 

