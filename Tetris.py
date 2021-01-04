import pygame
import os
from random import randint
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT)


    
class Piece(pygame.sprite.Sprite):
    def __init__(self):
        super(Piece, self).__init__()
        self.surf = pygame.image.load(os.getcwd()+r"\Ressources\Tetris_Piece.png").convert()
        self.rect = self.surf.get_rect(x=200, y=0)
        

class Straight(Piece):
    def __init__(self, class_piece):
        self.surf = class_piece.surf
        self.rect = class_piece.rect
        self.body = [[self.rect[0], self.rect[1]-40], [self.rect[0], self.rect[1]-80], [self.rect[0], self.rect[1]-120]]

    def coll_detect(self):
        if self.rect.left < 0:
            self.rect.move_ip(40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] += 40
        if self.rect.right > screen_width:
            self.rect.move_ip(-40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] -= 40
        if self.body[2][0] > screen_width-40:
            self.rect.move_ip(-40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] -= 40
        if [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces or self.rect.bottom == screen_height:
            pasted_pieces.append([self.rect.x, self.rect.y])
            for body in self.body:
                pasted_pieces.append(body)
            pygame.event.post(new_piece)
        
        security_check()
        same_numbers = []    
        for coord in pasted_pieces:   
            same_numbers.append(coord[1])
        count_max(same_numbers)

    def falling_piece(self):
        if self.rect.bottom >= screen_height:
            pygame.time.set_timer(FALLINGPIECE, 0)
        else:
            self.rect.move_ip(0, 40)
            for index, body in enumerate(self.body):
                self.body[index][1] += 40

    def rotate_piece(self):
        x_coordinates = []
        y_coordinates = []
        for body in self.body:
            x_coordinates.append(body[0])
            y_coordinates.append(body[1])
        
        if len(set(x_coordinates)) == 1:
            self.rect.move_ip(-40, -40)
            self.body[1][0] += 40
            self.body[1][1] += 40
            self.body[2][0] += 80
            self.body[2][1] += 80
            
            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(40, 40)
                self.body[1][0] -= 40
                self.body[1][1] -= 40
                self.body[2][0] -= 80
                self.body[2][1] -= 80
            
        elif len(set(y_coordinates)) == 1:
            self.rect.move_ip(40, 40)
            self.body[1][0] -= 40
            self.body[1][1] -= 40
            self.body[2][0] -= 80
            self.body[2][1] -= 80
            
            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(-40, -40)
                self.body[1][0] += 40
                self.body[1][1] += 40
                self.body[2][0] += 80
                self.body[2][1] += 80

    def move_piece(self, pressed_key):
        if pressed_key == K_DOWN:
            if self.rect.bottom >= screen_height or [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces:
                return
            else:
                self.rect.move_ip(0, 40)
                for index, body in enumerate(self.body):
                    self.body[index][1] += 40
        if pressed_key == K_LEFT:
            if [self.rect.x-40, self.rect.y] in pasted_pieces or [self.body[0][0]-40, self.body[0][1]] in pasted_pieces or [self.body[1][0]-40, self.body[1][1]] in pasted_pieces or [self.body[2][0]-40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(-40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] -= 40
        if pressed_key == K_RIGHT:
            if [self.rect.x+40, self.rect.y] in pasted_pieces or [self.body[0][0]+40, self.body[0][1]] in pasted_pieces or [self.body[1][0]+40, self.body[1][1]] in pasted_pieces or [self.body[2][0]+40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] += 40


class Cube(Piece):
    def __init__(self, class_piece):
        self.surf = class_piece.surf
        self.rect = class_piece.rect
        self.body = [[self.rect[0]+40, self.rect[1]], [self.rect[0], self.rect[1]-40], [self.rect[0]+40, self.rect[1]-40]]

    def coll_detect(self):
        if self.rect.left < 0:
            self.rect.move_ip(40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] += 40
        if self.body[0][0] > screen_width-40:
            self.rect.move_ip(-40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] -= 40
        if [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or self.rect.bottom == screen_height:
            pasted_pieces.append([self.rect.x, self.rect.y])
            for body in self.body:
                pasted_pieces.append(body)
            pygame.event.post(new_piece)
        
        security_check()
        same_numbers = []    
        for coord in pasted_pieces:   
            same_numbers.append(coord[1])
        count_max(same_numbers)

    def rotate_piece(self):
        return

    def falling_piece(self):
        if self.rect.bottom >= screen_height:
            pygame.time.set_timer(FALLINGPIECE, 0)
        else:
            self.rect.move_ip(0, 40)
            for index, body in enumerate(self.body):
                self.body[index][1] += 40

    def move_piece(self, pressed_key):
        if pressed_key == K_DOWN:
            if self.rect.bottom >= screen_height or [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces:
                return
            else:
                self.rect.move_ip(0, 40)
                for index, body in enumerate(self.body):
                    self.body[index][1] += 40
        if pressed_key == K_LEFT:
            if [self.rect.x-40, self.rect.y] in pasted_pieces or [self.body[1][0]-40, self.body[1][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(-40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] -= 40
        if pressed_key == K_RIGHT:
            if [self.body[0][0]+40, self.body[0][1]] in pasted_pieces or [self.body[2][0]+40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] += 40


class L_Shape(Piece):
    def __init__(self, class_piece):
        self.surf = class_piece.surf
        self.rect = class_piece.rect
        self.body = [[self.rect[0], self.rect[1]-40], [self.rect[0]+40, self.rect[1]-40], [self.rect[0]+80, self.rect[1]-40]]

    def coll_detect(self):
        if self.rect.left < 0 or self.body[2][0] < 0:
            self.rect.move_ip(40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] += 40
        if self.rect.right > screen_width or self.body[2][0] > screen_width-40:
            self.rect.move_ip(-40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] -= 40
        if [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces or self.rect.bottom == screen_height or self.body[2][1]+40 == screen_height:
            pasted_pieces.append([self.rect.x, self.rect.y])
            for body in self.body:
                pasted_pieces.append(body)
            pygame.event.post(new_piece)
        
        security_check()
        same_numbers = []    
        for coord in pasted_pieces:   
            same_numbers.append(coord[1])
        count_max(same_numbers)            

    def falling_piece(self):
        if self.rect.bottom == screen_height or self.body[2][1]+40 == screen_height:
            pygame.time.set_timer(FALLINGPIECE, 0)
        else:
            self.rect.move_ip(0, 40)
            for index, body in enumerate(self.body):
                self.body[index][1] += 40

    def rotate_piece(self):        
        x_coordinates = []
        y_coordinates = []
        for body in self.body:
            x_coordinates.append(body[0])
            y_coordinates.append(body[1])
        
        if len(set(y_coordinates)) == 1 and self.rect.y > self.body[0][1]:
            self.rect.move_ip(0, -80)
            self.body[0][0] += 40
            self.body[0][1] -= 40
            self.body[2][0] -= 40
            self.body[2][1] += 40
            
            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(0, +80)
                self.body[0][0] -= 40
                self.body[0][1] += 40
                self.body[2][0] += 40
                self.body[2][1] -= 40
        
        elif len(set(x_coordinates)) == 1 and self.rect.x < self.body[0][0]:
            self.rect.move_ip(80, 0)
            self.body[0][0] += 40
            self.body[0][1] += 40
            self.body[2][0] -= 40
            self.body[2][1] -= 40

            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(-80, 0)
                self.body[0][0] -= 40
                self.body[0][1] -= 40
                self.body[2][0] += 40
                self.body[2][1] += 40
                
        elif len(set(y_coordinates)) == 1 and self.rect.y < self.body[0][1]:
            self.rect.move_ip(0, 80)
            self.body[0][0] -= 40
            self.body[0][1] += 40
            self.body[2][0] += 40
            self.body[2][1] -= 40

            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(0, -80)
                self.body[0][0] += 40
                self.body[0][1] -= 40
                self.body[2][0] -= 40
                self.body[2][1] += 40
                
        elif len(set(x_coordinates)) == 1 and self.rect.x > self.body[0][0]:
            self.rect.move_ip(-80, 0)
            self.body[0][0] -= 40
            self.body[0][1] -= 40
            self.body[2][0] += 40
            self.body[2][1] += 40

            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(80, 0)
                self.body[0][0] += 40
                self.body[0][1] += 40
                self.body[2][0] -= 40
                self.body[2][1] -= 40
                
    def move_piece(self, pressed_key):
        if pressed_key == K_DOWN:
            if self.rect.bottom == screen_height or self.body[2][1]+40 == screen_height or [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces:
                return
            else:
                self.rect.move_ip(0, 40)
                for index, body in enumerate(self.body):
                    self.body[index][1] += 40
        if pressed_key == K_LEFT:
            if [self.rect.x-40, self.rect.y] in pasted_pieces or [self.body[0][0]-40, self.body[0][1]] in pasted_pieces or [self.body[1][0]-40, self.body[1][1]] in pasted_pieces or [self.body[2][0]-40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(-40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] -= 40
        if pressed_key == K_RIGHT:
            if [self.rect.x+40, self.rect.y] in pasted_pieces or [self.body[0][0]+40, self.body[0][1]] in pasted_pieces or [self.body[1][0]+40, self.body[1][1]] in pasted_pieces or [self.body[2][0]+40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] += 40


class Reverse_L(Piece):
    def __init__(self, class_piece):
        self.surf = class_piece.surf
        self.rect = class_piece.rect
        self.body = [[self.rect[0], self.rect[1]+40], [self.rect[0]+40, self.rect[1]+40], [self.rect[0]+80, self.rect[1]+40]]

    def coll_detect(self):
        if self.rect.left < 0 or self.body[2][0] < 0:
            self.rect.move_ip(40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] += 40
        if self.rect.right > screen_width or self.body[2][0] > screen_width-40:
            self.rect.move_ip(-40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] -= 40
        if [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces or self.rect.bottom == screen_height or self.body[2][1]+40 == screen_height:
            pasted_pieces.append([self.rect.x, self.rect.y])
            for body in self.body:
                pasted_pieces.append(body)
            pygame.event.post(new_piece)
        
        security_check()
        same_numbers = []    
        for coord in pasted_pieces:   
            same_numbers.append(coord[1])
        count_max(same_numbers)            

    def falling_piece(self):
        if self.rect.bottom == screen_height or self.body[2][1]+40 == screen_height:
            pygame.time.set_timer(FALLINGPIECE, 0)
        else:
            self.rect.move_ip(0, 40)
            for index, body in enumerate(self.body):
                self.body[index][1] += 40

    def rotate_piece(self):        
        x_coordinates = []
        y_coordinates = []
        for body in self.body:
            x_coordinates.append(body[0])
            y_coordinates.append(body[1])
        
        if len(set(y_coordinates)) == 1 and self.rect.y < self.body[0][1]:
            self.rect.move_ip(80, 0)
            self.body[0][0] += 40
            self.body[0][1] -= 40
            self.body[2][0] -= 40
            self.body[2][1] += 40
            
            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(-80, 0)
                self.body[0][0] -= 40
                self.body[0][1] += 40
                self.body[2][0] += 40
                self.body[2][1] -= 40
        
        elif len(set(x_coordinates)) == 1 and self.rect.x > self.body[0][0]:
            self.rect.move_ip(0, 80)
            self.body[0][0] += 40
            self.body[0][1] += 40
            self.body[2][0] -= 40
            self.body[2][1] -= 40

            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(0, -80)
                self.body[0][0] -= 40
                self.body[0][1] -= 40
                self.body[2][0] += 40
                self.body[2][1] += 40
                
        elif len(set(y_coordinates)) == 1 and self.rect.y > self.body[0][1]:
            self.rect.move_ip(-80, 0)
            self.body[0][0] -= 40
            self.body[0][1] += 40
            self.body[2][0] += 40
            self.body[2][1] -= 40

            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(80, 0)
                self.body[0][0] += 40
                self.body[0][1] -= 40
                self.body[2][0] -= 40
                self.body[2][1] += 40
                
        elif len(set(x_coordinates)) == 1 and self.rect.x < self.body[0][0]:
            self.rect.move_ip(0, -80)
            self.body[0][0] -= 40
            self.body[0][1] -= 40
            self.body[2][0] += 40
            self.body[2][1] += 40

            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(0, 80)
                self.body[0][0] += 40
                self.body[0][1] += 40
                self.body[2][0] -= 40
                self.body[2][1] -= 40
                
    def move_piece(self, pressed_key):
        if pressed_key == K_DOWN:
            if self.rect.bottom == screen_height or self.body[2][1]+40 == screen_height or [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces:
                return
            else:
                self.rect.move_ip(0, 40)
                for index, body in enumerate(self.body):
                    self.body[index][1] += 40
        if pressed_key == K_LEFT:
            if [self.rect.x-40, self.rect.y] in pasted_pieces or [self.body[0][0]-40, self.body[0][1]] in pasted_pieces or [self.body[1][0]-40, self.body[1][1]] in pasted_pieces or [self.body[2][0]-40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(-40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] -= 40
        if pressed_key == K_RIGHT:
            if [self.rect.x+40, self.rect.y] in pasted_pieces or [self.body[0][0]+40, self.body[0][1]] in pasted_pieces or [self.body[1][0]+40, self.body[1][1]] in pasted_pieces or [self.body[2][0]+40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] += 40
                    

class S_Shape(Piece):
    def __init__(self, class_piece):
        self.surf = class_piece.surf
        self.rect = class_piece.rect
        self.body = [[self.rect[0]+40, self.rect[1]], [self.rect[0]+40, self.rect[1]-40], [self.rect[0]+80, self.rect[1]-40]]

    def coll_detect(self):
        if self.rect.left < 0:
            self.rect.move_ip(40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] += 40
        if self.body[2][0] > screen_width-40:
            self.rect.move_ip(-40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] -= 40
        if [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces or self.rect.bottom == screen_height or self.body[2][1]+40 == screen_height:
            pasted_pieces.append([self.rect.x, self.rect.y])
            for body in self.body:
                pasted_pieces.append(body)
            pygame.event.post(new_piece)
        
        security_check()
        same_numbers = []    
        for coord in pasted_pieces:   
            same_numbers.append(coord[1])
        count_max(same_numbers)
            
    def falling_piece(self):
        if self.rect.bottom == screen_height or self.body[2][1]+40 == screen_height:
            pygame.time.set_timer(FALLINGPIECE, 0)
        else:
            self.rect.move_ip(0, 40)
            for index, body in enumerate(self.body):
                self.body[index][1] += 40

    def rotate_piece(self):        
        x_coordinates = []
        y_coordinates = []
        for body in self.body:
            x_coordinates.append(body[0])
            y_coordinates.append(body[1])
        
        if self.rect.y == self.body[0][1]:
            self.rect.move_ip(0, -80)
            self.body[0][0] -= 40
            self.body[0][1] -= 40
            self.body[2][0] -= 40
            self.body[2][1] += 40
            
            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(0, 80)
                self.body[0][0] += 40
                self.body[0][1] += 40
                self.body[2][0] += 40
                self.body[2][1] -= 40
        
        elif self.rect.x == self.body[0][0]:
            self.rect.move_ip(0, 80)
            self.body[0][0] += 40
            self.body[0][1] += 40
            self.body[2][0] += 40
            self.body[2][1] -= 40
            
            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(0, -80)
                self.body[0][0] -= 40
                self.body[0][1] -= 40
                self.body[2][0] -= 40
                self.body[2][1] += 40                

    def move_piece(self, pressed_key):
        if pressed_key == K_DOWN:
            if self.rect.bottom == screen_height or self.body[2][1]+40 == screen_height or [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces:
                return
            else:
                self.rect.move_ip(0, 40)
                for index, body in enumerate(self.body):
                    self.body[index][1] += 40
        if pressed_key == K_LEFT:
            if [self.rect.x-40, self.rect.y] in pasted_pieces or [self.body[0][0]-40, self.body[0][1]] in pasted_pieces or [self.body[1][0]-40, self.body[1][1]] in pasted_pieces or [self.body[2][0]-40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(-40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] -= 40
        if pressed_key == K_RIGHT:
            if [self.rect.x+40, self.rect.y] in pasted_pieces or [self.body[0][0]+40, self.body[0][1]] in pasted_pieces or [self.body[1][0]+40, self.body[1][1]] in pasted_pieces or [self.body[2][0]+40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] += 40


class Reverse_S(Piece):
    def __init__(self, class_piece):
        self.surf = class_piece.surf
        self.rect = class_piece.rect
        self.body = [[self.rect[0]+40, self.rect[1]], [self.rect[0]+40, self.rect[1]+40], [self.rect[0]+80, self.rect[1]+40]]

    def coll_detect(self):
        if self.rect.left < 0 or self.body[2][0] < 0:
            self.rect.move_ip(40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] += 40
        if self.rect.right > screen_width or self.body[2][0] > screen_width-40:
            self.rect.move_ip(-40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] -= 40
        if [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces or self.body[2][1]+40 == screen_height:
            pasted_pieces.append([self.rect.x, self.rect.y])
            for body in self.body:
                pasted_pieces.append(body)
            pygame.event.post(new_piece)
        
        security_check()
        same_numbers = []    
        for coord in pasted_pieces:   
            same_numbers.append(coord[1])
        count_max(same_numbers)            

    def falling_piece(self):
        if self.body[2][1]+40 == screen_height:
            pygame.time.set_timer(FALLINGPIECE, 0)
        else:
            self.rect.move_ip(0, 40)
            for index, body in enumerate(self.body):
                self.body[index][1] += 40

    def rotate_piece(self):        
        x_coordinates = []
        y_coordinates = []
        for body in self.body:
            x_coordinates.append(body[0])
            y_coordinates.append(body[1])
        
        if self.rect.y == self.body[0][1]:
            self.rect.move_ip(80, 0)
            self.body[0][0] += 40
            self.body[0][1] += 40
            self.body[2][0] -= 40
            self.body[2][1] += 40
            
            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(-80, 0)
                self.body[0][0] -= 40
                self.body[0][1] -= 40
                self.body[2][0] += 40
                self.body[2][1] -= 40
        
        elif self.rect.x == self.body[0][0]:
            self.rect.move_ip(-80, 0)
            self.body[0][0] -= 40
            self.body[0][1] -= 40
            self.body[2][0] += 40
            self.body[2][1] -= 40
            
            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(80, 0)
                self.body[0][0] += 40
                self.body[0][1] += 40
                self.body[2][0] -= 40
                self.body[2][1] += 40

    def move_piece(self, pressed_key):
        if pressed_key == K_DOWN:
            if self.body[2][1]+40 == screen_height or [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces:
                return
            else:
                self.rect.move_ip(0, 40)
                for index, body in enumerate(self.body):
                    self.body[index][1] += 40
        if pressed_key == K_LEFT:
            if [self.rect.x-40, self.rect.y] in pasted_pieces or [self.body[0][0]-40, self.body[0][1]] in pasted_pieces or [self.body[1][0]-40, self.body[1][1]] in pasted_pieces or [self.body[2][0]-40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(-40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] -= 40
        if pressed_key == K_RIGHT:
            if [self.rect.x+40, self.rect.y] in pasted_pieces or [self.body[0][0]+40, self.body[0][1]] in pasted_pieces or [self.body[1][0]+40, self.body[1][1]] in pasted_pieces or [self.body[2][0]+40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] += 40


class T_Shape(Piece):
    def __init__(self, class_piece):
        self.surf = class_piece.surf
        self.rect = class_piece.rect
        self.body = [[self.rect[0]-40, self.rect[1]-40], [self.rect[0], self.rect[1]-40], [self.rect[0]+40, self.rect[1]-40]]

    def coll_detect(self):
        if self.rect.left < 0 or self.body[0][0] < 0 or self.body[2][0] < 0:
            self.rect.move_ip(40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] += 40
        if self.rect.right > screen_width or self.body[0][0] > screen_width-40 or self.body[2][0] > screen_width-40:
            self.rect.move_ip(-40, 0)
            for index, body in enumerate(self.body):
                self.body[index][0] -= 40
        if [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces or self.rect.bottom == screen_height or self.body[0][1]+40 == screen_height or self.body[2][1]+40 == screen_height:
            pasted_pieces.append([self.rect.x, self.rect.y])
            for body in self.body:
                pasted_pieces.append(body)
            pygame.event.post(new_piece)
        
        security_check()
        same_numbers = []    
        for coord in pasted_pieces:   
            same_numbers.append(coord[1])
        count_max(same_numbers)
            
    def falling_piece(self):
        if self.rect.bottom == screen_height or self.body[0][1]+40 == screen_height or self.body[2][1]+40 == screen_height:
            pygame.time.set_timer(FALLINGPIECE, 0)
        else:
            self.rect.move_ip(0, 40)
            for index, body in enumerate(self.body):
                self.body[index][1] += 40

    def rotate_piece(self):        
        x_coordinates = []
        y_coordinates = []
        for body in self.body:
            x_coordinates.append(body[0])
            y_coordinates.append(body[1])
        
        if len(set(y_coordinates)) == 1 and self.rect.y > self.body[1][1]:
            self.rect.move_ip(-40, -40)
            self.body[0][0] += 40
            self.body[0][1] -= 40
            self.body[2][0] -= 40
            self.body[2][1] += 40
            
            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(40, 40)
                self.body[0][0] -= 40
                self.body[0][1] += 40
                self.body[2][0] += 40
                self.body[2][1] -= 40
        
        elif len(set(x_coordinates)) == 1 and self.rect.x < self.body[1][0]:
            self.rect.move_ip(40, -40)
            self.body[0][0] += 40
            self.body[0][1] += 40
            self.body[2][0] -= 40
            self.body[2][1] -= 40

            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(-40, 40)
                self.body[0][0] -= 40
                self.body[0][1] -= 40
                self.body[2][0] += 40
                self.body[2][1] += 40
                
        elif len(set(y_coordinates)) == 1 and self.rect.y < self.body[1][1]:
            self.rect.move_ip(40, 40)
            self.body[0][0] -= 40
            self.body[0][1] += 40
            self.body[2][0] += 40
            self.body[2][1] -= 40

            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(-40, -40)
                self.body[0][0] += 40
                self.body[0][1] -= 40
                self.body[2][0] -= 40
                self.body[2][1] += 40
                
        elif len(set(x_coordinates)) == 1 and self.rect.x > self.body[0][0]:
            self.rect.move_ip(-40, 40)
            self.body[0][0] -= 40
            self.body[0][1] -= 40
            self.body[2][0] += 40
            self.body[2][1] += 40

            if [self.rect.x, self.rect.y] in pasted_pieces or [self.body[0][0], self.body[0][1]] in pasted_pieces or [self.body[1][0], self.body[1][1]] in pasted_pieces or [self.body[2][0], self.body[2][1]] in pasted_pieces:
                self.rect.move_ip(40, -40)
                self.body[0][0] += 40
                self.body[0][1] += 40
                self.body[2][0] -= 40
                self.body[2][1] -= 40
                
    def move_piece(self, pressed_key):
        if pressed_key == K_DOWN:
            if self.rect.bottom == screen_height or self.body[0][1]+40 == screen_height or self.body[2][1]+40 == screen_height or [self.rect.x, self.rect.y+40] in pasted_pieces or [self.body[0][0], self.body[0][1]+40] in pasted_pieces or [self.body[1][0], self.body[1][1]+40] in pasted_pieces or [self.body[2][0], self.body[2][1]+40] in pasted_pieces:
                return
            else:
                self.rect.move_ip(0, 40)
                for index, body in enumerate(self.body):
                    self.body[index][1] += 40
        if pressed_key == K_LEFT:
            if [self.rect.x-40, self.rect.y] in pasted_pieces or [self.body[0][0]-40, self.body[0][1]] in pasted_pieces or [self.body[1][0]-40, self.body[1][1]] in pasted_pieces or [self.body[2][0]-40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(-40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] -= 40
        if pressed_key == K_RIGHT:
            if [self.rect.x+40, self.rect.y] in pasted_pieces or [self.body[0][0]+40, self.body[0][1]] in pasted_pieces or [self.body[1][0]+40, self.body[1][1]] in pasted_pieces or [self.body[2][0]+40, self.body[2][1]] in pasted_pieces:
                return
            else:
                self.rect.move_ip(40, 0)
                for index, body in enumerate(self.body):
                    self.body[index][0] += 40
                                                    

def new_object():
    random_number = randint(1, 1000)
    if random_number in range(1, 138):
        new_object = Straight(piece)
    elif random_number in range(138, 276):
        new_object = Reverse_S(piece)
    elif random_number in range(276, 383):
        new_object = L_Shape(piece)
    elif random_number in range(383, 521):
        new_object = Reverse_L(piece)
    elif random_number in range(521, 683):
        new_object = S_Shape(piece)
    elif random_number in range(683, 845):
        new_object = Cube(piece)
    elif random_number in range(845, 1001):
        new_object = T_Shape(piece)
    return new_object
    

def security_check():
    for index, coord in enumerate(pasted_pieces):
        piece_count = pasted_pieces.count(coord)
        if piece_count > 1:
            del pasted_pieces[index]
    
        
def count_max(input_list):
    result_list = []
    position_list = []
    compressed_list = set(input_list)
    for number in compressed_list:
        var = input_list.count(number)
        result_list.append(var)
        position_list.append(number)
    var2 = max(result_list) if result_list else 0
    if var2 == 10:
        var3 = position_list[result_list.index(var2)]
        for number in range(0, 400, 40):
            pasted_pieces.remove([number, var3])
        for index, piece in enumerate(pasted_pieces):
            if pasted_pieces[index][1] < var3:
                pasted_pieces[index][1] += 40
        point_counter()


def point_counter():
    global points
    points += 100



pygame.init()

base_screen = pygame.display.set_mode((700, 640))
stone_walls = pygame.image.load(os.getcwd()+r"\Ressources\Stone_Walls.png").convert()

tetris_font = pygame.font.Font(pygame.font.get_default_font(), 40)
tetris_text = tetris_font.render('TETRIS', True, (211,211,211))

score_font = pygame.font.Font(pygame.font.get_default_font(), 20)
score_text = score_font.render('SCORE', True, (211,211,211))

points = 0


screen_width = 400
screen_height = 600

screen = pygame.surface.Surface((screen_width, screen_height))

pasted_pieces = []

FALLINGPIECE = pygame.USEREVENT + 1
pygame.time.set_timer(FALLINGPIECE, 700)

NEWPIECE = pygame.USEREVENT + 2
new_piece = pygame.event.Event(NEWPIECE)

piece = Piece()
current_piece = new_object()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
                current_piece.move_piece(event.key)
            if event.key == K_UP:
                current_piece.rotate_piece()
        elif event.type == FALLINGPIECE:
            current_piece.falling_piece()
        elif event.type == NEWPIECE:
            piece = Piece()
            current_piece = new_object()
            pygame.time.set_timer(FALLINGPIECE, 700)
            
    points_text = score_font.render(str(points), True, (211,211,211))
    base_screen.fill((0,0,0))
    screen.fill((211,211,211))
    
    screen.blit(current_piece.surf, current_piece.rect)
    for body in current_piece.body:
        screen.blit(current_piece.surf, body)    

    for pasted in pasted_pieces:
        screen.blit(current_piece.surf, pasted)
        
    base_screen.blit(stone_walls, (0,0))
    base_screen.blit(screen, (40,0))
    base_screen.blit(tetris_text, dest=(515,20))
    base_screen.blit(score_text, dest=(515, 100))
    base_screen.blit(points_text, dest=(515, 130))
    
    current_piece.coll_detect()

    pygame.display.flip()
    
    clock.tick(60)
