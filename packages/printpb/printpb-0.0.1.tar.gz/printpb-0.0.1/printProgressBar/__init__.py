import time
import sys


class ProgressBar(object):
    def __init__(self, percentage, sleepTime=0.25):
        super(ProgressBar)
        color = '30'
        bgcolor = '40'
        if percentage <= 0:
            raise ValueError("Wrong total number ...")
        for x in range(1, percentage+1):
            if x != percentage:
                e = ''
            else:
                e = '\n'
            time.sleep(sleepTime)
            if x <= 10:
                color = '37'
                bgcolor = '47'
            elif 10 < x <= 25:
                color = '36'
                bgcolor = '46'
            elif 25 < x <= 35:
                color = '34'
                bgcolor = '44'
            elif 35 < x <= 47:
                color = '33'
                bgcolor = '44'
            elif 47 < x <= 60:
                color = '32'
                bgcolor = '42'
            elif 60 < x <= 80:
                color = '31'
                bgcolor = '41'
            elif 80 < x <= 90:
                color = '36'
                bgcolor = '46'
            else:
                color = '30'
                bgcolor = '40'
            print('\033[0;%s%s' % (color, 'm') +
                  '#'+'\033[0m', end=e, flush=True)
