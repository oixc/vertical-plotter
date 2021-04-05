# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:52:37 2021

@author: oixc
"""

import numpy as np
from util import command_dict
import svgwrite

def height_of_triangle(a, b, c):
    s = (a + b + c) / 2.0
    area = np.sqrt(s * (s - a) * (s - b) * (s - c))  # Heron's Formula
    h = area / (0.5 * c)  # height of triangle with base c
    return h

def find_pen_position(s1, s2, width):
    y = height_of_triangle(s1, s2, width)
    # s1^2 = y^2 + x^2
    x = np.sqrt(abs((s1 ** 2) - (y ** 2)))
    return x, y

def line_tensions(angle1, angle2):
    d = np.cos(angle1) * np.sin(angle2) + np.sin(angle1) * np.cos(angle2)
    return np.cos(angle2) / d, np.cos(angle1) / d
   

class Simulation():
    def __init__(self):
        # anchor lines
        self.line_length = [200, 200]
        self.max_line_length = 400
        self.step_unit = 1
        self.anchor_points = [(0, 0), (300, 0)]
        self._pen_down = False
        # drawing lines
        self.lines = []
        self.move_lines = []
        self.current_line = []
        self.home = (self.anchor_width / 2, self.anchor_width / 2)
        self.upper_tension_border = None
        self.find_home()
        self.set_home()
        self.lower_tension_border = [[(0, 0), (0, 0), (0, 0)], [(0, 0), (0, 0), (0, 0)]]
        self.find_lower_tension_border()
        
    def guesstimate_anchor_points(self):
        self.anchor_points = [(0, 0), (0.8 * sum(self.line_length), 0)]        

    def guesstimate_line_lenth(self):
        self.line_length = [self.anchor_width * 0.55] * 2
        
    def apply__readable_command(self, command):
        self.apply_command(command_dict[command])

    def apply_command(self, command):
        if command == 'a':
            self._step(0, -1)
        elif command == 'b':
            self._step(0, 1)
        elif command == 'c':
            self._step(1, 1)
        elif command == 'd':
            self._step(1, -1)
        elif command == 'e':
            self.pen_up()
        elif command == 'f':
            self.pen_down()
        else:
            print(f'unknown command {command}')
        
    def send_commands(self, commands):
        for command in commands:
            self.apply_command(command)

    def _step_command(self, anchor=0, direction=1):
        assert anchor in [0, 1]
        assert direction in [-1, 1]
        if anchor == 0:
            if direction == -1:
                return 'a'
            else:
                return 'b'
        else:
            if direction == -1:
                return 'd'
            else:
                return 'c'

    def _step(self, anchor=0, direction=1):
        assert anchor in [0, 1]
        assert direction in [-1, 1]
        self.line_length[anchor] += direction * self.step_unit
        self.current_line.append(self.pen_position)

    def pen_up(self):
        if self._pen_down:
            self._pen_down = False
            self.lines.append(self.current_line)
            self.current_line = [self.pen_position]
        
    def pen_down(self):
        if not self._pen_down:
            self._pen_down = True
            self.move_lines.append(self.current_line)
            self.current_line = [self.pen_position]

    @property
    def anchor_width(self):
        return self.anchor_points[1][0] - self.anchor_points[0][0]
    
    @property        
    def pen_position(self):
        return find_pen_position(self.line_length[0], self.line_length[1], self.anchor_width)
    
    def find_line_length(self, x, y):
        # pythagoras to the rescue: a**2 + b**2 = c**2
        line_length = []
        for anchor in [0, 1]:
            a = x - self.anchor_points[anchor][0]
            b = y - self.anchor_points[anchor][1]
            line_length.append(np.sqrt(a**2 + b**2))
            
        return line_length
    
    def tension(self, p):
        # find angles
        angle1 = np.arctan2(p[1] - self.anchor_points[0][1], p[0] - self.anchor_points[0][0])
        angle2 = np.arctan2(p[1] - self.anchor_points[1][1], self.anchor_points[1][0] - p[0])
        # tension calculation
        t1, t2 = line_tensions(angle1, angle2)
        return t1, t2
    
    def find_home(self):
        self.upper_tension_border = None
        x = self.anchor_width / 2
        y = 1
        tension_absolute_delta = 1000
        best_tension_absolute_delta = 1000        
        for y in range(1, self.anchor_width ):
            tension_absolute_delta = sum(abs(np.array(self.tension((x, y))) - 1))
            if (tension_absolute_delta < 3) and (not self.upper_tension_border):
                self.upper_tension_border = y
            if tension_absolute_delta < best_tension_absolute_delta:
                best_tension_absolute_delta = tension_absolute_delta
                self.home = (x, y)
            else:
                # once tension increases again it will never go down and we can stop
                break
            
            # print(y, tension_absolute_delta)
    
    def set_home(self):
        self.line_length = self.find_line_length(*self.home)
        
    def find_lower_tension_border(self, min_tension_threshold=0.5):
        self.lower_tension_border = [[], []]
        
        start_x = self.anchor_width / 2
        start_y = self.upper_tension_border / 2
        
        # for ratio in [1/128, 1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1, 2, 4, 8, 16, 32, 64]:
        for ratio in [1/32, 1/16, 1/8, 1/4, 1/2, 1, 2, 4, 8, 16]:
            for dy in range(self.max_line_length * 10):
                dx = ratio * dy
                x = start_x + dx
                y = start_y + dy
                if min(self.tension((x, y))) < min_tension_threshold:         
                    break
                
            self.lower_tension_border[0].append((x, y))            
            self.lower_tension_border[1].append((start_x - dx, y))   
            
    
    def draw_svg(self, filename='./plotter_simulation.svg', draw_move_lines=True):
        # finish virtual drawing
        if self._pen_down:
            self.pen_up()  
        self.pen_down()
        self.pen_up()  
            
        dwg = svgwrite.Drawing(filename=filename,
                               viewBox=('{} {} {} {}'.format(-self.anchor_width * 0.05, -self.max_line_length * 0.05, self.anchor_width * 1.05, self.max_line_length * 1.05)))
        
        max_line_length = dwg.add(dwg.g(id='max_line_length', fill='none', stroke='orange', stroke_dasharray='5,5', stroke_width=1))
        for center in self.anchor_points:
            max_line_length.add(dwg.circle(center=center, r=self.max_line_length))
            
        anchors = dwg.add(dwg.g(id='anchors', fill='lightgrey', stroke='red', stroke_width=1))
        for center in self.anchor_points:
            anchors.add(dwg.circle(center=center, r=5))
            
        anchor_lines = dwg.add(dwg.g(id='anchor_lines', fill='white', stroke='red', stroke_width=1))
        anchor_lines.add(dwg.line(start=self.anchor_points[0], end=self.pen_position))
        anchor_lines.add(dwg.line(start=self.anchor_points[1], end=self.pen_position))
            
        lines = dwg.add(dwg.g(id='lines', fill='white', stroke='black', stroke_width=1))
        for line in self.lines:
            for start, end in zip(line[:-1], line[1:]):
                lines.add(dwg.line(start=start, end=end))   
                
        if draw_move_lines:
            move_lines = dwg.add(dwg.g(id='move_lines', fill='white', stroke='green', stroke_width=0.5))
            for line in self.move_lines:
                for start, end in zip(line[:-1], line[1:]):
                    move_lines.add(dwg.line(start=start, end=end))   
                    
        upper_tension_border = dwg.add(dwg.g(id='upper_tension_border', fill='white', stroke='blue', stroke_width=1))
        upper_tension_border.add(dwg.line(start=(0, self.upper_tension_border), end=(self.anchor_width, self.upper_tension_border)))   
        
        dwg.save()
        
if __name__ == '__main__':
    sim = Simulation()
    # sim.send_commands(['f', 'a', 'e'])  # origin
    # sim.send_commands(['f'] + ['b', 'c'] * 20 + ['e'])  # down
    # sim.send_commands(['f'] + ['b', 'd'] * 20 + ['e'])  # right
    # sim.send_commands(['f'] + ['a', 'd'] * 20 + ['e'])  # up
    # sim.send_commands(['f'] + ['a', 'c'] * 20 + ['e'])  # left
    
    calibration_radius_steps = 50
    calibration_cross = []
    # calibration_cross.extend(['e'] + ['a', 'd'] * calibration_radius_steps)  # move up
    calibration_cross.extend(['f'] + ['b', 'c'] * 2 * calibration_radius_steps + ['e'])  # line down
    calibration_cross.extend(['e'] + ['a', 'd'] * calibration_radius_steps)  # move up
    calibration_cross.extend(['e'] + ['a', 'c'] * calibration_radius_steps)  # move left
    calibration_cross.extend(['f'] + ['b', 'd'] * 2 * calibration_radius_steps + ['e'])  # line right
    calibration_cross.extend(['e'] + ['a', 'c'] * calibration_radius_steps)  # move left = back to home
    
    sim.send_commands(calibration_cross)
    
    sim.draw_svg()