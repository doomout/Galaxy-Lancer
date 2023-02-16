#슈팅 게임  
언어 : 파이썬 3.11.1  
IDE : vs code  
Pygame 설치시 주의점  
-현재 pygame는 python 3.11 버전을 지원하지 않기에 pre-release 버전을 설치해야 한다.  
-명령어 : pip3 install pygame --pre  

게임 규칙  
1. 방향키로 기체를 움직인다.  
2. 스페이스 키로 탄환을 발사한다.  
3. z키로 탄막을 펼친다. 일정량의 실드를 사용한다.  

파이썬 문법
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
#배경 스크롤
bg_y = (bg_y + 16) % 720 
screen.blit(img_galaxy, [0, bg_y - 720])
screen.blit(img_galaxy, [0, bg_y])
#사용자 키 입력 받기
key = pygame.key.get_pressed() #튜플은()로 선언, 리스트는 []로 선언
move_starship(screen, key)

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
    scrn.blit(img_sship[3], [ss_x - 8, ss_y + 40 + (tmr % 3) * 2]) #엔진 불꽃 그리기
    scrn.blit(img_sship[ss_d], [ss_x - 37, ss_y - 48]) #기체 그리기
```