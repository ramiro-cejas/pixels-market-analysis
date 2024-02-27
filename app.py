#We have already an api to use in the route https://pixels-server.pixels.xyz/v1/marketplace/item/
#to use the api we need to make a get request with the name of the item appended to the url followed by the string "?pid=65dcdc7182a923ffd400003a"

from flask import Flask, request
import requests
import time

app = Flask(__name__)

#we will use a variable to store the last time we updated the data
last_update = 0

@app.route('/')
def index():
    return "Hello, World!"

#now we will add a new route to our app
#this route will be used to ask for the data about one element from the database
@app.route('/element', methods=['GET'])
def get_element():
    #first we need to get the id of the element from the request
    id = request.args.get('id')
    #if the id exist in the id_list we will return the data from the database
    if id == None:
        return "You need to provide an id"
    #search for the id in the id_list.txt
    #if the id is not in the list we will return an error message
    #if the id is in the list we will return the data from the database
    if id not in open('id_list.txt').read():
        return "The id does not exist in the database"
    
    #if the id exist in the id_list we will check if exist the file with that id
    try:
        #we will try to open the file with the id
        file = open("data/" + id + ".txt", "r")
        #if the file exist and the date is less than 5 minutes we will return the data from the file
        #the date is stored inside the file 
        #if the date is more than 5 minutes we will make a get request to the api and store the data in the file
        #we will return the data from the file
        #the data in the file is a json object, and the date is named "fetched" in the json object
        #we will use the date to check if the data is less than 5 minutes
        if (time.time() - float(file.readline())) < 300:
            return file.read()
        else:
            #if the date is more than 5 minutes we will make a get request to the api
            response = requests.get("https://pixels-server.pixels.xyz/v1/marketplace/item/" + id + "?pid=65dcdc7182a923ffd400003a")
            #we will store the data from the api in the file
            file = open("data/" + id + ".txt", "w")
            file.write(str(time.time()) + "\n" + str(response.json()))
            #we will return the data from the api
            return response.json()
    except:
        response = requests.get("https://pixels-server.pixels.xyz/v1/marketplace/item/" + id + "?pid=65dcdc7182a923ffd400003a")
        #we will store the data from the api in the file
        #first we create the file
        file = open("data/" + id + ".txt", "w")
        file.write(str(time.time()) + "\n" + str(response.json()))
        #we will return the data from the api
        return response.json()

@app.route('/updateAll', methods=['GET'])
def update_all():
    global last_update
    password = request.args.get('password')
    if password != "claveSuperSecreta":
        return "You need to provide a valid password"

    if (time.time() - last_update) < 300:
        return "You need to wait at least 5 minutes to update the data"

    for id in open('id_list.txt').read().splitlines():
        response = requests.get("https://pixels-server.pixels.xyz/v1/marketplace/item/" + id + "?pid=65dcdc7182a923ffd400003a")
        file = open("data/" + id + ".txt", "w")
        file.write(str(time.time()) + "\n" + str(response.json()))

    last_update = time.time()
    
    return "All the data has been updated"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880)
