from pygame.locals import *
import Image

EFFECT_MAX = 100 #폭발 연출 최대 수 정의
eff_no = 0 #폭발 연출시 사용할 리스트 인덱스 변수
eff_p = [0] * EFFECT_MAX #폭발 이미지 번호 리스트
eff_x = [0] * EFFECT_MAX #폭발 x좌표 리스트
eff_y = [0] * EFFECT_MAX #폭발 y좌표 리스트

   
def set_effect(x, y):  # 폭발 설정
    global eff_no
    eff_p[eff_no] = 1
    eff_x[eff_no] = x
    eff_y[eff_no] = y
    eff_no = (eff_no + 1) % EFFECT_MAX

def draw_effect(scrn):  # 폭발 연출
    for i in range(EFFECT_MAX):
        if eff_p[i] > 0:
            scrn.blit(Image.img_explode[eff_p[i]], [eff_x[i] - 48, eff_y[i] - 48]) #폭발 연출 표시
            eff_p[i] = eff_p[i] + 1 #폭발 이미지 인덱스 1씩 증가
            if eff_p[i] == 6: #6번 이미지까지 갔으면~
                eff_p[i] = 0 #0번 이미지(없음)