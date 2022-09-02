from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  

app = Flask(__name__)

client = MongoClient('mongodb://stephen:curry@13.124.80.27', 27017)  
db = client.dbclone



@app.route('/')     ## html을 주는 부분
def home():
    return render_template('clone.html')




@app.route('/memos', methods=['GET'])                     # 클라이언트로부터 /memos라는 url에 get방식으로 요청을 받으면     
def read_memos():
    result = list(db.memos.find({}, {'_id': 0}))               # 몽고db에서 _id 값을 제외한 모든 데이터 조회해오기
    return jsonify({'result': 'success', 'memos': result})     # memos라는 키 값으로 데이터(제목,내용) 보내주기





@app.route('/memo/create', methods=['POST'])                   # 클라이언트로부터 /memo/create 라는 url에 post방식으로 메모 생성 요청을 받으면
def post_memo():                                     # 클라이언트로부터 데이터(제목,내용) 받기
    title_receive = request.form['create_title_sent']  
    text_receive = request.form['create_text_sent']  
 
    doc = {'title': title_receive, 
               'text': text_receive}

    db.memos.insert_one(doc)                          # 받은 데이터(제목,내용)을 몽고db에 넣기

    return jsonify({'result': 'success'})





@app.route('/memo/edit', methods=["POST"])
def edit_memo():                                    # 클라이언트로부터 데이터(수정전 제목,내용과 수정후 제목,내용) 받기
    oldTitle = request.form['curr_title_sent']
    oldText = request.form['curr_text_sent']
    newTitle = request.form['edit_title_sent']
    newText = request.form['edit_text_sent']
    
    doc = {'title': oldTitle, 'text': oldText}
    
    db.articles.update_one(doc, {"$set": {"title" : newTitle, "comment" : newText}})       # 몽고db에 수정후 제목,내용으로 데이터 업데이트
    return jsonify({'result' : 'success'})
  




@app.route('/memo/delete', methods=['POST'])
def delete_memo():
    title_receive = request.form['delete_title_sent']
    text_receive = request.form['delete_text_sent']        # 클라이언트로부터 지우고싶은 데이터의 제목 받기
    db.articles.delete_one({'title': title_receive, 'text': text_receive})   # 몽고db에서 일치하는 제목을 찾아 삭제해주기
    return jsonify({'result': 'success'})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
