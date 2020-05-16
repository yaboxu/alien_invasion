import pygame
from pygame.sprite import Group

from settings import Settings #从模块导入类
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf #导入模块，别称

def run_game():
    """初始化游戏并创建一个屏幕对象"""
    pygame.init() #句点表示法.方法()
    ai_settings = Settings() #创建实例，并存储在变量ai_settings中
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)) #screen，游戏窗口大小
    pygame.display.set_caption("Alien Invasion")
    
    #创建Play按钮
    play_button = Button(screen, "Play")
    
    #创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats) #stats是计分板类的形参###注意位置
    
    #创建一艘飞船、一个外星人编组、一个用于存储子弹的编组
    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()
    
    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    #开始游戏主循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        
        if stats.game_active: 
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, 
            bullets, play_button)
        
run_game()
