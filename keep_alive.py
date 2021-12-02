from flask import Flask, request, url_for, redirect, render_template
from threading import Thread
import requests

app = Flask('')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/status/success')
def success():
  request=requests.get("http://mcapi.us/server/status?ip=realcraftsurvival.cf&port=43356")
  request2=requests.get('https://mcapi.us/server/status?ip=realcraftlifesteal.cf&port=45030')
  json=request.json()
  json2=request2.json()
  dicti = {"Lifesteal":json2, "Survival":json
    }
  return dicti  

@app.route('/status')
def status():
  return redirect(url_for('success'))


def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()