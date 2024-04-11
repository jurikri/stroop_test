# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:53:04 2024

@author: PC
"""

def msmain(arg1):
    #%%
    import subprocess
    import pkg_resources
    
    def install_package(package_name):
        # 패키지가 이미 설치되어 있는지 확인
        installed_packages = {pkg.key for pkg in pkg_resources.working_set}
        if package_name not in installed_packages:
            # 패키지가 설치되어 있지 않을 경우 설치
            subprocess.check_call(["python", "-m", "pip", "install", package_name])
            print(f"{package_name} has been installed.")
        else:
            # 패키지가 이미 설치되어 있음
            print(f"{package_name} is already installed.")
    
    # 패키지 이름 설정
    package_names = ['pygame', 'PyAutoGUI', 'pywin32', 'pygetwindow']
    for package_name in package_names:
        install_package(package_name)
    
    # import pygetwindow as gw
    import pyautogui
    import pygame
    import random
    import time
    # import csv
    from datetime import datetime
    import os
    import pickle

    def create_trial_folder(arg1):
        base_path_template = f"C:/Users/msbak/Desktop/eeg_saves/{arg1}_trial_"
        trial_num = 1
    
        while True:
            trial_path = f"{base_path_template}{trial_num}"
            if not os.path.exists(trial_path):
                os.makedirs(trial_path)
                break
            trial_num += 1
        return trial_path, trial_num

    # # Use the function
    # arg1 = "experiment_name"  # Example argument
    base_path, trial_num = create_trial_folder(arg1)
    print("Base path set to:", base_path)

        
    # Create block directories
    block_paths = []
    for i in range(1, 3):  # 1 to 8
        block_path = os.path.join(base_path, f"block{i}")
        block_paths.append(block_path)
        if not os.path.exists(block_path):
            os.makedirs(block_path)
                   
    ##

    
    # Define colors
    colors = {
        "빨강": (255, 0, 0),
        "초록": (0, 255, 0),
        "파랑": (0, 0, 255),
        "노랑": (255, 255, 0),
        "검정": (0, 0, 0),
        "하양": (255, 255, 255)
    }
   
    W, H = 1920, 1080
    FONT_SZ = int(round(46*(W/800)))

    # def run_predisp():
    #     pygame.event.clear()

    #     # top_word, top_color, bottom_word, is_correct = trial

    #     # Clear screen for new trial
    #     screen.fill(colors["하양"])

    #     # Display the top word in its color
    #     # font = pygame.font.SysFont(None, FONT_SZ)
    #     font = pygame.font.SysFont('malgungothic', FONT_SZ)
    #     top_text = font.render('1111', True, colors["하양"])
    #     top_rect = top_text.get_rect(center=(W/2, int(H/2 - (H*(1/12)))))  # Centered, adjusted for top position
    #     screen.blit(top_text, top_rect)

    #     pygame.display.flip()

    #     # Introduce a time gap before displaying the bottom word
    #     pygame.time.wait(100)  # 100 milliseconds gap as an example
        
    #     # Now display the bottom word (color name) in black
    #     bottom_text = font.render('1111', True, colors["하양"])
    #     bottom_rect = bottom_text.get_rect(center=(W/2, int(H/2 + (H*(1/12)))))  # Centered, adjusted for bottom position
    #     screen.blit(bottom_text, bottom_rect)

    #     pygame.display.flip()

        # Timing and response handling starts after displaying the bottom word
        # start_time = pygame.time.get_ticks()
        # response_made = False
        # response = None
    
    def run_baseline(duration=10 * 1000):  # Default duration set to 30 seconds -> 30으로 추후 수정
        screen.fill(colors["하양"])
        # font = pygame.font.SysFont(None, FONT_SZ)
        # font = pygame.font.SysFont('NanumGothic', FONT_SZ)
        font = pygame.font.SysFont('malgungothic', FONT_SZ)
        text = font.render("+", True, colors["검정"])  # Using "+" as a fixation dot
        rect = text.get_rect(center=(int(W/2), int(H/2)))
        screen.blit(text, rect)
        pygame.display.flip()
        # Wait for the specified duration
        pygame.time.wait(duration)
    
    # Pre-generate stimuli
    def generate_stimuli():
        # words = ["RED", "GREEN", "BLUE", "YELLOW"]
        colors = {"빨강": (255, 0, 0), "초록": (0, 255, 0), "파랑": (0, 0, 255), "노랑": (255, 255, 0)}
        stimuli = {"neutral": [], "congruent": [], "incongruent": []}
        
        # neutral, match
        for color in colors:
            stimuli["neutral"].append(('XXXX', colors[color], color, True))
            
        # neutral, non-match
        for color in colors:
            for color2 in colors:
                if color != color2:
                    stimuli["neutral"].append(('XXXX', colors[color], color2, False))
            
        # congruent, match
        for color in colors:
            stimuli["congruent"].append((color, colors[color], color, True))
            
        # congruent, non-match
        for color in colors:
            for color2 in colors:
                if color != color2:
                    stimuli["congruent"].append((color, colors[color], color2, False))
    
        # incongruent, match
        for color in colors:
            for color2 in colors:
                if color != color2:
                    stimuli["incongruent"].append((color, colors[color2], color2, True))
            
        # incongruent, non-match
        for color in colors:
            for color2 in colors:
                if color != color2:
                    stimuli["incongruent"].append((color, colors[color2], color, False))
    
        return stimuli
    
    
    def stimuli_중복확인(stimuli):
        # mskey = 'neutral'
        msset = []
        for mskey in stimuli:
            for i in range(len(stimuli[mskey])):
                msset.append(stimuli[mskey][i][:3])
        print(len(msset), len(set(msset)))
        print('중복 없음', len(msset) == len(set(msset)))
        
    stimuli = generate_stimuli()
    stimuli_중복확인(stimuli)
    
    def 카드랜덤배정(true_ratio = 0.5): # true_ratio = 0.5 인자는 표시만 해놓음. 아직 숫자 바꿔도 적용안됨
        stimuli_selected = {"neutral": [], "congruent": [], "incongruent": []}
        
        for mskey in stimuli:
            msset_a_condition_true = []
            msset_a_condition_false = []
            for i in range(len(stimuli[mskey])):
                if stimuli[mskey][i][-1]:
                    msset_a_condition_true.append(stimuli[mskey][i])
                elif not(stimuli[mskey][i][-1]):
                    msset_a_condition_false.append(stimuli[mskey][i])
            """  
            경우의 수에서, True, False 각각 10개를 뽑을껀데 총 경우의수가 네개 일 경우 예외처리가 필요함.
            예외처리 대신 네개의 경우의 수를 3번 자가 중첩시켜서 12개의 경우의 수로 만들고, 
            모든 conditions 를 12개의 경우의 수로 만들어서 동일하게 처리
            """
            if len(msset_a_condition_true) == 4:
                msset_a_condition_true_duplicate = []
                for _ in range(3):
                    msset_a_condition_true_duplicate += msset_a_condition_true
                msset_a_condition_true = msset_a_condition_true_duplicate
                
            print(mskey, len(msset_a_condition_true), len(msset_a_condition_false))
            
            slist = random.sample(msset_a_condition_true, 10) + random.sample(msset_a_condition_false, 10)
            random.shuffle(slist)
            stimuli_selected[mskey] = slist
            
        return stimuli_selected
        
    if False: # 최소 생성시에만 사용
        stimuli_selected = 카드랜덤배정()
        psave2 = r'C:\\mscode\\cardsets\\cardset6.pkl'
        with open(psave2, 'wb') as file:
            pickle.dump(stimuli_selected, file)
            
    # def display_start_screen():

    # Function to run a block of trials
    def run_block(stimuli_selected, savepath=None, click_start_time=None):
        # pyautogui.click()
        for condition in stimuli_selected:
            
            # trial = stimuli_selected[condition][0]
            for trial in stimuli_selected[condition]:
                pygame.event.clear()

                top_word, top_color, bottom_word, is_correct = trial
        
                # Clear screen for new trial
                screen.fill(colors["하양"])
        
                # Display the top word in its color
                # font = pygame.font.SysFont(None, FONT_SZ)
                font = pygame.font.SysFont('malgungothic', FONT_SZ)
                top_text = font.render(top_word, True, top_color)
                top_rect = top_text.get_rect(center=(W/2, int(H/2 - (H*(1/12)))))  # Centered, adjusted for top position
                screen.blit(top_text, top_rect)
        
                pygame.display.flip()
        
                # Introduce a time gap before displaying the bottom word
                pygame.time.wait(100)  # 100 milliseconds gap as an example
                
                # Now display the bottom word (color name) in black
                bottom_text = font.render(bottom_word, True, colors["검정"])
                bottom_rect = bottom_text.get_rect(center=(W/2, int(H/2 + (H*(1/12)))))  # Centered, adjusted for bottom position
                screen.blit(bottom_text, bottom_rect)
        
                pygame.display.flip()
        
                # Timing and response handling starts after displaying the bottom word
                start_time = pygame.time.get_ticks()
                response_made = False
                response = None
        
                while not response_made and (pygame.time.get_ticks() - start_time) < 1500:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                            
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:  # ESC 키를 누르면
                                pygame.quit()
                                quit()
                            
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:  # Left click for "Yes"
                                response = "Yes"
                                response_made = True
                            elif event.button == 3:  # Right click for "No"
                                response = "No"
                                response_made = True
        
                # Calculate response time
                response_time = pygame.time.get_ticks() - start_time if response_made else 1500
    
                # Clear screen before the next trial
                # screen.fill(colors["하양"])
                # pygame.display.flip()
                
                screen.fill(colors["하양"])
                font = pygame.font.SysFont('malgungothic', FONT_SZ)
                text = font.render("+", True, colors["검정"])  # Using "+" as a fixation dot
                rect = text.get_rect(center=(int(W/2), int(H/2)))
                screen.blit(text, rect)
                pygame.display.flip()
                
                total_wait_time = 2000  # 1.5초의 응답 시간 + 500ms의 추가 대기 시간
                elapsed_time = pygame.time.get_ticks() - start_time  # 이미 경과한 시간
                remaining_time = total_wait_time - elapsed_time  # 남은 대기 시간 계산
                
                # 남은 대기 시간만큼 대기
                if remaining_time > 0:
                    pygame.time.wait(remaining_time)
                
                
                save_time = time.time() # msdict 저장하기 바로 전 시간 기록
                elapsed_time = save_time - click_start_time

                msdict = {
                    'Condition': condition,
                    'Top Word': top_word,
                    'Top Color': top_color,
                    'Bottom Word': bottom_word,
                    'Response': response,
                    'Correct': is_correct,
                    'Response Time': response_time,
                    'response_made': response_made,
                    'running_time': elapsed_time * 1000,
                    # 'nonvalid_click_time': nonvalid_click_time_saves
                }
                print('Response', msdict['Response'], 'Correct', msdict['Correct'], \
                      'Response Time', msdict['Response Time'], 'running_time', msdict['running_time'])
                # mssave.append(msdict)
                
                base_path = savepath
                filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_eegdata.pkl")
                full_path = os.path.join(base_path, filename)
                
                # Save msdict to a file with the generated filename
                with open(full_path, 'wb') as file:
                    pickle.dump(msdict, file)
    
    
    #%%

    initial_x, initial_y = pyautogui.position()
    pyautogui.click(544, 15) ;time.sleep(1)
    pyautogui.move(initial_x, initial_y, duration=0)
    
    time.sleep(5)
    
    x, y = 130, 67
    pyautogui.FAILSAFE = False
    print(initial_x, initial_y)
    initial_x, initial_y = pyautogui.position()
    pyautogui.click(x, y)
    pyautogui.move(initial_x, initial_y, duration=0)
    click_start_time = time.time()
    # pyautogui.move(initial_x, initial_y, duration=0)
    # pyautogui.click(initial_x, initial_y)
    pygame.init()
    screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
    # run_predisp()
    
    run_baseline(duration=1)
    
    screen.fill(colors["하양"])  # 화면을 흰색으로 채웁니다.
    # "클릭하여 시작합니다." 텍스트 렌더링
    font = pygame.font.SysFont('malgungothic', FONT_SZ)  # 폰트 설정
    text = font.render("클릭하여 시작합니다.", True, colors["검정"])  # 텍스트 생성
    rect = text.get_rect(center=(W/2, H/2))  # 텍스트의 위치를 화면 중앙으로 설정
    screen.blit(text, rect)  # 텍스트를 화면에 그립니다.
    pygame.display.flip()  # 화면을 갱신하여 텍스트를 표시합니다.
    running = True  # 화면이 표시되는 동안 True로 유지됩니다.
    while running:
        for event in pygame.event.get():  # 이벤트를 확인합니다.
            if event.type == pygame.QUIT:  # 창이 닫힐 경우
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 감지
                if event.button == 1:  # 왼쪽 클릭
                    running = False  # 화면 종료
    
    # display_start_screen()
    for block_n in range(2):
        # stimuli_selected = 카드랜덤배정()
        cn = (trial_num-1)*2 + block_n + 1
        psave2 = r'C:\\mscode\\cardsets\\cardset' + str(cn) + '.pkl'
        with open(psave2, 'rb') as file:
            stimuli_selected = pickle.load(file)

        # pygame_window = gw.getWindowsWithTitle('pygame window')[0]  # 첫 번째 일치하는 윈도우
        # pygame_window.activate()
        # display_start_screen()
        run_baseline(duration=1000 * 10)
        run_block(stimuli_selected, savepath=block_paths[block_n], click_start_time=click_start_time)
    run_baseline()
    pygame.quit()


#%%

# msmain('mstest')


#%%
import sys

if __name__ == "__main__":
    msmain(sys.argv[1])

# 종료 버튼 누르기
# 인자 입력받아서 폴더 만들고 저장하기
# block 단위로 저장하기





