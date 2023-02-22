# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-

# 1. 라이브러리 임포트
from psychopy import visual, event, data, core

# 2. 문자 자극 정의
stim_text = ['빨강', '파랑', '검정', '노랑'] # 화면에 제시할 텍스트
stim_color = ['red', 'blue', 'black', 'yellow'] # 텍스트의 색상

# 자극 리스트 생성
stim_list = []
for idx_text in range(len(stim_text)):
    for idx_color in range(len(stim_color)):
        text = stim_text[idx_text]
        color = stim_color[idx_color]
        # set condition of stimlus
        if idx_text == idx_color:
            cond = 'Cong' # congruent condition
            cresp = 'z' # correct response
        else:
            cond = 'Incong' # incongruent condition
            cresp = 'period' # correct response'
        stim_list.append({'Stim': text, 'Color': color, 'Cond': cond, 'Cresp': cresp})


# 리스트 분리

trials = data.TrialHandler(stim_list, 1, method = 'random') # method = 'random', 'sequential', 'fullRandom' 선택가능

# 3. Window 만들기
win = visual.Window([1000,1000]) # 자극을 제시하는 창의 크기 설정(가로 500, 세로 500); 단위: 픽셀

# 4. 화면에 출력하기

clock = core.Clock()

for trial in trials:
    stim_time = clock.getTime() # 자극 제시 전 시간 기록
    message = visual.TextStim(win,
                              text = trial['Stim'], # win에 출력할 문자열(stim_text) 지정
                              font='Malgun Gothic',
                              color = trial['Color'],
                              bold = True,
                              height = 1)
    message.draw()
    win.flip()
    Response = event.waitKeys() # 5. 키 입력 기다리기
    current_time = clock.getTime() # 반응 버튼 누른 후 시간 기록
    ResponseTime = current_time - stim_time # 반응시간 계산
    if Response[0] == trial['Cresp']:
        acc = 1
    else: acc = 0
    trials.data.add('ResponseTime', ResponseTime) #response time 기록
    trials.data.add('Response', Response[0]) # response 기록
    trials.data.add('Condition', trial['Cond'])
    trials.data.add('Accuracy', acc)
    
# Window 닫기
win.close()
print(trials)

# 결과 저장
trials.saveAsExcel(fileName='stroop_results',sheetName = 'rawData', stimOut=[], dataOut=['all_raw'])