import pygame
from pygame.locals import *



# SE 로딩 변수
se_barrage = None  #탄막 발사시 사용
se_damage = None #데미지 입을 때 사용
se_explosion = None #보스 폭발시 사용
se_shot = None #탄환 발사시 사용

pygame.init()

se_barrage = pygame.mixer.Sound("sound_gl/barrage.ogg")
se_damage = pygame.mixer.Sound("sound_gl/damage.ogg")
se_explosion = pygame.mixer.Sound("sound_gl/explosion.ogg")
se_shot = pygame.mixer.Sound("sound_gl/shot.ogg")