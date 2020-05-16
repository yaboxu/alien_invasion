import pygame
from pygame.sprite import Sprite

class Ship(Sprite): #子类继承父类
    """表示飞船的类"""
    def __init__(self, ai_settings, screen):
        """初始化飞船，并设置其初始位置"""
        super().__init__() #初始化父类属性
        self.screen = screen
        self.ai_settings = ai_settings
        #加载飞船图像，并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect() #飞船图像外接矩形 rectangular，不准确值
        self.screen_rect = screen.get_rect() #表示屏幕的矩形
        
        #将飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        #在飞船的属性center中存储小数，准确值
        self.center = float(self.rect.centerx)
        
        #移动标志
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """根据移动标志调整飞船的位置"""
        #更新飞船的self.center值，而不是self.rect.centerx
        if self.moving_right and (self.rect.right < self.screen_rect.right):
           self.center += self.ai_settings.ship_speed_factor 
        if self.moving_left and (self.rect.left > 0):
           self.center -= self.ai_settings.ship_speed_factor 
           
        #根据self.center更新飞船位置的self.rect.centerx
        self.rect.centerx = self.center #self.rect.centerx只存储self.center的整数部分

    def blitme(self):
        """在屏幕指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
