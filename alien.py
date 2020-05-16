import pygame
from pygame.sprite import Sprite #从模块中导入类

class Alien(Sprite): #子类继承父类
    """表示单个外星人的类"""
    
    def __init__(self, ai_settings, screen):
        """初始化外星人，并设置其初始位置"""
        super().__init__() #初始化父类属性值
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载外星人图像，并获取其外接矩形
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect() #外星人图像外接矩形
        
        #将外星人放在屏幕左上方，设置左边距和上边距
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #存储外星人的准确位置
        self.x = float(self.rect.x)
        #self.y = float(self.rect.y) #外星人的y值不是连续变化的，而是以5向下移动，不需要准确
        
    def blitme(self):
        """在屏幕指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)
    
    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    
    def update(self):
        """向左或向右移动外星人"""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x
