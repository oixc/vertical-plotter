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
    

class Simulation():
    def __init__(self):
        self.line_length = [200, 200]
        self.step_unit = 1
        self.anchor_points = [(0, 0), (300, 0)]
        self._pen_down = False
        self.lines = []
        self.current_line = []

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
        if self._pen_down:
            self.current_line.append(self.pen_position)

    def pen_up(self):
        if self._pen_down:
            self._pen_down = False
            self.lines.append(self.current_line)
            self.current_line = []
        
    def pen_down(self):
        if not self._pen_down:
            self._pen_down = True
            self.current_line = [self.pen_position]

    @property
    def anchor_width(self):
        return self.anchor_points[1][0] - self.anchor_points[0][0]
    
    @property        
    def pen_position(self):
        return find_pen_position(self.line_length[0], self.line_length[1], self.anchor_width)
    
    def draw_svg(self, filename='./plotter_simulation.svg'):
        if self._pen_down:
            # finish virtual drawing
            self.pen_up()  
            self.pen_down()
        
        dwg = svgwrite.Drawing(filename=filename,
                               viewBox=('-100 -100 {} {}'.format(1000, self.anchor_width)))
        
        anchors = dwg.add(dwg.g(id='anchors', fill='lightgrey', stroke='red', stroke_width=0.2))
        for center in self.anchor_points:
            anchors.add(dwg.circle(center=center, r=5))
            
        anchor_lines = dwg.add(dwg.g(id='anchor_lines', fill='white', stroke='red', stroke_width=0.3))
        anchor_lines.add(dwg.line(start=self.anchor_points[0], end=self.pen_position))
        anchor_lines.add(dwg.line(start=self.anchor_points[1], end=self.pen_position))
            

        lines = dwg.add(dwg.g(id='lines', fill='white', stroke='black', stroke_width=0.2))
        for line in self.lines:
            for start, end in zip(line[:-1], line[1:]):
                lines.add(dwg.line(start=start, end=end))        
    
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