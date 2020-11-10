from flask import Flask, render_template, request 
import io
import random

# import json to load JSON data to a python dictionary 
import json 
  
# urllib.request to make a request to api 
import urllib.request 
  
  
app = Flask(__name__) 
  
@app.route('/')
def home(): 
    return render_template("index.html")
  
if __name__ == '__main__': 
    app.run(debug = True) 