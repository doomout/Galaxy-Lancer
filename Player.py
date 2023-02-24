import pygame
import math
from pygame.locals import *
import Image
import Enemy
import Effect
import Sound
import Game


ss_x = 0
ss_y = 0
ss_d = 0
ss_shield = 0 #쉴드량 변수
ss_muteki = 0 #플레이어 기체 무적 상태 변수
key_spc = 0 #스페이스를 눌렀을 때 사용할 변수
key_z = 0 #z키룰 늘렀을 때 사용할 변수

MISSILE_MAX = 200 #최대 탄환 수
msl_no = 0 #탄환 발사에 사용할 리스트 인덱스
msl_f = [False] * MISSILE_MAX #탄환 발사 중인지 체크 리스트
msl_x = [0] * MISSILE_MAX #탄환의 x좌표 리스트
msl_y = [0] * MISSILE_MAX #탄환의 y좌표 리스트
msl_a = [0] * MISSILE_MAX #탄환이 날라가는 각도 리스트

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
        Sound.se_shot.play() #발사음 출력
    key_z = (key_z + 1) * key[K_z] #z키를 누르는 동안 변수 값 증가
    if key_z == 1 and ss_shield > 10: #한번 눌렀을 때 실드량이 10보다 크다면~
        set_missile(10) #탄막 치기
        ss_shield = ss_shield - 10 #쉴드량 10 감소
        Sound.se_barrage.play() #탄막 사운드 출력
    if ss_muteki % 2 == 0: #0 > 1 > 0 > 1 과 같이 교대로 반복되어 0이 되면 무적
        scrn.blit(Image.img_sship[3], [ss_x - 8, ss_y + 40 + (Game.tmr % 3) * 2]) #엔진 불꽃 그리기
        scrn.blit(Image.img_sship[ss_d], [ss_x - 37, ss_y - 48]) #기체 그리기     
    if ss_muteki > 0: #무적 상태라면
        ss_muteki = ss_muteki - 1 
        return #함수를 벗어남(히트 체크 미수행)
    elif Game.idx == 1:
        for i in range(Enemy.ENEMY_MAX):  # 적 기체와 히트 체크
            if Enemy.emy_f[i] == True: #적 기체가 존재하면
                w = Image.img_enemy[Enemy.emy_type[i]].get_width()
                h = Image.img_enemy[Enemy.emy_type[i]].get_height()
                r = int((w + h) / 4 + (74 + 96) / 4)
                if get_dis(Enemy.emy_x[i], Enemy.emy_y[i], ss_x, ss_y) < r * r: #적과 충돌하면.
                    Effect.set_effect(ss_x, ss_y) #폭발 연출
                    ss_shield = ss_shield - 10 #쉴드 10 감소
                    if ss_shield <= 0: #쉴드가 0이하가 되면
                        ss_shield = 0 #0으로 설정
                        Game.idx = 2 #게임오버
                        Game.tmr = 0 
                    if ss_muteki == 0: #무적 상태가 아니라면
                        ss_muteki = 60 #60프레임으로 설정
                        Sound.se_damage.play() #데미지 효과음 출력
                    Enemy.emy_f[i] = False #적 삭제

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
            img_rz = pygame.transform.rotozoom(Image.img_weapon, -90 - msl_a[i], 1.0) #날아가는 각도의 회전 이미지 생성
            scrn.blit(img_rz, [msl_x[i] - img_rz.get_width() / 2, msl_y[i] - img_rz.get_height() / 2]) #탄환 이미지 그리기
            if msl_y[i] < 0 or msl_x[i] < 0 or msl_x[i] > 960: #탄환 화면 밖으로 나가면
                msl_f[i] = False #탄환삭제