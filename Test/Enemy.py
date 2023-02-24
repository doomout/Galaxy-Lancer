import pygame
import math
import random
from pygame.locals import *
import Image
import Player
import Effect
import Game

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

def bring_enemy():  # 적 기체 등장
    if Game.tmr % 30 == 0:
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
    global score, ss_shield
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
                w = Image.img_enemy[emy_type[i]].get_width() #적 이미지 가로(픽셀수)
                h = Image.img_enemy[emy_type[i]].get_height() #적 기체 이미지 세로(픽셀수)
                r = int((w + h) / 4) + 12 #히트 체크에 사용할 거리 계산
                for n in range(Player.MISSILE_MAX):
                    if Player.msl_f[n] == True and Player.get_dis(emy_x[i], emy_y[i], Player.msl_x[n], Player.msl_y[n]) < r * r: #기체 탄환과 접촉 여부 판단
                        Player.msl_f[n] = False #탄환 삭제
                        Effect.set_effect(emy_x[i], emy_y[i]) #폭발 이펙트
                        score = score + 100 #점수 증가
                        emy_f[i] = False #적 기체 삭제
                        if ss_shield < 100: #플레이어 쉴드량이 100미만이면
                            ss_shield = ss_shield + 1 #쉴드량 1 증가
                        
            img_rz = pygame.transform.rotozoom(Image.img_enemy[png], ang, 1.0) #적 회전 이미지 생성
            scrn.blit(img_rz, [emy_x[i] - img_rz.get_width() / 2, emy_y[i] - img_rz.get_height() / 2]) #적 이미지 그리기
 