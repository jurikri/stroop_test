# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 11:02:38 2023

@author: PC
"""
#%%
import pyautogui
import serial # pip install pyserial
import time

def ms_blsend(data, port, baudrate):
    ser = serial.Serial(port, baudrate)
    try:
        ser.write(data.encode('ascii'))
        print("Data sent:", data)

        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('ascii')
            print("Received:", response)
    
    except Exception as e:
        print("Error:", e)
    
    finally:
        # 연결 종료
        ser.close()

def find_portnum():
    # 시리얼 포트 설정
    for comnum in range(0, 13):
        print(comnum)
        port = "COM" + str(comnum)  # 포트 번호
        baudrate = 9600  # 보드레이트

        try:
            _ = serial.Serial(port, baudrate)
            # ms_blsend("CS229E", ser)
            return comnum
        except:
            pass
    return None

comnum = find_portnum()

comnum = 6
print('comnum ->', comnum)
port = "COM" + str(comnum)  # 포트 번호
baudrate = 9600  # 보드레이트
ms_blsend("CT110E", port, baudrate)

#%%


# 클릭할 좌표
x, y = 67, 1016
# 클릭하기
pyautogui.click(x, y)

for epoch in range(10): # 5초간 VNS 자극 후, 종료
    print('baseline')
    time.sleep(2)

    print('on')
    ms_blsend("CS229E", port, baudrate)
    time.sleep(10) # duty cycle, 1에서 50%, 2에서 100%으로 수정됨
    
    print('off')
    ms_blsend("CT110E", port, baudrate)
    # time.sleep(2)
    
#%%

import pyautogui
import time

# 1초마다 좌표 출력 함수
def print_mouse_position():
    try:
        while True:
            x, y = pyautogui.position()
            print(f"현재 마우스 위치: X={x}, Y={y}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("종료되었습니다.")

# 코드 실행
if __name__ == "__main__":
    print("마우스 위치를 파악하기 위한 프로그램을 시작합니다. 종료하려면 Ctrl+C를 누르세요.")
    print_mouse_position()


#%%
x, y = 67, 1016
# 클릭하기
pyautogui.click(x, y)

tcnt = 0
for epoch in range(1000): # 5초간 VNS 자극 후, 종료
    time.sleep(1); tcnt += 1
    print('tcnt', tcnt)
    
    if tcnt == 60:
        print('60초 경과, 자극 시작하세요')
        
    elif tcnt == 120:
        print('자극이후 60초 경과, 자극종료 하세요')
        
    elif tcnt == 240:
        print('자극이후 120초 경과, 실험종료 하세요')


























