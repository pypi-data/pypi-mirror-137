
from time import sleep
import os
from animations import progress_bar

from threading import Thread

import sys
import time

# for i in range(100):
#     time.sleep(0.1)
#     sys.stdout.write(f'salutare-{i}\n')
#     sys.stdout.write(f'andrew-{i}\n')

#     sys.stdout.write("\x1b[1A")  # cursor up one line
#     sys.stdout.write("\x1b[2K")  # delete the last line

#     sys.stdout.write("\x1b[1A")  # cursor up one line
#     sys.stdout.write("\x1b[2K")  # delete the last line



def clear_lines(total=1):
    for _ in range(total):
        sys.stdout.write("\x1b[1A")  # cursor up one line
        sys.stdout.write("\x1b[2K")  # delete the last line


from random import randrange
from random import uniform

def work(_range, reference: list):
    for i in range(_range):
        reference[0] = i
        sleep(uniform(0.01, 0.2))
    reference[0] = _range


def work2(_range, reference: list):
    for i in range(_range):
        reference[0] = i
        sleep(uniform(0.01, 0.05))
    reference[0] = _range



work_ref = [0]
total_range = 100
work_thread = Thread(target=work, args=(total_range, work_ref))
work_thread.start()


work_ref2 = [0]
total_range2 = 100
work_thread2 = Thread(target=work2, args=(total_range2, work_ref2))
work_thread2.start()

while 1:
    p = progress_bar(work_ref[0], total_range, color="yellow", title="work_thread")
    print(p)

    p = progress_bar(work_ref2[0], total_range2, color="yellow", title="work_thread")
    print(p)

    if not work_thread.is_alive() and not work_thread2.is_alive():
        break

    clear_lines(2)
    sleep(0.01)

    # if j < 100:
    #     j += 2
    # p = progress_bar(j, 100, color="yellow", title="tqdm")
    # print(p)

    # if j >= 100 and index >= 100:
    #     break

