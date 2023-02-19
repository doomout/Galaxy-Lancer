import pygame
import sys

# 이미지 로딩
img_galaxy = pygame.image.load("image_gl/galaxy.png")

bg_y = 0

def main():  # 메인 루프
    global bg_y

    pygame.init()
    pygame.display.set_caption("Galaxy Lancer")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get(): #이벤트 반복 처리
            if event.type == pygame.QUIT: #윈도우 x버튼 누른 경우
                pygame.quit() #pygame 모듈 초기화 해제
                sys.exit() #프로그램 종료
            if event.type == pygame.KEYDOWN: #키를 누르는 이벤트 발생시
                if event.key == pygame.K_F1: #f1 키를 누르면...
                    screen = pygame.display.set_mode((960, 720), pygame.FULLSCREEN) #전체 화면
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE: # f2, ESC 키를 누르면
                    screen = pygame.display.set_mode((960, 720)) #원래 화면으로 전환

        # 배경 스크롤
        bg_y = (bg_y + 16) % 720 #배경 스크롤 위치계산
        screen.blit(img_galaxy, [0, bg_y - 720]) #배경 y 축으로 그리기(위쪽)
        screen.blit(img_galaxy, [0, bg_y]) #배경 y축으로 그리기(아래쪽)

        pygame.display.update() #화면 업데이트
        clock.tick(30) #30프레임으로 반복

if __name__ == '__main__':
    main()
