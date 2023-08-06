

from _core._time import get_exec_time

from time import sleep

# @get_exec_time(1, 1)
def worker():
	print("start")
	for _ in range(10):
		sleep(0.1)
	print("done")

if __name__ == '__main__':
	worker()