# pip install -qr https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
# 참고 사이트 1 : https://github.com/ultralytics/yolov5/issues/36
# 참고 사이트 2 : https://foss4g.tistory.com/1646


import os
import pandas
import torch
from flask import Flask, render_template, request, redirect

import sqlite3

app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def predict():
    # Model(YOLOv5 종속 항목 설치)
    model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'best.pt', force_reload =True)
    # Image
    img = ['C:\\Users\\admin\\Desktop\\최종 프로젝트\\글,그림\\벤치.png']
    ########## 이 사진을 어떻게 가지고 올지에 대해서 알아봐야한다. !!

    # 추론
    results = model(img)


    # 결과
    #results.print()
    #results.show()
    #results.save() # Save image to 'runs\detect\exp'
    #results.xyxy[0]  # 예측 (tensor)
    # results.pandas().xyxy[0]  # 예측 (pandas)
    conf = results.pandas().xyxy[0]
   
    # 오답 여부
    OX = []
    if str(conf.name) == '토끼':
        OX.append('정답')
    else : OX.append('오답')
    print(OX)
    

    # DB 생성 / 이미 있으면 나중에 주석처리하기.
    # isolation_level = None (auto commit)
    conn = sqlite3.connect('ijm.db', isolation_level=None)
    # 커서
    cursor = conn.cursor()
    # 테이블 생성(데이터 타입 = TEST, NUMERIC, INTEGER, REAL, BLOB(image) 등)
    # 필드명(ex. name) -> 데이터 타입(ex. text) 순서로 입력 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS text_write (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        game text,
        point float,
        OX text)""")

    # db 에 정보 저장
    game = '글->그림'
    point = float(conf.confidence)
    OX = OX[0]

    cursor.execute("""
        INSERT INTO text_write (game, point, OX) VALUES (?,?,?)          
        """, (game, point, OX)
        )

    conn.commit()
    cursor.close()
    conn.close()    

    
    render_template('index.html')
    
if __name__ == "__main__":
        app.run(host="0.0.0.0")  # debug=True causes Restarting with stat