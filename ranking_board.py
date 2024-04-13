# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 10:59:14 2024

@author: PC
"""

import pandas as pd
import pygame
import sys
import numpy as np
import os
import subprocess
import ranking_board_backend
# import time
# XLS 파일에서 데이터를 읽어오는 함수


# Pygame 창에 랭킹을 그리는 함수
def draw_ranking_board(screen, rankings, base_heigth = None, width=None, height=None):
    
    pygame.font.init()
    font_path = os.path.join(os.getcwd(), 'Gorditas\Gordita Medium.otf')
    font = pygame.font.Font(font_path, 32)
    # font = pygame.font.Font(None, 36)  # 폰트 설정
    colors = [(154, 164, 174), (0, 238, 205)]  # 줄마다 색상 변경을 위한 색상 설정

    for j in range(len(rankings)):
        msid, score = rankings[j][0], rankings[j][1]
        
        color = colors[j % 2]
        
        blank = int(width*0.1)
        blank2 = 50
        gap = int((width-(2*blank))/6)
        
        col1 = font.render("#", True, colors[1])
        col2 = font.render("ID", True, colors[1])
        col3 = font.render("Score", True, colors[1])
        screen.blit(col1, (blank - blank2 + gap*1, 40 + base_heigth))
        screen.blit(col2, (blank - blank2 + gap*2, 40 + base_heigth))
        screen.blit(col3, (blank - blank2 + gap*5, 40 + base_heigth))

        rank_text = font.render(f"{j+1}", True, color)
        id_text = font.render(f"{msid}", True, color)
        score_text = font.render(f"{score}", True, color)
        screen.blit(rank_text, (blank - blank2 + gap*1, 45 * (j+1) + 40 + base_heigth))
        screen.blit(id_text, (blank - blank2 + gap*2, 45 * (j+1) + 40 + base_heigth))
        screen.blit(score_text, (blank - blank2 + gap*5, 45 * (j+1)+ 40 + base_heigth))

# 메인 함수
def main():
    ranking_board_backend.msmain()
    current_path = os.getcwd()
    df = pd.read_excel(os.path.join(current_path, 'ranking', 'ranking_data.xlsx'), index_col=0)
    data = np.array(df)
    mix = np.argsort(np.array(data[:,1], dtype=float))[::-1]
    
    # filename = "ranking_data.xlsx"  # 여기에 xls 파일의 경로를 입력하세요.
    # path = r'C:\mscode\test\stroop_test\ranking' + '\\' 
    # data = pd.read_excel(path + filename)
    rankings = data[mix[:15]]
    
    # data = data.sort_values(by='score', ascending=False).head(20)
    pygame.init()
    width = 1000
    height = 1200
    screen = pygame.display.set_mode((width, height))
    screen.fill((255, 255, 255))
    
    # 이미지 로드
    logo_path = r'C:\\mscode\\test\\stroop_test\\utility' + '\\neurogrin_LOGO.png'  # 이미지 경로
    # if os.path.exists(logo_path):  # 파일이 실제 존재하는지 확인
    logo_image = pygame.image.load(logo_path)
    sr = 0.3
    logo_witdh = int(width * sr)
    ratio = logo_witdh / logo_image.get_width()  # 원본 너비 대비 조정 너비의 비율
    logo_height = int(logo_image.get_height() * ratio)  # 비율에 따라 조정된 높이
    logo_image = pygame.transform.scale(logo_image, (logo_witdh, logo_height))
    top_empty = 120
    screen.blit(logo_image, (int(width * (1-sr)/2), top_empty))  # 조정된 로고를 화면의 최상단에 배치

    pygame.display.set_caption('Ranking Board')
    draw_ranking_board(screen, rankings, base_heigth = logo_height + top_empty, width=width, height=height)

    font = pygame.font.SysFont('malgungothic', 45)  # 폰트 설정
    guide_text = font.render("색깔 맞추고 귀여운 인형을! 지금 도전하세요!", True, (154, 164, 174))
    text_rect = guide_text.get_rect(center=(int(width/2), 60))  # 텍스트의 위치를 화면 중앙으로 설정
    screen.blit(guide_text, text_rect)  # 텍스트를 화면에 그립니다.

    pygame.display.flip()  # 화면 업데이트

    # 이벤트 루프
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()

#%%



# 메인 함수
def main():
    pygame.init()
    width = 1000
    height = 1000
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Ranking Board')
    
    update_time = 0  # 마지막 업데이트 시간을 저장할 변수
    
    while True:
        current_time = pygame.time.get_ticks()  # 현재 시간을 가져옵니다.
        if current_time - update_time > 1000:  # 마지막 업데이트로부터 1초가 지났는지 확인합니다.
            ranking_board_backend.msmain()  # 업데이트 함수를 호출합니다.
            current_path = os.getcwd()
            df = pd.read_excel(os.path.join(current_path, 'ranking', 'ranking_data.xlsx'), index_col=0)
            data = np.array(df)
            mix = np.argsort(np.array(data[:,1], dtype=float))[::-1]
            rankings = data[mix[:20]]
            
            screen.fill((255, 255, 255))
            
            """
            nuerogrin logo
            """
            logo_path = r'C:\\mscode\\test\\stroop_test\\utility' + '\\neurogrin_LOGO.png'  # 이미지 경로
            # if os.path.exists(logo_path):  # 파일이 실제 존재하는지 확인
            logo_image = pygame.image.load(logo_path)
            sr = 0.3
            logo_witdh = int(width * sr)
            ratio = logo_witdh / logo_image.get_width()  # 원본 너비 대비 조정 너비의 비율
            logo_height = int(logo_image.get_height() * ratio)  # 비율에 따라 조정된 높이
            logo_image = pygame.transform.scale(logo_image, (logo_witdh, logo_height))
            top_empty = 120
            screen.blit(logo_image, (int(width * (1-sr)/2), top_empty))  # 조정된 로고를 화면의 최상단에 배치
            
            """
            ranking board 그리기
            """
            draw_ranking_board(screen, rankings, base_heigth = logo_height + top_empty, width=width, height=height)
            
            
            """
            홍보 문구
            """
            pygame.font.init()
            font_path = os.path.join(os.getcwd(), 'NotoSansKR.ttf')
            font = pygame.font.Font(font_path, 45)
            
            
            guide_text = font.render("색깔 맞추고 귀여운 인형을! 지금 도전하세요!", True, (154, 164, 174))
            text_rect = guide_text.get_rect(center=(int(width/2), 60))  # 텍스트의 위치를 화면 중앙으로 설정
            screen.blit(guide_text, text_rect)  # 텍스트를 화면에 그립니다.
            
            pygame.display.flip()  # 화면 업데이트
            update_time = current_time  # 업데이트 시간을 현재 시간으로 갱신합니다.
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
















































