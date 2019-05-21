
class rrange(dict):
	def __init__(self, beg, end, step=1):


		super().update({'b':beg})
		super().update({'e':end})
		super().update({'s':step})
		super().update({'t':'rrange'})
		super().update({0:beg}) #default value

		if end is None: end = float('inf')
		self.beg = beg
		self.end = end
		self.step = step

	def __contains__(self,v):
		return v <= self.end and v >= self.beg

	def __getitem__(self, key):
		v = (key+1)*self.step;
		if not self.__contains__(v):
			raise IndexError('Index out of bound!')

		return v



if __name__ == "__main__":
	print(4 in rrange(1,5))
	print(8 in rrange(1,5))