# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:30:22 2021

@author: oixc
"""

import serial
import itertools
import sys
import time

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def cmd(ser, cmd):
    cmd = cmd.encode()
    ser.write(cmd)
    ser.flush()
    result = ser.read()
    assert (cmd == result), 'cmd and result need to match'
    print(cmd, result, cmd == result)

def send_commands(commands):
    chunk_size = 20
    progress_print_commands = 1000
    with serial.Serial() as ser:
        ser.baudrate = 9600
        # ser.port = 'COM4'  # usb
        # ser.port = 'COM5'  # bluetooth
        ser.port = '/dev/ttyACM0' # raspberry
        ser.timeout = None
        ser.open()
        
        establish_contact(ser)
        start = time.time()
        # start_time = time.strftime('%H:%M:%S', time.localtime(start))
        total_commands = len(commands)
        commands_sent = 0
        temp = -1
        try:
            for chunk in chunks(commands, chunk_size):
                for c in chunk:
                    ser.write(c.encode())
                
                # print progress and end time estimate
                commands_sent += chunk_size
                # only print every <progress_print_commands> commands
                if temp < commands_sent // progress_print_commands:
                    temp = commands_sent // progress_print_commands
                    progress = commands_sent * 1.0 / total_commands
                    elapsed_time = time.time() - start
                    # time_per_command = elapsed_time / commands_sent()
                    total_time_estimate = elapsed_time / progress
                    time_left = total_time_estimate - elapsed_time
                    end_time_estimate = time.strftime('%H:%M:%S', time.localtime(start + total_time_estimate))
                    # print(f'{time.strftime("%H:%M:%S")}: {commands_sent} {progress:.2%} {time_left:.0f}s left --- end time {end_time_estimate}')      
                    print('{}: {} {:.2%} {:.0f}s left --- {}'.format(time.strftime("%H:%M:%S"), commands_sent, progress, time_left, end_time_estimate))         
                
                # wait for the plotter to clear the serial buffer
                while ser.in_waiting <= 0:
                    pass
                ser.read(ser.in_waiting)
        except KeyboardInterrupt:
            print('interrupted - moving home')
            for c in ['h'] * chunk_size * 2:
                ser.write(c.encode())
            
                               
def establish_contact(ser):
    while ser.in_waiting <= 0:
        pass
    ser.write(b'A')
    result = ser.read(ser.in_waiting)
    time.sleep(0.3)
    return result
    
        
if __name__ == '__main__':
    # knightrider = ['a', 'b', 'c', 'd']
    # knightrider.extend(reversed(knightrider[1:-1]))
    # knightrider = itertools.cycle(knightrider)
    
    send_commands(['d'] * 2500 + ['x'])
    # send_commands(['c', 'a'] * 100)
    # send_commands(knightrider)
    
    # send_commands(['e', 'f'] * 10)
    
    # ser = serial.Serial()
    # ser.baudrate = 9600
    # ser.port = 'COM4'  # usb
    # # ser.port = 'COM5'  # bluetooth
    # ser.timeout = None
    # ser.open()
    # result = establish_contact(ser)
    
    # # for c in knightrider * 10: # ['a', 'c'] * 25:
    # #     ser.write(c.encode())
    # ser.close()
# 
