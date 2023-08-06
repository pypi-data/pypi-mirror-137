

import timeit

def get_exec_time(total_execs=1, _repeat=1):
	"""
		basically here we calculate the
		average time it takes to run this function
		or block of code
	"""
	def inner_wrapper(_function, *args, **kwargs):
		computational_times = timeit.repeat(
			lambda: _function(*args, **kwargs),
			number=total_execs,
			repeat=_repeat
		)
		return sum(computational_times) / len(computational_times)
	return inner_wrapper

def print_exec_time(total_execs=1, _repeat=1):
	"""
		same thing but just printing
	"""
	def inner_wrapper(function):
		computational_times: list = timeit.repeat(function(
			*arguments, **keyword_arguments), number=total_execs, repeat=_repeat)
		print(sum(computational_times) / len(computational_times))
	return inner_wrapper


# testing the module right there