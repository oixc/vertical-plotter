# -*- coding: utf-8 -*-
"""
Created on Sun Apr  18 16:16:44 2021

@author: oixc

https://howtomechatronics.com/tutorials/g-code-explained-list-of-most-important-g-code-commands/
"""

import numpy as np
from util import command_dict
import plotter

if __name__ == '__main__':        
    p, send_commands, sim = plotter.create_plotter(simulate=True)
    
    sim.step_unit = p.step_unit = 1
    # p.translate = [0, 0]
    # p.scale = [1/2, 1/2]
    all_commands = []
    all_commands.extend(p.move_to(200, 200))
    all_commands.extend(p.line_to(20, 200))
    all_commands.extend(p.move_to(*p.home))
      
    print(len(all_commands))
    send_commands(all_commands)
    
    # sim.draw_svg(draw_move_lines=False, draw_tension_lines=False, draw_anchor_lines=False)
    sim.draw_svg(draw_move_lines=True, draw_tension_lines=True, draw_anchor_lines=True)
