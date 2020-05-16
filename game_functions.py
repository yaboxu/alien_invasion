import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, aliens): 
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        #设置移动标志
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:    
        start_game(ai_settings, stats, sb, aliens, bullets, screen, ship)

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    #创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
            
def check_keyup_events(event, ship):
    """响应松键"""
    if event.key == pygame.K_RIGHT:
        #设置移动标志
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets): 
    """监视键盘和鼠标事件"""
    for event in pygame.event.get(): #event首次出现在这里，所以不作为函数check_events()的形参
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN: #按键
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, aliens)
        elif event.type == pygame.KEYUP: #松键
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                bullets, mouse_x, mouse_y)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, 
        bullets, mouse_x, mouse_y):
    """玩家单击PLAY按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active: #玩家单击PLAY按钮且游戏处于非活动状态
        start_game(ai_settings, stats, sb, aliens, bullets, screen, ship)
        
def start_game(ai_settings, stats, sb, aliens, bullets, screen, ship):
    """开始游戏""" 
    #重置游戏的动态设置       
    ai_settings.initialize_dynamic_settings()
    
    #隐藏光标
    pygame.mouse.set_visible(False)
    
    #重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    
    #重置记分牌(初始得分和最高得分)、等级、飞船图像###
    sb.prep_images()
    
    #清空外星人编组和子弹编组
    aliens.empty()
    bullets.empty()
    
    #创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
     
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环都重绘屏幕  
    screen.fill(ai_settings.bg_color)
    
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    ship.blitme()
    aliens.draw(screen)
    
    #显示得分
    sb.show_score()
    
    #如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
          
    #不断更新屏幕
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    #更新子弹的位置
    bullets.update()
    
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets)) #确认删除，记得注释，否则占内存
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):    
    """如果有子弹击中外星人，就删除相应的子弹和外星人"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) #两个编组
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
        
    #如果整群外星人都被消灭，开始新等级
    if len(aliens) == 0:    
        start_new_level(aliens, bullets, ai_settings, stats, sb, screen, ship)
    
def start_new_level(aliens, bullets, ai_settings, stats, sb, screen, ship):
    """开始新等级：删除现有的子弹，加快游戏节奏，提高一个等级，新建外星人群"""
    bullets.empty()
    ai_settings.increase_speed()
    stats.level += 1
    sb.prep_level()
    create_fleet(ai_settings, screen, ship, aliens)

def check_high_score(stats, sb):
    """检查是否产生了最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def get_number_aliens_x(ai_settings, alien_width):
    """计算一行可容纳多少个外星人"""
    availabel_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(availabel_space_x / (2 * alien_width))
    return number_aliens_x
    
def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""  
    availabel_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(availabel_space_y / (2 * alien_height))
    return number_rows  
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人，并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width #外星人间距为外星人宽度
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)    

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    #创建一个外星人，并计算一行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """若外星人碰到左边缘或右边缘，向下移动并改变方向"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            
def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        #将ships_left减1
        stats.ships_left -= 1
        
        #更新记分牌
        sb.prep_ships()
        
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        
        #创建一群新的外星人，并将飞船放在屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True) #游戏为非活动状态时，使光标可见

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被外星人撞到一样处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
    
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘，更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
