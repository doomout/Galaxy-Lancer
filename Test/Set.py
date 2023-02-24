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