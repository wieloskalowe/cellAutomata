
import matplotlib.pyplot as plt

		
def graph(data):
	plt.matshow(data)
	plt.show()


def print_step(spsht):
	for v in spsht:
		c = v.get('state')

		if c is None or c==False : c = ' '
		else: c = '*'

		sys.stdout.write(c)
	print()
