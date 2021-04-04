# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:16:44 2021

@author: oixc
"""

import arduino_serial
import simulation
import numpy as np
from util import command_dict

class Plotter(simulation.Simulation):
    def __init__(self):
        super().__init__()
        
    def find_line_length(self, x, y):
        # pythagoras to the rescue: a**2 + b**2 = c**2
        line_length = []
        for anchor in [0, 1]:
            a = x - self.anchor_points[anchor][0]
            b = y - self.anchor_points[anchor][1]
            line_length.append(np.sqrt(a**2 + b**2))
            
        return line_length
    
    def find_step_squence(self, x, y):
        target_line_length = np.array(self.find_line_length(x, y))
        current_line_lenght = np.array(self.line_length)
        delta_line_lenght = target_line_length - current_line_lenght
        line_steps = delta_line_lenght / self.step_unit
        
        step_sequence = []
        if any(abs(line_steps) < 0.5):
            # only one line needs to change lenght
            for anchor in [0, 1]:
                direction = np.sign(line_steps[anchor])
                number_of_steps = int(abs(np.round(line_steps[anchor], 0)))
                step_sequence.extend(number_of_steps * [self._step_command(anchor, direction)])
            
            return step_sequence
        
        step_sequence = []
        
        orthogonal_grid = False
        if orthogonal_grid:
            # inspired by https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
            directions = []
            number_of_steps = []
            for anchor in [0, 1]:
                directions.append(np.sign(line_steps[anchor]))
                number_of_steps.append(int(abs(np.round(line_steps[anchor], 0))))
    
            target_step_ratio = number_of_steps[0] / number_of_steps[1]
            while sum(number_of_steps) > 0:
                if number_of_steps[1] == 0:
                    anchor = 0
                else:
                    if number_of_steps[0] / number_of_steps[1] > target_step_ratio :
                        anchor = 0
                    else:
                        anchor = 1
                direction = directions[anchor]
                step_sequence.append(self._step_command(anchor, direction))
                number_of_steps[anchor] -= 1

        else:
            current_point = np.array(self.pen_position)
            target_point = np.array([x, y])
            delta_point = target_point - current_point
            delta_max_steps = int(abs(np.ceil(np.sum(delta_point / self.step_unit))))
            
            left_anchor = np.array(self.anchor_points[0])
            right_anchor = np.array(self.anchor_points[1])
            
            prev_left_steps = -1
            prev_right_steps = -1
            left_delta = 0
            right_delta = 0
            
            for i in np.linspace(0, 1, delta_max_steps):
                temp_point = current_point + i * delta_point
                left = np.linalg.norm(temp_point - left_anchor)
                right = np.linalg.norm(temp_point - right_anchor)
                
                left_steps = np.round(left / self.step_unit, 0)
                right_steps = np.round(right / self.step_unit, 0)
                
                if prev_left_steps > -1:
                    left_delta = left_steps - prev_left_steps
                    right_delta = right_steps - prev_right_steps
                
                if abs(left_delta) > 0:
                    # assert abs(left_delta) < 2
                    anchor = 0
                    direction = np.sign(left_delta)
                    for _ in range(int(abs(left_delta))):
                        step_sequence.append(self._step_command(anchor, direction))
                    
                if abs(right_delta) > 0:
                    # assert abs(right_delta) < 2
                    anchor = 1
                    direction = np.sign(right_delta)
                    for _ in range(int(abs(right_delta))):
                        step_sequence.append(self._step_command(anchor, direction))
                
                # if abs(right_delta) + abs(left_delta) > 0:    
                #     print(temp_point, left_steps, right_steps, left_delta, right_delta)
                
                prev_left_steps = left_steps
                prev_right_steps = right_steps
                
        return step_sequence
    
    def sequence_to(self, x, y, draw_line=False):
        step_sequence = []
        if draw_line and (not self._pen_down):
            step_sequence = [command_dict['PD']] 
        if (not draw_line) and self._pen_down:
            step_sequence = [command_dict['PU']] 
        step_sequence.extend(self.find_step_squence(x, y))
        # step_sequence.append(command_dict['PU'])
        
        self.send_commands(step_sequence)
        return step_sequence
    
    def line_to(self, x, y):
        return self.sequence_to(x, y, draw_line=True)
    
    def move_to(self, x, y):
        return self.sequence_to(x, y, draw_line=False)
    
    
if __name__ == '__main__':    
    send_commands = arduino_serial.send_commands
    
    sim = simulation.Simulation()
    send_commands = sim.send_commands
    
    # def send_commands(commands):
    #     sim.send_commands(commands)
    #     arduino_serial.send_commands(commands)

    p = Plotter()
    
    if True:
        sim.anchor_points[0] = (0, 0)
        sim.anchor_points[1] = (1750, 0)
        sim.guesstimate_line_lenth()
        p.anchor_points = sim.anchor_points.copy()
        p.line_length = sim.line_length.copy()
        
        sim.step_unit = p.step_unit = 1 # 0.1
        # x, y = 150, 100
        # x, y = p.pen_position
        # x = 10
        # x, y = 200, 100
        # step_sequence = p.find_step_squence(x, y)
        # send_commands(['f'] + step_sequence + ['e']) 
            
        # send_commands(['f'] + ['c', 'c', 'a'] * 30 + ['e'] + ['a', 'a', 'd'] * 20 + ['f'] + ['a', 'c'] * 30 + ['e']) 
        
        intermediate_steps = 1
        
        all_commands = []
        ## rectanlge(100, 100, 100, 100)
        # all_commands.extend(p.move_to(100, 100))
        # for i in range(intermediate_steps):
        #     all_commands.extend(p.line_to(100 + (100 / intermediate_steps) * (i + 1), 100))
        # for i in range(intermediate_steps):
        #     all_commands.extend(p.line_to(200, 100 + (100 / intermediate_steps) * (i + 1)))
        # for i in range(intermediate_steps):
        #     all_commands.extend(p.line_to(200 - (100 / intermediate_steps) * (i + 1), 200))
        # for i in range(intermediate_steps):
        #     all_commands.extend(p.line_to(100, 200 - (100 / intermediate_steps) * (i + 1)))
        
        # all_commands.extend(p.line_to(1, 100))
        # all_commands.extend(p.line_to(150, 100))
        # all_commands.extend(p.line_to(299, 100))
        
        filename = 'calibration'
        with open(f'svg/{filename}.path', 'r') as f:
            path = f.read()
            
        xs = []
        ys = []
            
        path = iter(path.split())
        for action in path:
            x = float(next(path)) * 0.8
            y = float(next(path)) * 0.8
            
            xs.append(x)
            ys.append(y)
            
            if action == 'M':
                all_commands.extend(p.move_to(x, y))
            elif action == 'L':
                all_commands.extend(p.line_to(x, y))
            else:
                raise NotImplementedError()
    
    else:
        all_commands = []
        all_commands.extend(p.line_to(200, 200))
        all_commands.extend(p.line_to(20, 200))
      
    print(len(all_commands))
    send_commands(all_commands)

    sim.draw_svg()
