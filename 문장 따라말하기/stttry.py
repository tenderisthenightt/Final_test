 #-*- coding:utf-8 -*-
import urllib3
import json
import base64
openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
accessKey = "	b4b296d2-da29-42e6-ab19-858685f178f4" #사이트에서 발급받은 키를 이용
audioFilePath = "C:/Users/admin/Desktop/최종 프로젝트/Model/STT/hello.wav" #우리가 넣을 음성파일
languageCode = "korean" #우리가 stt할 언어
   
file = open(audioFilePath, "rb")
audioContents = base64.b64encode(file.read()).decode("utf8")
file.close()
   
requestJson = {    
    "argument": {
        "language_code": languageCode,
        "audio": audioContents
      }
  }
   
http = urllib3.PoolManager()
response = http.request(
      "POST",
      openApiURL,
      headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
      body=json.dumps(requestJson)
  )
   
print("[responseCode] " + str(response.status))
print("[responBody]")
print("===== 결과 확인 ====")
print(str(response.data,"utf-8"))

string = str(response.data,"utf-8")
List = string.split('"')
print(List)

target = List[-2]
target = target[:-1]
print(target)

dic = {'1' : "안녕하세요. 오늘도 멋진 하루 되세요"}

if target == dic['1'] :
    print('정답입니다')
else:
    print('틀렸습니다')