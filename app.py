#We have already an api to use in the route https://pixels-server.pixels.xyz/v1/marketplace/item/
#to use the api we need to make a get request with the name of the item appended to the url followed by the string "?pid=65dcdc7182a923ffd400003a"

from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

#now we will add a new route to our app
#this route will be used to ask for the data about one element from the database
@app.route('/element', methods=['GET'])
def get_element():
    #first we need to get the id of the element from the request
    id = request.args.get('id')
    #now we will use the id to get the data from the database
    #for now we will just return a string with the id
    return "Element with id: " + id

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880)
