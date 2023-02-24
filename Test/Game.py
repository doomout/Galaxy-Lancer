import pygame
import sys
import random
from pygame.locals import *
import Image
import Player
import Enemy
import Effect
import Sound


idx = 0
tmr = 0
score = 0
bg_y = 0

def get_dis(x1, y1, x2, y2):  # 두 점 사이 거리 계산
    return ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

def draw_text(scrn, txt, x, y, siz, col):  # 문자 표시
    fnt = pygame.font.Font(None, siz)
    sur = fnt.render(txt, True, col)
    x = x - sur.get_width() / 2
    y = y - sur.get_height() / 2
    scrn.blit(sur, [x, y])


#메인 함수
def main():  # 메인 루프
    global idx, tmr, score, bg_y, ss_x, ss_y, ss_d, ss_shield, ss_muteki
    global se_barrage, se_damage, se_explosion, se_shot

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
        screen.blit(Image.img_galaxy, [0, bg_y - 720])
        screen.blit(Image.img_galaxy, [0, bg_y])

        key = pygame.key.get_pressed() #모든 키 상태 대입
        
        if idx == 0:  # 타이틀
            img_rz = pygame.transform.rotozoom(Image.img_title[0], -tmr % 360, 1.0)
            screen.blit(img_rz, [480 - img_rz.get_width() / 2, 280 - img_rz.get_height() / 2])
            screen.blit(Image.img_title[1], [70, 160])
            draw_text(screen, "Press [SPACE] to start!", 480, 600, 50, Image.SILVER)
            if key[K_SPACE] == 1:
                idx = 1
                tmr = 0
                score = 0
                ss_x = 480
                ss_y = 600
                ss_d = 0
                ss_shield = 100
                ss_muteki = 0
                for i in range(Enemy.ENEMY_MAX):
                    Enemy.emy_f[i] = False
                for i in range(Player.MISSILE_MAX):
                    Player.msl_f[i] = False
                pygame.mixer.music.load("sound_gl/bgm.ogg") #BGM 로딩
                pygame.mixer.music.play(-1) #무한반복 재생
        
        if idx == 1:  # 게임 플레이 중
            Player.move_starship(screen, key)
            Player.move_missile(screen)
            Enemy.bring_enemy()
            Enemy.move_enemy(screen)
            if tmr == 30 * 60:
                idx = 3   
                tmr = 0

        if idx == 2:  # 게임 오버
            Player.move_missile(screen)
            Enemy.move_enemy(screen)
            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr <= 90:
                if tmr % 5 == 0:
                    Effect.set_effect(ss_x + random.randint(-60, 60), ss_y + random.randint(-60, 60))
                if tmr % 10 == 0:
                    Sound.se_damage.play()
            if tmr == 120:
                pygame.mixer.music.load("sound_gl/gameover.ogg")
                pygame.mixer.music.play(0)
            if tmr > 120:
                draw_text(screen, "GAME OVER", 480, 300, 80, Image.RED)
            if tmr == 400:
                idx = 0
                tmr = 0

        if idx == 3:  # 게임 클리어
            Player.move_starship(screen, key)
            Player.move_missile(screen)
            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr == 2:
                pygame.mixer.music.load("sound_gl/gameclear.ogg")
                pygame.mixer.music.play(0)
            if tmr > 20:
                draw_text(screen, "GAME CLEAR", 480, 300, 80, Image.SILVER)
            if tmr == 300:
                idx = 0
                tmr = 0      
                
        Effect.draw_effect(screen)  # 폭발 연출
        draw_text(screen, "SCORE " + str(score), 200, 30, 50, Image.SILVER)
        if idx != 0:  # 실드 표시
            screen.blit(Image.img_shield, [40, 680])
            pygame.draw.rect(screen, (64, 32, 32), [40 + ss_shield * 4, 680, (100 - ss_shield) * 4, 12])

        pygame.display.update()
        clock.tick(30)
        
if __name__ == '__main__':
    main()