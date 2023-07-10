from flask import Flask, request, redirect, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import desc
from datetime import datetime
import hashlib
import base64
import string
import re
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shorturl.db"
db = SQLAlchemy(app)

base_url = "http://127.0.0.1:5000/"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    username_bot = db.Column(db.String(50), unique=True)
    chat_id = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(25), nullable=False)
    user_status = db.Column(db.String(50), nullable=False, default="activate")
    active_time = db.Column(db.DateTime, default=datetime.now)
    crush_select =  db.Column(db.String(50))
    idd = db.Column(db.Integer, default=random.randint(100000, 999999))
    idd_r = db.Column(db.Integer, default=random.randint(1000, 9999))
    def __repr__(self):
        return f"User('{self.username}','{self.username_bot}','{self.chat_id}','{self.first_name}','{self.user_status}','{self.crush_select}')"


class MsgSend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rchat_id = db.Column(db.String(50))
    schat_id = db.Column(db.String(50))
    msg = db.Column(db.String)
    command = db.Column(db.String)
    msg_status = db.Column(db.String(50))


    def __repr__(self):
        return f"MsgSend('{self.rchat_id}','{self.schat_id}','{self.msg}','{self.command}','{self.msg_status}')"




@app.route("/msg_link")
def msg_link():
    command = request.args.get('command')
    username = request.args.get("username")
    message_text = request.args.get("message_text")
    chat_id = request.args.get("chat_id")
    first_name = request.args.get("first_name")
    existing_user = User.query.filter_by(chat_id=chat_id).first()    
    if not existing_user:
        new_user = User(username=username, chat_id=chat_id,
                        first_name=first_name)
        db.session.add(new_user)
        db.session.commit()
    user_idd = User.query.filter_by(chat_id=chat_id).first().idd
    existing_command = MsgSend.query.filter_by(schat_id=chat_id).order_by(desc(MsgSend.id)).first()
    if existing_command:
        command_is = existing_command.command
    else : 
        command_is = None
    new_msg = MsgSend(msg=message_text, schat_id=chat_id, command=command)
    db.session.add(new_msg)
    db.session.commit()

    user_statuss = User.query.filter_by(chat_id=chat_id).first().user_status

    user_crush = User.query.filter_by(chat_id=chat_id).first().crush_select
    if user_crush is not None :
        userc_chatid = User.query.filter_by(idd=user_crush).first().chat_id
    else : 
        userc_chatid = None

    result = {
        
        "user_idd": user_idd,
        "command_is":command_is,
        "user_statuss" :user_statuss,
        "userc_chatid":userc_chatid,

 }

    return result

@app.route("/addcrush")
def addcrush():
    command = request.args.get('command')
    username = request.args.get("username")
    message_text = request.args.get("message_text")
    chat_id = request.args.get("chat_id")
    first_name = request.args.get("first_name")
    user_id = User.query.filter_by(chat_id=chat_id).first()    
    match = User.query.filter_by(idd=message_text).first() 

    if match :
        fname = match.first_name
        user_id.crush_select = message_text
        db.session.commit()
        msg_bot = f'انت تتكلم مع {match}'

    else:
        msg_bot = "لايوجد مستخدم بهذا المعرف "
    result={"msg_bot":msg_bot}
    return result



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
