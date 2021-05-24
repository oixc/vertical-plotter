# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:16:44 2021

@author: oixc
"""

import arduino_serial
import simulation
import numpy as np
from util import command_dict
import cairo

class Plotter(simulation.Simulation):
    def __init__(self):
        super().__init__()
        self.translate = [0, 0]
        self.scale = [1, 1]
        
    def offset(self, x, y):
        x = self.translate[0] + x * self.scale[0]
        y = self.translate[1] + y * self.scale[1]
        return x, y
    
    def reverse_offset(self, x, y):
        x = (x - self.translate[0]) / self.scale[0]
        y = (y - self.translate[1]) / self.scale[1] 
        return x, y
    
    def find_step_squence(self, x, y, fast=False):
        target_line_length = np.array(self.find_line_length(x, y))
        current_line_length = np.array(self.line_length)
        delta_line_length = target_line_length - current_line_length
        line_steps = delta_line_length / self.step_unit
        
        step_sequence = []
        if any(abs(line_steps) < 0.5):
            # only one line needs to change length
            for anchor in [0, 1]:
                direction = np.sign(line_steps[anchor])
                number_of_steps = int(abs(np.round(line_steps[anchor], 0)))
                if number_of_steps > 0:
                    step_sequence.extend(number_of_steps * [self._step_command(anchor, direction)])
            
            return step_sequence
        
        step_sequence = []
        
        if fast or False:
            # orthogonal grid: inspired by https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
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
            # polar grid
            approach = 'rounding'
            approach = 'test'
            if approach == 'rounding':
                np_anchor = np.array(self.anchor_points)
                current_point = np.array(self.pen_position)
                target_point = np.array([x, y])
                delta_point = target_point - current_point
                delta_max_steps = int(10 + abs(np.ceil(np.sum(abs(delta_point) / self.step_unit))))
                
                prev_steps = np.array([-1, -1])
                delta_steps = np.array([0, 0])
                dist = np.array([0.0, 0.0])
                for i in np.linspace(0, 1, delta_max_steps):
                    temp_point = current_point + i * delta_point
                    for anchor in [0, 1]:
                        dist[anchor] = np.linalg.norm(temp_point - np_anchor[anchor])
                    
                    # the closest polar grid point to temp_point is determined by rounding
                    steps = np.round(dist / self.step_unit, 0)
                    
                    if prev_steps[0] > -1:
                        delta_steps = steps - prev_steps
                        
                    # if step numbers changed for the closest point we need a command
                    if any(abs(delta_steps)) > 0:
                        for anchor in [0, 1]:
                            direction = np.sign(delta_steps[anchor])
                            for _ in range(int(abs(delta_steps[anchor]))):
                                step_sequence.append(self._step_command(anchor, direction))
                        
                    prev_steps = steps
                    
            elif approach == 'test':
                
                simulated_pen_position = []
                current_points = []
                
                debug = False
                if debug:
                    surface = cairo.SVGSurface('step_sequence.svg', 10 * self.anchor_width, 10 * self.max_line_length)
                    cr = cairo.Context(surface)
                    cr.scale(25, 25)
                    cr.translate(-self.pen_position[0] + 10, -self.pen_position[1] + 10)
                
                np_anchor = np.array(self.anchor_points)
                start_point = np.array(self.pen_position)
                
                target_line_length = np.array(self.find_line_length(x, y))
                target_steps = target_line_length / self.step_unit
                target_steps = np.round(target_steps, 0)
                target_line_length = target_steps * self.step_unit
                
                target_point = np.array(self.pen_position_from_lines(target_line_length))
                delta_point = target_point - start_point
                
                current_line_length = np.array(self.line_length)
                
                current_steps = current_line_length / self.step_unit
                # target_steps = target_line_length / self.step_unit
                
                line_steps = target_steps - current_steps
                
                directions = np.sign(line_steps)
                number_of_steps = np.abs(np.round(line_steps, 0)).astype(int)
                
                current_point = start_point
                # current_points.append(current_point)
                # simulated_pen_position.append(self.pen_position_from_lines(current_steps * self.step_unit))
                
                
                
                if debug:
                    cr.save()
                    for anchor in [0, 1]:
                        for steps in range(number_of_steps[anchor]):
                            cr.new_sub_path()
                            cr.arc(*self.anchor_points[anchor], (current_steps[anchor] + directions[anchor] * steps) * self.step_unit, 0, 2 * np.pi)
                            cr.set_source_rgba(0, 0, 0, 0.5)
                            # cr.set_dash([0.1, 0.1])
                            cr.set_line_width(0.05)
                            cr.stroke()
                    cr.restore()
                    
                    cr.move_to(*start_point)
                    cr.line_to(*target_point)
                    cr.set_source_rgb(1, 0, 0)
                    cr.set_line_width(0.1)
                    cr.stroke()
                
                while sum(number_of_steps) > 0:
                    
                    if debug:   
                        current_points.append(current_point)
                        simulated_pen_position.append(self.pen_position_from_lines(current_steps * self.step_unit))
                    current_point = self.pen_position_from_lines(current_steps * self.step_unit)
                
                    next_point1 = current_point - np_anchor
                    next_point2 = next_point1
                    for anchor in [0, 1]:
                        next_point2[anchor] = next_point1[anchor] / current_steps[anchor] * (current_steps[anchor] + directions[anchor])
                    next_point = next_point2 + np_anchor
                             
                    # next_point = np_anchor.astype(float)
                    # for anchor in [0, 1]:
                    #     temp_next_steps = current_steps
                    #     temp_next_steps[anchor] += directions[anchor]
                    #     next_point[anchor] = self.pen_position_from_lines(temp_next_steps * self.step_unit)
                        
                    # cr.save()
                    # for anchor in [0, 1]:
                    #     cr.new_sub_path()
                    #     cr.arc(*self.anchor_points[anchor], current_steps[anchor] * self.step_unit, 0, 2 * np.pi)
                    #     cr.set_source_rgba(0, 0, 0, 0.5)
                    #     # cr.set_dash([0.1, 0.1])
                    #     cr.set_line_width(0.05)
                    #     cr.stroke()
                    # cr.restore()
                    
                    # cr.save()
                    # for anchor in [0, 1]:
                    #     cr.move_to(*current_point)
                    #     cr.line_to(*self.anchor_points[anchor])
                    #     cr.set_source_rgba(0, 0, 0, 0.5)
                    #     # cr.set_dash([0.1, 0.1])
                    #     cr.set_line_width(0.05)
                    #     cr.stroke()
                    # cr.restore()
                        
                
                    if debug:   
                        for anchor in [0, 1]:
                            cr.move_to(*current_point)
                            cr.line_to(*next_point[anchor])
                            cr.set_source_rgb(0, 0, 1)
                            cr.stroke()
                        
                        
                    # cr.move_to(*next_point[0])
                    # cr.line_to(*next_point[1])
                    # cr.set_source_rgb(0, 1, 0)
                    # cr.stroke()
                    
                
                    # next_point[0] + t0 * (next_point[1] - next_point[0])
                    # start_point + t1 * (target_point - start_point)
                    
                    x0 = next_point[0][0]
                    y0 = next_point[0][1]
                    
                    dx0 = (next_point[1] - next_point[0])[0]
                    dy0 = (next_point[1] - next_point[0])[1]
                    
                    x1 = start_point[0]
                    y1 = start_point[1]
                    
                    dx1 = (target_point - start_point)[0]
                    dy1 = (target_point - start_point)[1]
                    
                    # print('dx0, dy0, dx1, dy1', dx0, dy0, dx1, dy1)
                    if dx0 == 0:
                        t1 = (x0 - x1) / dx1
                        y = y1 + t1 * dy1
                        t0 = (y - y0) / dy0
                    elif dy1 == 0:
                        if dy0 == 0:
                            t0 = 0
                        else:
                            t0 = (y1 - y0) / dy0
                    elif dy0 == 0:
                        t1 = (y0 - y1) / dy1
                        x = x1 + t1 * dx1
                        t0 = (x - x0) / dx0
                    elif dx1 == 0:
                        if dx0 == 0:
                            t0 = 0
                        else:
                            t0 = (x1 - x0) / dx0    
                    else:
                        part1 = (x1 - x0) / dx0
                        part2 = dx1 / dx0 * (y0 - y1) / dy1
                        part3 = 1 - dx1 / dx0 * dy0 / dy1
                        
                        t0 = (part1 + part2) / part3 
                        
                    # print('t0', t0)
                    # assert 0 <= t0 <= 1, t0
                    if t0 < 0.5:
                        anchor = 0
                    else:
                        anchor = 1
                        
                    # if number_of_steps[anchor] <= 0:
                    #     anchor = 1 - anchor
                        
                    direction = directions[anchor]
                    step_sequence.append(self._step_command(anchor, direction))
                    number_of_steps[anchor] -= 1
                    current_steps[anchor] += directions[anchor]
                    current_point = next_point[anchor]      
                        
                    # debugging information
                    if debug:   
                        x = x0 + t0 * dx0
                        y = y0 + t0 * dy0
                        
                        t1_x = (x - x1) / dx1
                        t1_y = (y - y1) / dy1 
                        
                        cr.move_to(*next_point[anchor])
                        cr.line_to(x, y)
                        cr.set_source_rgb(0, 1, 0)
                        cr.stroke()
                        
                        epsilon = 1e-10
                        
                        assert abs(t1_x - t1_y) < epsilon
                        # print('t1_x, t1_y', t1_x, t1_y, abs(t1_x - t1_y))
                        
                        t1 = t1_x
                        x_t1 = x1 + t1 * dx1
                        y_t1 = y1 + t1 * dy1
                        
                        assert abs(x - x_t1) < epsilon
                        assert abs(y - y_t1) < epsilon
                        # print('x, y, next_point[anchor]', x, y, next_point[anchor])
                        
                        # print('t0, anchor, direction', t0, anchor, direction)
                        # print('number_of_steps', number_of_steps)
                        # print('current_steps', current_steps)
                        # print('target_steps', target_steps)
                        
                if debug:   
                    cr.move_to(*current_points[0])
                    for p in current_points[1:]:
                        cr.line_to(*p)
                    cr.set_source_rgb(1, 1, 0)
                    cr.stroke()
                        
                    cr.move_to(*simulated_pen_position[0])
                    for p in simulated_pen_position[1:]:
                        cr.line_to(*p)
                    cr.set_source_rgb(0.5, 0, 0.5)
                    cr.stroke()
                    
                    surface.finish()
                
            else:
                raise NotImplementedError
                                    
        return step_sequence
    
    def sequence_to(self, x, y, draw_line=False):
        x, y = self.offset(x, y)
        step_sequence = []
        if draw_line and (not self._pen_down):
            step_sequence = [command_dict['PD']] 
        if (not draw_line) and self._pen_down:
            step_sequence = [command_dict['PU']] 
        step_sequence.extend(self.find_step_squence(x, y, fast=(not draw_line)))
        # step_sequence.append(command_dict['PU'])
        
        self.send_commands(step_sequence)
        return step_sequence
    
    def line_to(self, x, y):
        return self.sequence_to(x, y, draw_line=True)
    
    def rel_line_to(self, dx, dy):
        x = self.pen_position[0] + dx
        y = self.pen_position[1] + dy
        return self.sequence_to(x, y, draw_line=True)
    
    def move_to(self, x, y):
        return self.sequence_to(x, y, draw_line=False)

    def rel_move_to(self, dx, dy):
        x = self.pen_position[0] + dx
        y = self.pen_position[1] + dy
        return self.sequence_to(x, y, draw_line=False)
    
    
def create_plotter(simulate=True, anchor_width=1000):
    sim = simulation.Simulation()

    if simulate:
        send_commands = sim.send_commands
    else:
        send_commands = arduino_serial.send_commands

    p = Plotter()
    
    sim.anchor_points[0] = (0, 0)
    sim.anchor_points[1] = (anchor_width, 0)
    sim.guesstimate_line_lenth()
    sim.find_home()
    sim.set_home()
    sim.find_lower_tension_border(min_tension_threshold=1/3)
    sim.max_line_length = sim.anchor_width * 1.2
    p.anchor_points = sim.anchor_points.copy()
    p.line_length = sim.line_length.copy()
    p.max_line_length = sim.max_line_length
    p.find_home()
    p.set_home()
    
    p.translate = [0, 0]
    p.scale = [1, 1]
    
    pulley_diameter = 10
    full_rotation_steps = 200 * 4
    sim.step_unit = p.step_unit = np.pi * pulley_diameter / full_rotation_steps
    
    return p, send_commands, sim 
    
    
if __name__ == '__main__':    
    send_commands = arduino_serial.send_commands
    
    sim = simulation.Simulation()
    # send_commands = sim.send_commands
    
    # def send_commands(commands):
    #     sim.send_commands(commands)
    #     arduino_serial.send_commands(commands)

    p = Plotter()
    
    calibrate = False
    if True:
        sim.anchor_points[0] = (0, 0)
        sim.anchor_points[1] = (1000, 0)
        sim.guesstimate_line_lenth()
        sim.find_home()
        sim.set_home()
        sim.drawing_area = [(390 + 30, 300 + 30), (390 + 297 - 50, 300 + 420 - 50)]
        sim.find_lower_tension_border(min_tension_threshold=1/3)
        sim.max_line_length = sim.anchor_width * 1.2
        p.anchor_points = sim.anchor_points.copy()
        p.line_length = sim.line_length.copy()
        p.max_line_length = sim.max_line_length
        p.find_home()
        p.set_home()
        p.drawing_area = sim.drawing_area  
        
        place_to_drawing_area = False
        
        p.translate = [0, 0]
        p.scale = [1, 1]
        
        pulley_diameter = 10
        full_rotation_steps = 200 * 4
        sim.step_unit = p.step_unit = np.pi * pulley_diameter / full_rotation_steps
        
        # sim.step_unit = p.step_unit = 1  # 0.1
        
        # x, y = 150, 100
        # x, y = p.pen_position
        # x = 10
        # x, y = 200, 100
        # step_sequence = p.find_step_squence(x, y)
        # send_commands(['f'] + step_sequence + ['e']) 
            
        # send_commands(['f'] + ['c', 'c', 'a'] * 30 + ['e'] + ['a', 'a', 'd'] * 20 + ['f'] + ['a', 'c'] * 30 + ['e']) 
        
        all_commands = []
        
        ## rectanlge(100, 100, 100, 100)
        # p.translate = [300, 400]
        # p.scale = [4, 4]
        
        # intermediate_steps = 10
        
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
        
        # filename = 'calibration'
        # p.translate = [238, 180]
        # p.scale = [0.3, 0.3]
        # sim.step_unit = p.step_unit = 1  # 0.1
        
        # filename = 'test_pattern'
        # p.translate = [100, 200]
        # p.scale = [0.4, 0.4]
        
        # filename = 'star'
        # p.translate = [500, 289]
        # p.scale = [0.4, 0.4]
        # sim.step_unit = p.step_unit = 5  # 0.1
              
        filename = 'penguin'
        # p.translate = [391, 30]
        # p.scale = [2.5, 2.5]
        p.translate = [310, 180]
        p.scale = [1, 1]
        
        # p.find_home()
        # p.set_home()
        with open(f'svg/{filename}.path', 'r') as f:
            path = f.read()
            
        xs = []
        ys = []
            
        path = iter(path.split())
        for action in path:
            x = float(next(path))
            y = float(next(path))
            
            xs.append(x)
            ys.append(y)
            
            if not place_to_drawing_area:
                if action == 'M':
                    all_commands.extend(p.move_to(x, y))
                elif action == 'L':
                    all_commands.extend(p.line_to(x, y))
                else:
                    raise NotImplementedError()
                    
        print('top left canvas: ', p.offset(min(xs), min(ys)))
        print('bottom right canvas: ', p.offset(max(xs), max(ys)))
                
        current_width = max(xs) - min(xs)
        target_width = p.anchor_width * 0.5
        x_scale = target_width / current_width            
        x_scale = p.scale[0] 
        
        current_center = (max(xs) + min(xs)) / 2 * x_scale
        target_center = p.anchor_width / 2 
        x_translate = target_center - current_center            
        
        current_top = min(ys) * x_scale
        target_top = (p.home[1] + p.upper_tension_border) / 2
        target_top = p.home[1]
        y_translate = target_top - current_top        
        
        print('translate', x_translate, y_translate)
        print('scale', x_scale, x_scale)
        
        ## scale to drawing area        
        current_width = max(xs) - min(xs)
        target_width = p.drawing_area[1][0] - p.drawing_area[0][0]
        # target_width *= 0.9
        x_scale = target_width / current_width   
        
        current_height = max(ys) - min(ys)
        target_height = p.drawing_area[1][1] - p.drawing_area[0][1]
        # target_height *= 0.9
        y_scale = target_height / current_height            
        
        x_scale = y_scale = min(x_scale, y_scale)
        
        current_center = (max(xs) + min(xs)) / 2 * x_scale
        target_center = (p.drawing_area[1][0] + p.drawing_area[0][0]) / 2
        x_translate = target_center - current_center            
        
        # current_top = min(ys) * x_scale
        # target_top = p.drawing_area[0][1]
        # y_translate = target_top - current_top        
        
        current_center = (max(ys) + min(ys)) / 2 * y_scale
        target_center = (p.drawing_area[1][1] + p.drawing_area[0][1]) / 2
        y_translate = target_center - current_center     
        
        print('-- drawing area --')        
        print(f'p.translate = [{x_translate:.0f}, {y_translate:.0f}]')        
        print(f'p.scale = [{x_scale:.3f}, {y_scale:.3f}]')
        
        assert not place_to_drawing_area, 'if we only place to drawing area we do not need the rest'
        
        # return home
        all_commands.append(command_dict['PU'])
        all_commands.extend(p.move_to(*p.reverse_offset(*p.home)))
        # all_commands.extend(p.move_to(p.anchor_width / 2, 200))
        # all_commands.extend([command_dict['RL']] * 500)
        
    elif calibrate:
        sim.anchor_points[0] = (0, 0)
        sim.anchor_points[1] = (1000, 0)
        sim.guesstimate_line_lenth()
        # sim.find_home()
        # sim.set_home()        
        sim.line_length = [300.0, 1000.0]
        sim.find_lower_tension_border()
        sim.max_line_length = sim.anchor_width * 1.2
        p.anchor_points = sim.anchor_points.copy()
        p.line_length = sim.line_length.copy()
        p.max_line_length = sim.max_line_length
        # p.find_home()
        # p.set_home()
        
        p.translate = [0, 0]
        p.scale = [1, 1]
        
        pulley_diameter = 10
        full_rotation_steps = 200 * 8
        sim.step_unit = p.step_unit = np.pi * pulley_diameter / full_rotation_steps
        # sim.step_unit = p.step_unit = 1.0
        
        all_commands = []
        # all_commands.extend(p.rel_line_to(0, 200))
        # all_commands.extend(p.rel_move_to(-100, -100))
        # all_commands.extend(p.rel_line_to(200, 0))
        all_commands.extend(p.rel_line_to(100, 100))
        all_commands.extend(p.rel_line_to(100, -100))
        all_commands.extend(p.rel_line_to(100, 100))
        all_commands.extend(p.rel_line_to(100, -100))
        all_commands.extend(p.rel_line_to(100, 100))
        all_commands.extend(p.rel_line_to(100, -100))
        all_commands.extend(p.rel_line_to(100, 100))
        all_commands.extend(p.rel_line_to(100, -100))
        all_commands.extend(p.rel_line_to(100, 100))
        # all_commands.append(command_dict['PU'])
        # all_commands.extend(p.move_to(*p.reverse_offset(*p.home)))
      
    else:
        # p.translate = [20, 0]
        # p.scale = [1/2, 1/2]
        all_commands = []
        all_commands.extend(p.move_to(200, 200))
        all_commands.extend(p.line_to(20, 200))
        all_commands.extend(p.move_to(*p.home))
      
    print(len(all_commands))
    send_commands(all_commands)
    
    # write commands
    if False:        
        with open('plot_commands.txt', 'w') as f:
            f.write(''.join(all_commands))  
        
    # commands analysis
    if True:
        compact_commands = []
        last_c = -1
        repetition = 0
        for c in all_commands:    
            repetition += 1
            if c != last_c:
                compact_commands.append([last_c, repetition])
                repetition = 0
                last_c = c
                
        counter = 0
        prev_count = -1
        prev_c = -1
        for c, count in compact_commands:
            if c in ['a', 'b', 'c', 'd']:
                # print(prev_c, prev_count, c, count)
                if (prev_count == 1) and (count == 1):
                    print(prev_c, c)
                    counter += 1
                prev_count = count
            else:
                prev_count = -1
            prev_c = c
            
        command_lengths = set(c[1] for c in compact_commands)
            
    # sim.draw_svg(draw_move_lines=False, draw_tension_lines=False, draw_anchor_lines=False)
    sim.draw_svg(draw_move_lines=True, draw_tension_lines=True, draw_anchor_lines=True)
