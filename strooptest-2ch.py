# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:53:04 2024

@author: PC
"""



def msmain(arg1=None):
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
    package_names = ['pygame', 'PyAutoGUI', 'pywin32', 'pygetwindow', 'screeninfo']
    for package_name in package_names:
        install_package(package_name)
        
    import pygetwindow as gw
    import pygame
    import pyautogui
    from screeninfo import get_monitors

    for monitor in get_monitors():
        print(monitor)


    def set_pygame_window_position(x, y, width, height):
        """
        Pygame window의 위치와 크기를 설정합니다.
        """
        import win32gui
        import win32con

        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, width, height, 0)
        
    import pyautogui
    import pygame
    import random
    import time
    from datetime import datetime
    import os
    import pickle
    current_path = os.getcwd()
    # from datetime import datetime
    import time

    # base_path, trial_num = create_trial_folder(arg1)
    # print("Base path set to:", base_path)


    # Define colors
    colors = {
        "빨강": (255, 0, 0),
        "초록": (0, 255, 0),
        "파랑": (0, 0, 255),
        "노랑": (255, 255, 0),
        "검정": (0, 0, 0),
        "하양": (255, 255, 255)
    }
   
    W, H = 1080, 1920
    FONT_SZ = int(round(46*(H/800)))

    def run_baseline(duration=10 * 1000, disp="+"):  # Default duration set to 30 seconds -> 30으로 추후 수정
        screen.fill(colors["하양"])
        font = pygame.font.SysFont('malgungothic', FONT_SZ)
        text = font.render(disp, True, colors["검정"])  # Using "+" as a fixation dot
        rect = text.get_rect(center=(int(W/2), int(H/2)))
        screen.blit(text, rect)
        pygame.display.flip()
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
    def run_block(stimuli_selected, savepath=None, msid=None):
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
                cue_time_stamp = time.time()
        
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

                # save_time = time.time() # msdict 저장하기 바로 전 시간 기록
                msdict = {
                    'Condition': condition,
                    'Top Word': top_word,
                    'Top Color': top_color,
                    'Bottom Word': bottom_word,
                    'Response': response,
                    'Correct': is_correct,
                    'Response Time': response_time,
                    'response_made': response_made,
                    'save_time_stamp': time.time(),
                    'cue_time_stamp': cue_time_stamp
                    # 'nonvalid_click_time': nonvalid_click_time_saves
                }
                
                if msdict['Correct'] and msdict['Response']=='Yes': iscorrect = '맞음'
                elif not(msdict['Correct']) and msdict['Response']=='No': iscorrect = '맞음'
                elif msdict['Response'] is None: iscorrect = '응답 안함'
                else: iscorrect = '틀림'
 
                print('Correct', iscorrect, 'Response Time', msdict['Response Time'])

                base_path = savepath
                filename = datetime.now().strftime("%Y%m%d_%H%M%S_stroopdata.pkl")
                full_path = os.path.join(base_path, filename)
                
                # Save msdict to a file with the generated filename
                with open(full_path, 'wb') as file:
                    pickle.dump(msdict, file)
    
    #%%
    # import pygame
    from screeninfo import get_monitors
    import win32gui
    import win32con
    
    def set_window_position(x, y, width, height):
        """
        지정된 위치와 크기로 Pygame 윈도우의 위치를 설정합니다.
        """
        hwnd = pygame.display.get_wm_info()['window']
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, width, height, win32con.SWP_NOZORDER)
    
    
    import pyautogui
    import time
    
    # for _ in range(10):
    #     time.sleep(0.5)
    #     x, y = pyautogui.position()
    #     print(f"Current mouse position is: {x}, {y}")
    
    initial_x, initial_y = pyautogui.position()
    pyautogui.click(134, 63) ;time.sleep(1)
    pyautogui.move(initial_x, initial_y, duration=0)


    pygame.init()
    monitors = get_monitors()
    
    if len(monitors) > 1:
        # 보조 모니터가 있다고 가정하고, 보조 모니터 정보를 사용합니다.
        secondary_monitor = monitors[1]
        screen = pygame.display.set_mode((secondary_monitor.width, secondary_monitor.height), pygame.NOFRAME)  # 무테두리 창 생성
        set_window_position(secondary_monitor.x, secondary_monitor.y, secondary_monitor.width, secondary_monitor.height)
    else:
        print("보조 모니터가 감지되지 않았습니다. 기본 설정으로 실행합니다.")
        screen = pygame.display.set_mode((1800, 1200))
        
    run_baseline(duration=1)
    def wait_screen():
        screen.fill(colors["하양"])  # 화면을 흰색으로 채웁니다.
        font = pygame.font.SysFont('malgungothic', FONT_SZ)  # 폰트 설정
        text = font.render("클릭하여 시작합니다.", True, colors["검정"])  # 텍스트 생성
        rect = text.get_rect(center=(W/2, H/2))  # 텍스트의 위치를 화면 중앙으로 설정
        screen.blit(text, rect)  # 텍스트를 화면에 그립니다.
        pygame.display.flip()  # 화면을 갱신하여 텍스트를 표시합니다.
        
    def id_input():
        input_text = ''
        active = False  # 텍스트 입력 상태를 관리하는 플래그
        cursor_visible = True  # 커서 가시성 상태
        last_cursor_toggle_time = pygame.time.get_ticks()
        cursor_blink_interval = 500  # 커서 깜빡임 간격 (밀리초)
        font = pygame.font.SysFont('malgungothic', 30)  # 폰트 설정
        
        # 메인 이벤트 루프
        running = True
        while running:
            screen.fill(colors["하양"])
            # 커서 깜빡임 처리
            current_time = pygame.time.get_ticks()
            if current_time - last_cursor_toggle_time > cursor_blink_interval:
                cursor_visible = not cursor_visible
                last_cursor_toggle_time = current_time

            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:  # Enter 키
                            msid = input_text
                            print(f"입력 완료: {msid}")  # 콘솔에 입력된 텍스트 출력
                            input_text = ''  # 입력 필드 초기화
                            running = False
                        elif event.key == pygame.K_BACKSPACE:  # 백스페이스 처리
                            input_text = input_text[:-1]
                        else:
                            input_text += event.unicode  # 입력된 문자 추가
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = True

            # 안내 문구 표시
            guide_text = font.render("영어 ID를 자유롭게 입력하세요!", True, (154, 164, 174))
            text_rect = guide_text.get_rect(center=(W/2, H/2-200))  # 텍스트의 위치를 화면 중앙으로 설정
            screen.blit(guide_text, text_rect)  # 텍스트를 화면에 그립니다.

            # 입력 텍스트 및 커서 표시
            text_surface = font.render(input_text, True, colors["검정"])
            text_rect = text_surface.get_rect(center=(W/2, H/2))  # 텍스트의 위치를 화면 중앙으로 설정
            screen.blit(text_surface, text_rect)  # 텍스트를 화면에 그립니다.

            # 커서 깜빡임 효과
            if active and cursor_visible:
                cursor_rect = pygame.Rect(text_rect.topright, (3, text_rect.height))
                pygame.draw.rect(screen, colors["검정"], cursor_rect)

            pygame.display.flip()
        return msid
        
    wait_screen()
    msid = id_input()
    # msid = msid + '_' + datetime.now().strftime("%m%d%H%M%S")
    
    # Create block directories
    current_path = os.getcwd()
    now = datetime.now()
    filename = now.strftime("%Y%m%d%H%M")
    filename2 = filename + '_' + msid
    base_path_template = current_path + '\\saved_data\\' + filename2
    if not os.path.exists(base_path_template):
        os.makedirs(base_path_template)
    
    block_paths = []
    for i in range(1, 3):  # 1 to 8
        block_path = os.path.join(base_path_template, f"block{i}")
        block_paths.append(block_path)
        if not os.path.exists(block_path):
            os.makedirs(block_path)
            
    wait_screen()
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
    for block_n in range(1):
        # stimuli_selected = 카드랜덤배정()
        cn = block_n + 1
        if arg1 == 1: cn += 2
        if arg1 == 2: cn += 4
            
        psave2 = os.getcwd() + '\\cardsets\\cardset' + str(cn) + '.pkl'
        with open(psave2, 'rb') as file:
            stimuli_selected = pickle.load(file)

        run_baseline(duration=1000 * 10)
        run_block(stimuli_selected, savepath=block_paths[block_n], msid=msid)
        
    run_baseline(duration=3 * 1000, disp="테스트 끝!")
    pygame.quit()



#%%
import sys

if __name__ == "__main__":
    # msmain(sys.argv[1])
    msmain(0)





