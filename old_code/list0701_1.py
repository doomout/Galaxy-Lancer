import pygame
import sys
import math
import random
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
img_enemy = [
    pygame.image.load("image_gl/enemy0.png"),
    pygame.image.load("image_gl/enemy1.png")
]

tmr = 0
bg_y = 0

ss_x = 480
ss_y = 360
ss_d = 0
key_spc = 0 #스페이스를 눌렀을 때 사용할 변수
key_z = 0 #z키룰 늘렀을 때 사용할 변수

MISSILE_MAX = 200 #최대 탄환 수
msl_no = 0 #탄환 발사에 사용할 리스트 인덱스
msl_f = [False] * MISSILE_MAX #탄환 발사 중인지 체크 리스트
msl_x = [0] * MISSILE_MAX #탄환의 x좌표 리스트
msl_y = [0] * MISSILE_MAX #탄환의 y좌표 리스트
msl_a = [0] * MISSILE_MAX #탄환이 날라가는 각도 리스트

ENEMY_MAX = 100 #적 최대 수
emy_no = 0 #적 등장시 사용할 리스트 인덱스 변수
emy_f = [False] * ENEMY_MAX #적 등장 여부 관리 플래그 리스트
emy_x = [0] * ENEMY_MAX #적의 x좌표 리스트
emy_y = [0] * ENEMY_MAX #적의 y좌표 리스트
emy_a = [0] * ENEMY_MAX #적의 비행각도 리스트
emy_type = [0] * ENEMY_MAX #적의 종류 리스트
emy_speed = [0] * ENEMY_MAX #적 속도 리스트

#적이 나타나고 사라지는 좌표
LINE_T = -80 #위
LINE_B = 800 #아래
LINE_L = -80 #좌 
LINE_R = 1040 #우


def move_starship(scrn, key):  # 플레이어 기체 이동
    global ss_x, ss_y, ss_d, key_spc, key_z
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
    key_spc = (key_spc + 1) * key[K_SPACE] #스페이스 키를 누르는 동안 변수 값 증가
    if key_spc % 5 == 1: #스페이스 누른 후, 5프레임마다 탄환 발사(탄환 딜레이)
        set_missile(0) #탄환 발사
    key_z = (key_z + 1) * key[K_z] #z키를 누르는 동안 변수 값 증가
    if key_z == 1: #1번 누르면
        set_missile(10) #탄막 치기
    scrn.blit(img_sship[3], [ss_x - 8, ss_y + 40 + (tmr % 3) * 2]) #엔진 불꽃 그리기
    scrn.blit(img_sship[ss_d], [ss_x - 37, ss_y - 48]) #기체 그리기

def set_missile(typ):  # 플레이어 기체 발사 탄환 설정
    global msl_no 
    
    if typ == 0:  # 단발
        msl_f[msl_no] = True #탄환 발사 플래그
        msl_x[msl_no] = ss_x #탄환의 x좌표 대입
        msl_y[msl_no] = ss_y - 50 #탄환의 y좌표 대입
        msl_a[msl_no] = 270 #탄환 발사 각도
        msl_no = (msl_no + 1) % MISSILE_MAX #탄환 변호 계산
    
    if typ == 10:  # 탄막
        for a in range(160, 390, 10):
            msl_f[msl_no] = True #탄막 발사 플레그
            msl_x[msl_no] = ss_x #탄환 x좌표 대입
            msl_y[msl_no] = ss_y - 50 #탄환 y 좌표 대입
            msl_a[msl_no] = a #탄환 발사 각도
            msl_no = (msl_no + 1) % MISSILE_MAX #다음 설정을 위한 번호 계산

def move_missile(scrn):  # 탄환 이동 
    for i in range(MISSILE_MAX):
        if msl_f[i] == True: #탄환이 발사 되었다면~
            msl_x[i] = msl_x[i] + 36 * math.cos(math.radians(msl_a[i])) #x좌표 계산
            msl_y[i] = msl_y[i] + 36 * math.sin(math.radians(msl_a[i])) #y좌표 계산
            img_rz = pygame.transform.rotozoom(img_weapon, -90 - msl_a[i], 1.0) #날아가는 각도의 회전 이미지 생성
            scrn.blit(img_rz, [msl_x[i] - img_rz.get_width() / 2, msl_y[i] - img_rz.get_height() / 2]) #탄환 이미지 그리기
            if msl_y[i] < 0 or msl_x[i] < 0 or msl_x[i] > 960: #탄환 화면 밖으로 나가면
                msl_f[i] = False #탄환삭제

def bring_enemy():  # 적 기체 등장
    if tmr % 30 == 0:
        set_enemy(random.randint(20, 940), LINE_T, 90, 1, 6)

def set_enemy(x, y, a, ty, sp):  # 적 기체 설정
    global emy_no
    while True:
        if emy_f[emy_no] == False: #리스트가 비어있다면~
            emy_f[emy_no] = True #플레그 설정
            emy_x[emy_no] = x #x좌표
            emy_y[emy_no] = y #y좌표
            emy_a[emy_no] = a #각도 대입
            emy_type[emy_no] = ty #적 종류
            emy_speed[emy_no] = sp #적 속도
            break
        emy_no = (emy_no + 1) % ENEMY_MAX #다음 설정을 위한 번호 계산

def move_enemy(scrn):  # 적 기체 이동
    for i in range(ENEMY_MAX):
        if emy_f[i] == True: #적이 존재하는가?
            ang = -90 - emy_a[i] #회전 각도 대입
            png = emy_type[i] #이미지 번호 대입
            emy_x[i] = emy_x[i] + emy_speed[i] * math.cos(math.radians(emy_a[i])) #x좌표 변화
            emy_y[i] = emy_y[i] + emy_speed[i] * math.sin(math.radians(emy_a[i])) #y좌표 변화
            if emy_type[i] == 1 and emy_y[i] > 360: #적의 y좌표가 360도를 넘었다면
                set_enemy(emy_x[i], emy_y[i], 90, 0, 8) #탄환 발사
                emy_a[i] = -45 #방향 변경
                emy_speed[i] = 16 #속도 변경
            if emy_x[i] < LINE_L or LINE_R < emy_x[i] or emy_y[i] < LINE_T or LINE_B < emy_y[i]: #화면 상하좌우에서 벗어나면
                emy_f[i] = False #적 삭제
            img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.0) #적 회전 이미지 생성
            scrn.blit(img_rz, [emy_x[i] - img_rz.get_width() / 2, emy_y[i] - img_rz.get_height() / 2]) #적 이미지 그리기
            
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
        bring_enemy()
        move_enemy(screen)

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
