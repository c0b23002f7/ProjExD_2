import os
import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def kk_img0(kk_img: pg.Rect) -> tuple[bool]:
    """
    引数：こうかとんimg
    戻り値：辞書の値
    """
    KAITEN = {
        (0, -5):pg.transform.rotozoom(kk_img, 90, 1.0), # 上
        (+5, -5):pg.transform.rotozoom(kk_img, 45, 1.0), # 右上
        (+5, 0):pg.transform.rotozoom(kk_img, 180, 1.0), # 反転
        (+5, +5):pg.transform.rotozoom(kk_img, -45, 1.0), # 右下
        (0, +5):pg.transform.rotozoom(kk_img, -90, 1.0), # 下
        (-5, +5):pg.transform.rotozoom(kk_img, -45, 1.0), # 左下
        (-5, 0):pg.transform.rotozoom(kk_img, 0, 1.0), # 左
        (-5, -5):pg.transform.rotozoom(kk_img, 45, 1.0), # 左上
        }
    return KAITEN


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect、または、爆弾Rect
    戻り値：真理値タプル（横方向、縦方向）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or 800 < rct.right:
        yoko = False
    if rct.top < 0 or 600 < rct.bottom:
        tate = False
    return yoko, tate 
    


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 400, 300
    enn = pg.Surface((20, 20)) # 1辺が20の空のSurfaceを作る
    pg.draw.circle(enn, (255, 0, 0), (10, 10), 10)
    enn.set_colorkey((0, 0, 0))
    bb_rct = enn.get_rect()
    bb_rct.center = random.randint(0, 800), random.randint(0, 600)
    vx, vy = +5, +5  # 爆弾の速度
    kk_imgs = kk_img0()
    kk_img = kk_imgs[tuple(sum_mv)]
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        kk_img = kk_imgs[tuple(sum_mv)]
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(enn, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
