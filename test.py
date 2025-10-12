import pygame

pygame.init()

display = pygame.display.set_mode((800, 400)) # 윈도우 크기
pygame.display.set_caption("Duda") # 윈도우 이름

y_pos = display.get_height() // 2 # 원의 중심의 y좌표
x_pos = display.get_width() // 2 # 원의 중심의 x좌표

# 이동 관련 변수들
move_factor = 1
to_y = 0 # 위, 아래 방향키를 눌렀을 때(KEYDOWN), y_pos에 (+-)move_factor 만큼 더한다
to_x = 0 # 왼쪽, 오른쪽 방향키를 눌렀을 때(KEYDOWN), x_pos에 (+-)move_factor 만큼 더한다

fps = pygame.time.Clock()

play = True
while play:
    deltaTime = fps.tick(60) # 60프레임 유지
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 종료 감지
            play = False

        if event.type == pygame.KEYDOWN: # 키 입력 감지
            if event.key == pygame.K_LEFT:
                to_x = -move_factor

            if event.key == pygame.K_RIGHT:
                to_x = move_factor

            if event.key == pygame.K_UP:
                to_y = -move_factor

            if event.key == pygame.K_DOWN:
                to_y = move_factor
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_x = 0

            if event.key == pygame.K_RIGHT:
                to_x = 0

            if event.key == pygame.K_UP:
                to_y = 0

            if event.key == pygame.K_DOWN:
                to_y = 0

    y_pos += to_y
    x_pos += to_x

    display.fill((255, 255, 255)) # 배경색 변경
    # pygame.draw.circle(그릴화면, (R, G , B), (원의 x좌표, 원의 y좌표), 반지름)
    pygame.draw.circle(display, (0, 255, 0), (x_pos, y_pos), 5) # 원을 그림
    pygame.display.update() # 디스플레이의 변경사항을 화면에 반영

pygame.quit()