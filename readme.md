#슈팅 게임  
언어 : 파이썬 3.11.1  
IDE : vs code  
Pygame 설치시 주의점  
-현재 pygame는 python 3.11 버전을 지원하지 않기에 pre-release 버전을 설치해야 한다.  
-명령어 : pip3 install pygame --pre  

게임 핵심 함수들
1. 배경 이미지 움직이는 함수
```py
global bg_y
pygame.init()
pygame.display.set_caption("Galaxy Lancer")
screen = pygame.display.set_mode((960, 720))
clock = pygame.time.Clock()
while True:
    # 배경 스크롤
    bg_y = (bg_y + 16) % 720 #배경 스크롤 위치계산
    screen.blit(img_galaxy, [0, bg_y - 720]) #배경 y 축으로 그리기(위쪽)
    screen.blit(img_galaxy, [0, bg_y]) #배경 y축으로 그리기(아래쪽)

    pygame.display.update() #화면 업데이트
    clock.tick(30) #30프레임으로 반복
```
2. 튜플을 사용한 키보드 받기 함수(튜플=값을 변경할 수 없는 리스트)
```py
#사용자 키 입력 받기
key = pygame.key.get_pressed() #튜플은()로 선언, 리스트는 []로 선언
```
3. 탄환 발사 함수(1발씩일 때)
```py
msl_f = False #탄환 발사중인지 체크 변수
msl_x = 0 #탄환 x좌표
msl_y = 0 #탄환 y좌표
if key[K_SPACE] == 1: #스페이스 키를 누르면
    set_missile() #탄환 발사

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
```
4. 탄환 발사 함수(연속으로 발사일 때)
```py
MISSILE_MAX = 200 #최대 탄환 수
msl_no = 0 #탄환 발사에 사용할 리스트 인덱스
msl_f = [False] * MISSILE_MAX #탄환 발사 중인지 체크 리스트
msl_x = [0] * MISSILE_MAX #탄환의 x좌표
msl_y = [0] * MISSILE_MAX #탄환의 y좌표

def set_missile():  # 플레이어 기체 발사 탄환 설정
    global msl_no 
    msl_f[msl_no] = True #탄환 발사 플래그
    msl_x[msl_no] = ss_x #탄환의 x좌표 대입
    msl_y[msl_no] = ss_y - 50 #탄환의 y좌표 대입
    msl_no = (msl_no + 1) % MISSILE_MAX #탄환 변호 계산

def move_missile(scrn):  # 탄환 이동
    for i in range(MISSILE_MAX):
        if msl_f[i] == True: #탄환이 발사 상태라면
            msl_y[i] = msl_y[i] - 36 #y좌표 계산
            scrn.blit(img_weapon, [msl_x[i] - 10, msl_y[i] - 32]) #탄환 이미지 그리기
            if msl_y[i] < 0: #탄환 화면 밖으로 나가면
                msl_f[i] = False #탄환삭제
```
5. 탄환 발사 딜레이
```py
key_spc = 0 #스페이스를 눌렀을 때 사용할 변수

key_spc = (key_spc + 1) * key[K_SPACE] #스페이스 키를 누르는 동안 변수 값 증가
if key_spc % 5 == 1: #스페이스 누른 후, 5프레임마다 탄환 발사(탄환 딜레이)
    set_missile() #탄환 발사
```
6. 탄막 아이디어  
픽셀 수 * math.cos(각도)가 x축 방향의 좌표 변화  
msl_x[i] = msl_x[i] + 36 * math.cos(math.radians(msl_a[i]))   
픽셀 수 * math.sin(각도)가 y축 방향의 좌표 변화  
msl_y[i] = msl_y[i] + 36 * math.sin(math.radians(msl_a[i]))  
```py
key_z = 0 #z키룰 늘렀을 때 사용할 변수
msl_a = [0] * MISSILE_MAX #탄환이 날라가는 각도 리스트

key_z = (key_z + 1) * key[K_z] #z키를 누르는 동안 변수 값 증가
if key_z == 1: #z키를 1번 누르면
    set_missile(10) #탄막 치기

def set_missile(typ):  # 플레이어 기체 발사 탄환 설정
    global msl_no     
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
            
            #날아가는 각도의 회전 이미지 생성(원래 이미지, 회전각, 확대비율)
            img_rz = pygame.transform.rotozoom(img_weapon, -90 - msl_a[i], 1.0)
            
            #탄환 이미지 그리기
            scrn.blit(img_rz, [msl_x[i] - img_rz.get_width() / 2, msl_y[i] - img_rz.get_height() / 2]) 
            if msl_y[i] < 0 or msl_x[i] < 0 or msl_x[i] > 960: #탄환 화면 밖으로 나가면
                msl_f[i] = False #탄환삭제
```
7.적 이동, 적 탄환 함수
```py
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
            #화면 상하좌우에서 벗어나면
            if emy_x[i] < LINE_L or LINE_R < emy_x[i] or emy_y[i] < LINE_T or LINE_B < emy_y[i]: 
                emy_f[i] = False #적 삭제
            img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.0) #적 회전 이미지 생성
            scrn.blit(img_rz, [emy_x[i] - img_rz.get_width() / 2, emy_y[i] - img_rz.get_height() / 2])
```
8. 탄환과 적의 충돌 
```py
def get_dis(x1, y1, x2, y2):  # 두 점 사이 거리 계산
    return ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

# 플레이어 기체 발사 탄환과 히트 체크
if emy_type[i] != EMY_BULLET:  #emy_type: 0은 적 탄환, 1은 적 기체(즉, 기체만 체크)
    w = img_enemy[emy_type[i]].get_width() #적 이미지 가로(픽셀수)
    h = img_enemy[emy_type[i]].get_height() #적 기체 이미지 세로(픽셀수)
    r = int((w + h) / 4) + 12 #히트 체크에 사용할 거리 계산(탄환의 반지름이 12픽셀)
    for n in range(MISSILE_MAX):
        #기체 탄환과 접촉 여부 판단
        if msl_f[n] == True and get_dis(emy_x[i], emy_y[i], msl_x[n], msl_y[n]) < r * r: 
            msl_f[n] = False #탄환 삭제
            emy_f[i] = False #적 기체 삭제
```
9. 폭발 함수
```py
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
            scrn.blit(img_explode[eff_p[i]], [eff_x[i] - 48, eff_y[i] - 48]) #폭발 연출 표시
            eff_p[i] = eff_p[i] + 1 #폭발 이미지 인덱스 1씩 증가
            if eff_p[i] == 6: #6번 이미지까지 갔으면~
                eff_p[i] = 0 #0번 이미지(없음)
```
10. 플레이어와 적 충돌 했을 때 쉴드 감소, 2초 동안 무적
```py
if ss_muteki % 2 == 0: ##0 > 1 > 0 > 1 과 같이 교대로 반복되어 0이 되면 무적
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
                ss_muteki = 60 #무적 상태로 설정
            emy_f[i] = False #적 삭제
```
11. 쉴드 화면 처리
```py
screen.blit(img_shield, [40, 680]) #쉴드 화면 그리기
#쉴드가 감소할 때 마다 사각형으로 덮어서 표현
pygame.draw.rect(screen, (64, 32, 32), [40 + ss_shield * 4, 680, (100 - ss_shield) * 4, 12]) 
```
12. 문자열 표시 함수
```py
def draw_text(scrn, txt, x, y, siz, col):  # 문자 표시
    fnt = pygame.font.Font(None, siz)
    sur = fnt.render(txt, True, col)
    x = x - sur.get_width() / 2
    y = y - sur.get_height() / 2
    scrn.blit(sur, [x, y])
```
13. Pygame 사운드 명령어(Pygame 사운드 파일은 ogg 형식이 mp3파일보다 재생시 안전하다.)   

(1) BGM 명령어  
- 파일로딩 : pygame.mixer.music.load(파일명)
- 재생 : pygame.mixer.music.play(인수) #-1:반복재생, 0:1회 재생
- 정지 : pygame.mixer.music.stop()  

(2) SE(효과음) 명령어  
- 파일로딩 : 변수명 = pygame.mixer.Sound(파일명)
- 재생 : 변수명.play()
