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
img_shield = pygame.image.load("image_gl/shield.png") #쉴드 이미지
img_enemy = [
    pygame.image.load("image_gl/enemy0.png"),
    pygame.image.load("image_gl/enemy1.png")
]
img_explode = [
    None,
    pygame.image.load("image_gl/explosion1.png"),
    pygame.image.load("image_gl/explosion2.png"),
    pygame.image.load("image_gl/explosion3.png"),
    pygame.image.load("image_gl/explosion4.png"),
    pygame.image.load("image_gl/explosion5.png")
]

tmr = 0
bg_y = 0

ss_x = 480
ss_y = 360
ss_d = 0
ss_shield = 100 #쉴드량 변수
ss_muteki = 0 #플레이어 기체 무적 상태 변수
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
EMY_BULLET = 0
LINE_T = -80 #위
LINE_B = 800 #아래
LINE_L = -80 #좌 
LINE_R = 1040 #우

EFFECT_MAX = 100 #폭발 연출 최대 수 정의
eff_no = 0 #폭발 연출시 사용할 리스트 인덱스 변수
eff_p = [0] * EFFECT_MAX #폭발 이미지 번호 리스트
eff_x = [0] * EFFECT_MAX #폭발 x좌표 리스트
eff_y = [0] * EFFECT_MAX #폭발 y좌표 리스트

def get_dis(x1, y1, x2, y2):  # 두 점 사이 거리 계산
    return ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

def move_starship(scrn, key):  # 플레이어 기체 이동
    global ss_x, ss_y, ss_d, key_spc, key_z, ss_shield, ss_muteki
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
    if key_z == 1 and ss_shield > 10: #한번 눌렀을 때 실드량이 10보다 크다면~
        set_missile(10) #탄막 치기
        ss_shield = ss_shield - 10 #쉴드량 10 감소
    if ss_muteki % 2 == 0: #0 > 1 > 0 > 1 과 같이 교대로 반복되어 0이 되면 무적
        scrn.blit(img_sship[3], [ss_x - 8, ss_y + 40 + (tmr % 3) * 2]) #엔진 불꽃 그리기
        scrn.blit(img_sship[ss_d], [ss_x - 37, ss_y - 48]) #기체 그리기     
    if ss_muteki > 0: #무적 상태라면
        ss_muteki = ss_muteki - 1 
        return #함수를 벗어남(히트 체크 미수행)
    for i in range(ENEMY_MAX):  # 적 기체와 히트 체크
        if emy_f[i] == True: #적 기체가 존재하면
            w = img_enemy[emy_type[i]].get_width()
            h = img_enemy[emy_type[i]].get_height()
            r = int((w + h) / 4 + (74 + 96) / 4)
            if get_dis(emy_x[i], emy_y[i], ss_x, ss_y) < r * r: #적과 충돌하면.
                set_effect(ss_x, ss_y) #폭발 연출
                ss_shield = ss_shield - 10 #쉴드 10 감소
                if ss_shield <= 0: #쉴드가 0이하가 되면
                    ss_shield = 0 #0으로 설정
                if ss_muteki == 0: #무적 상태가 아니라면
                    ss_muteki = 60 #60프레임으로 설정
                emy_f[i] = False #적 삭제

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
    global ss_shield
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
            
            #플레이어 기체 발사 탄환과 히트 체크
            if emy_type[i] != EMY_BULLET:  #emy_type: 0은 적 탄환, 1은 적 기체
                w = img_enemy[emy_type[i]].get_width() #적 이미지 가로(픽셀수)
                h = img_enemy[emy_type[i]].get_height() #적 기체 이미지 세로(픽셀수)
                r = int((w + h) / 4) + 12 #히트 체크에 사용할 거리 계산
                for n in range(MISSILE_MAX):
                    if msl_f[n] == True and get_dis(emy_x[i], emy_y[i], msl_x[n], msl_y[n]) < r * r: #기체 탄환과 접촉 여부 판단
                        msl_f[n] = False #탄환 삭제
                        set_effect(emy_x[i], emy_y[i]) #폭발 이펙트
                        emy_f[i] = False #적 기체 삭제
                        if ss_shield < 100: #플레이어 쉴드량이 100미만이면
                            ss_shield = ss_shield + 1 #쉴드량 1 증가
                        
            img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.0) #적 회전 이미지 생성
            scrn.blit(img_rz, [emy_x[i] - img_rz.get_width() / 2, emy_y[i] - img_rz.get_height() / 2]) #적 이미지 그리기
       
def set_effect(x, y):  # 폭발 설정
    global eff_no
    eff_p[eff_no] = 1
    eff_x[eff_no] = x
    eff_y[eff_no] = y
    eff_no = (eff_no + 1) % EFFECT_MAX

def draw_effect(scrn):  # 폭발 연출
    for i in range(EFFECT_MAX):
        if eff_p[i] > 0:
            scrn.blit(img_explode[eff_p[i]], [eff_x[i] - 48, eff_y[i] - 48]) #폭발 연출 표시
            eff_p[i] = eff_p[i] + 1 #폭발 이미지 인덱스 1씩 증가
            if eff_p[i] == 6: #6번 이미지까지 갔으면~
                eff_p[i] = 0 #0번 이미지(없음)
                     
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
                if event.key == K_F1: #F1은 전체 화면
                    screen = pygame.display.set_mode((960, 720), FULLSCREEN)
                if event.key == K_F2 or event.key == K_ESCAPE: #F2, ESC 키는 일반 화면모드 
                    screen = pygame.display.set_mode((960, 720))

        # 배경 스크롤
        bg_y = (bg_y + 16) % 720
        screen.blit(img_galaxy, [0, bg_y - 720])
        screen.blit(img_galaxy, [0, bg_y])

        key = pygame.key.get_pressed() #모든 키 상태 대입
        move_starship(screen, key) #기체 이동 함수
        move_missile(screen) #탄환 발사 함수
        bring_enemy() #적 등장
        move_enemy(screen) #적 이동
        draw_effect(screen) #폭발 연출
        screen.blit(img_shield, [40, 680]) #쉴드 화면 그리기
        #감소한 쉴드 사각형으로 그리기
        pygame.draw.rect(screen, (64, 32, 32), [40 + ss_shield * 4, 680, (100 - ss_shield) * 4, 12]) 


        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
