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