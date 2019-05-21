class RuleMask:
	"""   
         z(0,0,+)
        /
       /
      /
     /
    *-----------x(+,0,0)
    |
    |
    |
    |
    |
	y(0,+,0)

	* - (0,0,0)




    *1d mask constructor format
     ---x-->
     [1,2,3]

     normal list element reference looks like this then:
     [x]



    *2d mask constructor format
     [
      --x-->
     [1,2,3], |
     [1,2,3], y
     [1,2,3], |
              V
     ]

     python list element reference looks like this then:
      [y][x]





   *3d mask constructor format
    [
         ---z--> ---z--> ---z-->
        [[1,2,3],[1,2,3],[1,2,3]], |
        [[1,2,3],[1,2,3],[1,2,3]], y
        [[1,2,3],[1,2,3],[1,2,3]]  |
        ---------- x ----------->  V
    ]
    (ones are on the front surface of the cube, twos are on middle, and threes are on back surface)
	
	     z(0,0,+)
        / 3   3    3
       /
      / 2    2    2
     /
    *-1----1----1-x(+,0,0)
    | 
    | 1    1    1
    |
    | 1    1    1
    |
	y(0,+,0)

     python list element reference looks like this then:
      [y][x][z]

	
	passed rules are converted to 1d list of bools to make applying simpler
	1d list of values above looks like this
		*for 2d input
			[[1,2,3],
			 [1,2,3], => [1,2,3, 1,2,3, 1,2,3]
			 [1,2,3]]
		*for 3d input
		[
			[[1,2,3],[1,2,3],[1,2,3]],     v(0,0,0)    v(0,1,0)    v(0,2,0)
			[[1,2,3],[1,2,3],[1,2,3]], => [1,1,1,      1,1,1       1,1,1,    #<-1st layer#,
			[[1,2,3],[1,2,3],[1,2,3]]        ^(1,0,0)    ^(1,1,0)    ^(1,2,0)
                                           v(0,0,1)    v(0,1,1)    v(0,1,1)
										   2,2,2       2,2,2       2,2,2,    #<-2nd layer# (...and so on) ] 
                                             ^(1,0,1)    ^(1,0,1)    ^(1,2,1)
			]


	"""
	@staticmethod
	def _are_dims3(l):
		f = len(l)
		r = [len(x)==f for x in l]

		return all(r)

	def get(self, x, y=0, z=0):
		return self.mask[x + 3*y+9*z]


	def __init__(self,
				 mask #as above in comment
				 ):

		if type(mask) is not list:
			raise TypeError("Argument 'mask' has to be a list of max 3 dimensions ([x][y][z]) with size as follows x=3,y=3,z=3.")

		self.dimension 	= 0
		self.mask = []

		if len(mask) == 3: 
			self.dimension+=1
		else:
			raise TypeError("First dimension (x) of 'mask' has to be exacly of size 3.")



		if type(mask[0]) is list: 
			if RuleMask._are_dims3(mask): 
				self.dimension+=1
			else:
				raise TypeError("Second dimension (y) of 'mask' has to be exacly of size 3.")


			if type(mask[0][0]) is list: 
				if RuleMask._are_dims3(mask[0]): 
					self.dimension+=1
				else:
					raise TypeError("Third dimension (z) of 'mask' has to be exacly of size 3.")

		if self.dimension == 1:
			self.mask 		= 	[bool(x) for x in mask]

		if self.dimension == 2:
			for y in range(3):
				for x in range(3):
					self.mask.append(bool(mask[y][x]))



		if self.dimension == 3:
			for y in range(3):
				for x in range(3):
					for z in range(3):
						self.mask.append(bool(self.mask[y][x][z]))
						

		self.mask = tuple(self.mask)
