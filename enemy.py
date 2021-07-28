import pygame
import math
import os
from settings import PATH, PATH_2

pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))
# 宣告global變數path_lr 用來決定路線左或路線右
path_lr = list(PATH)


class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        self.path = path_lr  # 將路線左或右賦予給path
        self.path_index = 0
        self.move_count = 0
        self.stride = 1
        self.x, self.y = self.path[0]

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        # 用self.x, self.y 當座標讓血條跟著enemy
        pygame.draw.rect(win, (255, 0, 0), [self.x-20, self.y-30, self.max_health*4, 5])
        pygame.draw.rect(win, (0, 255, 0), [self.x-20, self.y-30, self.health*4, 5])

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        ax, ay = self.path[self.path_index]  # x, y position of point A
        bx, by = self.path[self.path_index+1]
        distance_a_b = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
        max_count = int(distance_a_b / self.stride)  # total footsteps that needed from A to B

        # 當抵達當前設定的點後，將index+1並且步數歸零
        if max_count == self.move_count:
            self.path_index += 1
            self.move_count = 0

        if self.move_count < max_count:
            unit_vector_x = (bx - ax) / distance_a_b
            unit_vector_y = (by - ay) / distance_a_b
            delta_x = unit_vector_x * self.stride
            delta_y = unit_vector_y * self.stride

            # update the coordinate and the counter
            self.x += delta_x
            self.y += delta_y
            self.move_count += 1


class EnemyGroup:
    def __init__(self):
        self.left_right = 0  # 用來決定路線左或右
        self.campaign_count = 0
        self.campaign_max_count = 120   # (unit: frame)
        self.reserved_members = []
        self.expedition = []  # don't change this line until you do the EX.3

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        # 每過120禎 且 尚有保留的敵人 就生產敵人並消耗掉一個保留敵人
        if self.campaign_count % self.campaign_max_count == 0 and len(self.reserved_members) != 0:
            self.expedition.append(Enemy())
            self.reserved_members.pop()
        # 用來計經過時間(禎數)
        self.campaign_count += 1

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        # 經過時間先歸零並增加num個保留敵人
        self.campaign_count = 0
        for i in range(num):
            self.reserved_members.append(Enemy())
        # 輪流令path_lr為左、右路線
        global path_lr
        if self.left_right % 2 == 1:
            path_lr = list(PATH_2)
        else:
            path_lr = list(PATH)
        self.left_right += 1

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)
