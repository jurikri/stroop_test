import pygame
import sys

pygame.init()

# 윈도우 설정
W, H = 800, 600  # 화면 크기 설정
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("텍스트 입력 예제")

# 색상 정의
colors = {
    "하양": (255, 255, 255),
    "검정": (0, 0, 0),
    "회색": (200, 200, 200)
}

# 폰트 설정

# noto_sans_kr_font_path = r'NotoSansThai-Regular.ttf'  # 폰트 파일 경로를 적절히 수정하세요.
FONT_SZ = 36
# font = pygame.font.Font(noto_sans_kr_font_path, FONT_SZ)


font = pygame.font.SysFont('malgungothic', FONT_SZ)

# 입력 텍스트 관리 변수
input_text = ''
active = False  # 텍스트 입력 상태를 관리하는 플래그
cursor_visible = True  # 커서 가시성 상태
last_cursor_toggle_time = pygame.time.get_ticks()
cursor_blink_interval = 500  # 커서 깜빡임 간격 (밀리초)

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
                elif event.key == pygame.K_BACKSPACE:  # 백스페이스 처리
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode  # 입력된 문자 추가
        if event.type == pygame.MOUSEBUTTONDOWN:
            active = True

    # 안내 문구 표시
    guide_text = font.render("영어 ID를 자유롭게 입력하세요!", True, colors["회색"])
    screen.blit(guide_text, (50, H // 2 - 50))

    # 입력 텍스트 및 커서 표시
    text_surface = font.render(input_text, True, colors["검정"])
    text_rect = text_surface.get_rect(topleft=(50, H // 2))
    screen.blit(text_surface, text_rect)

    # 커서 깜빡임 효과
    if active and cursor_visible:
        cursor_rect = pygame.Rect(text_rect.topright, (3, text_rect.height))
        pygame.draw.rect(screen, colors["검정"], cursor_rect)

    pygame.display.flip()
