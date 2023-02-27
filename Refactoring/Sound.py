import pygame

global se_barrage, se_damage, se_explosion, se_shot, se_bgm, se_gameover, se_gameclear

pygame.init()

# SE 로딩 변수
se_barrage = None  #탄막 발사시 사용
se_damage = None #데미지 입을 때 사용
se_explosion = None #보스 폭발시 사용
se_shot = None #탄환 발사시 사용
se_bgm = None #배경음악
se_gameover = None
se_gameclear = None


se_barrage = pygame.mixer.Sound("sound_gl/barrage.ogg")
se_damage = pygame.mixer.Sound("sound_gl/damage.ogg")
se_explosion = pygame.mixer.Sound("sound_gl/explosion.ogg")
se_shot = pygame.mixer.Sound("sound_gl/shot.ogg")
se_bgm = pygame.mixer.Sound("sound_gl/bgm.ogg") #BGM 로딩
se_gameover = pygame.mixer.Sound("sound_gl/gameover.ogg")
se_gameclear = pygame.mixer.Sound("sound_gl/gameclear.ogg")