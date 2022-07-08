#-*- coding:utf-8 -*-


from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient
app = Flask(__name__)
 
@app.route('/')
def hello():
    return "Hello!"



 
if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0', port=5000) 
    #port번호 : 0 0 0 0 으로 설정해야 외부에서 접근 가능
    #port : 5000번으로 설정


