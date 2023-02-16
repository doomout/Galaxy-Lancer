import pygame
import sys
from pygame.locals import *

# 이미지 로딩
img_galaxy = pygame.image.load("image_gl/galaxy.png") #배경이미지
img_sship = [
    pygame.image.load("image_gl/starship.png"), #기본 이미지(0번)
    pygame.image.load("image_gl/starship_l.png"), #왼쪽 기운 이미지(1번)
    pygame.image.load("image_gl/starship_r.png"), #오른쪽 기운 이미지(2번)
    pygame.image.load("image_gl/starship_burner.png") #불꽃
]
img_weapon = pygame.image.load("image_gl/bullet.png") #무기 이미지

tmr = 0
bg_y = 0

ss_x = 480
ss_y = 360
ss_d = 0

msl_f = False #탄환 발사중인지 체크 변수
msl_x = 0 #탄환 x좌표
msl_y = 0 #탄환 y좌표


def move_starship(scrn, key):  # 플레이어 기체 이동
    global ss_x, ss_y, ss_d
    ss_d = 0 #기본 기체 이미지
    if key[K_UP] == 1:
        ss_y = ss_y - 20
        if ss_y < 80:
            ss_y = 80
    if key[K_DOWN] == 1:
        ss_y = ss_y + 20
        if ss_y > 640:
            ss_y = 640
    if key[K_LEFT] == 1:
        ss_d = 1 #왼쪽 이미지
        ss_x = ss_x - 20
        if ss_x < 40:
            ss_x = 40
    if key[K_RIGHT] == 1:
        ss_d = 2 #오른쪽 이미지
        ss_x = ss_x + 20
        if ss_x > 920:
            ss_x = 920
    if key[K_SPACE] == 1: #스페이스 키를 누르면
        set_missile() #탄환 발사
    scrn.blit(img_sship[3], [ss_x - 8, ss_y + 40 + (tmr % 3) * 2]) #엔진 불꽃 그리기
    scrn.blit(img_sship[ss_d], [ss_x - 37, ss_y - 48]) #기체 그리기

def set_missile():  # 플레이어 기체 발사 탄환 설정
    global msl_f, msl_x, msl_y
    if msl_f == False: #탄환이 발사되지 않았다면!
        msl_f = True #탄환 발사 모드로 설정
        msl_x = ss_x #x 좌표는 기체 앞 끝
        msl_y = ss_y - 50 #y 좌표는 기체

def move_missile(scrn):  # 탄환 이동
    global msl_f, msl_y
    if msl_f == True: #탄환 발사 모드
        msl_y = msl_y - 36 #y 좌표 계산
        scrn.blit(img_weapon, [msl_x - 10, msl_y - 32]) #탄환 이미지 그리기
        if msl_y < 0: #탄환이 화면 밖으로 나가면...
            msl_f = False #탄환 미발사 모드
            
def main():  # 메인 루프
    global tmr, bg_y

    pygame.init()
    pygame.display.set_caption("Galaxy Lancer")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()

    while True:
        tmr = tmr + 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_F1:
                    screen = pygame.display.set_mode((960, 720), FULLSCREEN)
                if event.key == K_F2 or event.key == K_ESCAPE:
                    screen = pygame.display.set_mode((960, 720))

        # 배경 스크롤
        bg_y = (bg_y + 16) % 720
        screen.blit(img_galaxy, [0, bg_y - 720])
        screen.blit(img_galaxy, [0, bg_y])

        key = pygame.key.get_pressed()
        move_starship(screen, key) #기체 이동 함수
        move_missile(screen) #탄환 발사 함수

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
