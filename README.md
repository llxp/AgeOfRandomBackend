# AgeOfRandomBackend
Backend to the AgeOfRandom AOE3 Random card deck generator

## How to use
Download the AOE3 Resource Manager https://github.com/KevinW1998/Resource-Manager to extract the .bar resources needed to run the backend
In the Resource Manager open AoE3DE\Game\Data\Data.bar (AoE3DE is the game directory. can be found in steam) and extract it in the 'data' directory
Make sure, the checkbox "AUTO CONVERT .XMB FILES TO .XML" is checked under EXTRACT -> ALL FILES

start the app using the following command (assuming you have python 3.7+ installed)

    pip install flask flask-cors
    python3 app.py
