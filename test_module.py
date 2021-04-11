import unittest
from kmap import minFunc



class testpoint(unittest.TestCase):
	def test_minFunc(self):
		self.assertEqual(minFunc(4,'(0,1,2,4,5,6,8,9,12,13,14) d -'),('w\'z\'+xz\'+y\''))
		self.assertEqual(minFunc(2,'(1,2,3) d -'),('w+x'))		
		self.assertEqual(minFunc(3,'(2,3,4,5) d -'),('w\'x+wx\''))
		self.assertEqual(minFunc(4,'(0,5,7,8,9,10,11,14,15) d -'),('w\'xz+wx\'+wy+x\'y\'z\''))
		self.assertEqual(minFunc(4,'(0,1,2,6,8,9,10) d -'),('w\'yz\'+x\'y\'+x\'z\''))
                
if __name__=='__main__':
	unittest.main()
