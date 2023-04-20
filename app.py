#API TO PAGINATE DATABASE
from flask import Flask,request,jsonify
import os
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import datetime
import sqlite3
from functools import wraps
import uuid
from flask_restful import Resource,Api,fields
from flask import Flask, make_response,request,jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_swagger_ui import get_swaggerui_blueprint
from flask import request,Blueprint
from flask_authorize import Authorize
from flask_sqlalchemy import SQLAlchemy
DATABASE_URL='postgresql://dipalok_render_example_user:sL8HJ3qItX11mxj7ClHxhpkRqfNnziHe@dpg-cgvov8gdh87joktf68o0-a.oregon-postgres.render.com/dipalok_render_example'
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=DATABASE_URL
app.config["SECRET_KEY"]='thisissecret'
db=SQLAlchemy(app)
#MAKING CONNECTION WITH SWAGGER
SWAGGER_URL='/swagger'
API_URL='/static/swagger.json'
SWAGGER_BLUEPRINT=get_swaggerui_blueprint(SWAGGER_URL,API_URL,config={
    "app_name":"Employee DATABASE API"

})



app.register_blueprint(SWAGGER_BLUEPRINT,url_prefix=SWAGGER_URL)
#DECLARING THE DATABASE

class Thread(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
                 

#DECORATOR FUNCTION FOR ROUTING THE APPLICATION
@app.route('/thread/<int:num>')
#FUNCTION TO CREATE PAGINATION
def thread(num):
    page = request.args.get('page', num, type=int)
    per_page =20
    data=[]
    threads=Thread.query.paginate(page=page,per_page=per_page,error_out=False)
    t=Thread.query.all()
    maxpage=threads.total//per_page
    if num>maxpage:
        return jsonify({"status":"Success","message":"Page does not exist.list=[]"})
    elif num<0:
        return jsonify("Page number has to start from 1.For all print five 0")
    elif num==0:
        for i in t:
            data.append({"id":i.id,"title":i.title})
        return jsonify({'all_data':data,"message":"Success","status":"OK"}) 
        
    else:
        for i in threads:
            data.append({"id":i.id,"title":i.title})
        return jsonify({'data':data,"message":"Success","status":"OK",
                    "current_page":num,
            "total_data_count":threads.total,
            "next_page":threads.next_num,
            "prev_page":threads.prev_num,
            "has_next":threads.has_next,
            "has_prev":threads.has_prev,
           "total_page":maxpage })
#CREATING THE DATABASE BY SQLALCHEMY AND USING SQLITE3 and then getting all the attributes from the database.
#USING THE PAGINATE FUNCTION TO CREATE THE DATABASE PAGGING.IT TAKES 3 PARAMETERS TO CREATE PAGINATION.1st 1 page which is equal to current page
#Here the request.args takes the initial paage number as 1 and then it uses the parameters per_page to take the data per page.
#©Annonymous
