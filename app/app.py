from flask import Flask, render_template, jsonify, session
# from flask.ext.session.__init__ import Session
from flask_bootstrap import Bootstrap
from flask import request
#import redis
import facebook
#import requests
#import json
#import MySQLdb
#import mysql.connector




app = Flask(__name__)
SESSION_TYPE = 'redis'
Bootstrap(app)
app.config.from_object(__name__)
app.secret_key = "Sparrow Maketting Secret Key"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/handle_data_fb', methods=['POST'])
def handle_data_fb():
    Page_ID = request.form['Page_ID']
    Access_Token = request.form['Access_Token']
    # graph=facebook.GraphAPI(Access_Token, version="3.2")
    session['Access_Token'] = Access_Token
    session['Page_ID'] = Page_ID
    # post = graph.get_object(id=Page_ID, fields='posts')
    return render_template('interface.html')


@app.route('/posts', methods=['POST'])
def posts():
    # data=jsonify(post)
    token = session.get('Access_Token', 'not set')
    pid = session.get('Page_ID', 'not set')
    if token is not "not set" and pid is not "not set":
        graph=facebook.GraphAPI(token, version="3.2")
        post = graph.get_object(id=pid, fields='posts')

        post_id=[]
        ids=[]
        for itemx in post["posts"]["data"]:
            if "id" in itemx:
                ids.append(itemx["id"])
                temp = {"id":itemx["id"]}
                if "story" in itemx:
                    temp["story"] = itemx["story"]
                else:
                    temp["story"] = "none"
                if "message" in itemx:
                    temp["message"] = itemx["message"] 
                else:
                    temp["message"] = "none"
                post_id.append(temp)
            else:
                post_id.append('none')
    
    return render_template('posts.html', posts = post_id)

@app.route('/get/')
def get():
    return session.get('Access_Token', 'not set')                    


@app.route('/comments',methods=['POST'])
def comments():
    comment_list=[]
    for i in post_ids:
        comment_list.append(graph.get_object(i, fields='comments{from,message}'))

    return comment_list


@app.route('/details', methods=['POST'])
def details():
    token = session.get('Access_Token', 'not set')
    pid = session.get('Page_ID', 'not set')
    post_ids=session.get('ids', 'not set')
    if token is not "not set" and pid is not "not set":
        graph=facebook.GraphAPI(token, version="3.2")
    
    temp = request.form["details"]
    comments = graph.get_object(temp, fields='comments,reactions,shares')
    comment_list=[]
    if "comments" in comments:
        for itemx in comments["comments"]["data"]:
            temp = {}
            if "id" in itemx["from"]:
                temp["sender_id"] = itemx["from"]["id"]
            else:
                temp["sender_id"] = "none"
            if "name" in itemx["from"]:
                temp["name"] = itemx["from"]["name"]
            else:
                temp["name"] = "none"
            if "id" in itemx:
                temp["comment_id"] = itemx["id"]
            if "message" in itemx:
                temp["comment"] = itemx["message"]
            else:
                temp["comment"] = "none"
            comment_list.append(temp)
    else:
        comment_list.append("none")    
    
    like_list = []
    if "reactions" in comments:
        for itemx in comments["reactions"]["data"]:
            temp = {}
            if "id" in itemx:
                temp["likers_id"] = itemx["id"]
            else: 
                temp["likers_id"]= 'none'
            if "name" in itemx:
                temp["liker_name"] = itemx["name"]
            else:
                temp["liker_name"] = "none"
            if "type" in itemx:
                temp["type"] = itemx["type"]
            else:
                temp["type"] = 'none'
            like_list.append(temp)
    else:
        like_list.append('none')

    final_return_dict = {
       "comment_list":comment_list,
       "like_list":like_list
        }
    if "count" in comments["shares"]:
        final_return_dict["shares"] = comments["shares"]["count"]
    else: 
        final_return_dict["shares"]= 'none'


    return render_template('details.html', final = final_return_dict)




@app.route('/conversations', methods=['POST'])
def conversations():
    token = session.get('Access_Token', 'not set')
    pid = session.get('Page_ID', 'not set')
    if token is not "not set" and pid is not "not set":
        graph=facebook.GraphAPI(token, version="3.2")
    conversations = graph.get_object(id=pid, fields='conversations')
    conversations_list=[]
    for itemx in conversations["conversations"]["data"]:
        temp={}
        if "id" in itemx:
            temp["conversation_id"]= itemx["id"]
        else:
            temp["conversation_id"]='none'
        if "link" in itemx:
            temp["post_link"]=itemx["link"]
        else:
            temp["post_link"]='none'
        if "updated_time" in itemx:
            temp["last_updated"]=itemx["updated_time"]
        else:
            temp["updated_time"]='none'
        conversations_list.append(temp)
    return render_template('conversations.html', conversations=conversations_list)


@app.route('/handle_data_twitter', methods=['POST'])
def handle_data_twitter():
    return render_template('temp.html')

@app.route('/chats', methods=['POST'])
def chats():
    token = session.get('Access_Token', 'not set')
    pid = session.get('Page_ID', 'not set')
    if token is not "not set" and pid is not "not set":
        graph=facebook.GraphAPI(token, version="3.2")
    temp_id = request.form["see_chats"]
    conversations = graph.get_object(temp_id, fields='messages{message,id}')
    message_list=[]
    for itemx in conversations["messages"]["data"]:
        temp={}
        if "id" in itemx:
            temp["message_id"]= itemx["id"]
        else:
            temp["message_id"]='none'
        if "message" in itemx:
            temp["message"]=itemx["message"]
        else:
            temp["message"]='none'
        message_list.append(temp)
    final = {
    "message_list":message_list,
    "conversation_id":temp_id
    }
    print(final)
   
    return render_template('chat.html', messages=final)

@app.route('/reply', methods=['POST'])
def reply():
    reply = request.form['reply']
    conversation_id=request.form['conversation_id']
    token = session.get('Access_Token', 'not set')
    pid = session.get('Page_ID', 'not set')
    if token is not "not set" and pid is not "not set":
        graph=facebook.GraphAPI(token, version="3.2")
    graph.put_object(parent_object=conversation_id, connection_name="messages", message=reply)
    
    return reply


if __name__ == '__main__':
    app.run(debug=True)