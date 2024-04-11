# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 10:04:49 2023

@author: msbak
"""

import serial

# COM 포트 설정
ser = serial.Serial('COM5', 19200)  # COM1 포트를 9600 baudrate로 연다.
raw_data = ser.readline()
print(raw_data)

while True:
    data = ser.readline()
    # 데이터 읽기
    print(data)

import pickle

# raw_data 저장
with open('raw_data.pkl', 'wb') as f:
    pickle.dump(raw_data, f)


#%%

import serial

# 시도할 baudrate 리스트
baudrates = [9600, 115200, 57600, 38400, 19200, 4800]

for br in baudrates:
    try:
        ser = serial.Serial('COM5', br, timeout=1)
        data = ser.readline()
        # 데이터 출력
        print(f"Baudrate {br}: {data}")
    except Exception as e:
        print(f"Error with baudrate {br}: {e}")
    finally:
        ser.close()
