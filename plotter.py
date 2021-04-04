# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:16:44 2021

@author: oixc
"""

import arduino_serial
import simulation

# send_commands = arduino_serial.send_commands

sim = simulation.Simulation()
send_commands = sim.send_commands

# def send_commands(commands):
#     sim.send_commands(commands)
#     arduino_serial.send_commands(commands)

send_commands(['c', 'c', 'd'] * 100)
send_commands(['c', 'd', 'd'] * 100)