import string
import itertools
import copy

def minFunc(numvar, stringIn):
	"""
    This python function takes function of maximum of 4 variables
    as input and gives the corresponding minimized function(s)
    as the output (minimized using the K-Map methodology),
    considering the case of Don’t Care conditions.

	Input is a string of the format (a0,a1,a2, ...,an) d(d0,d1, ...,dm)
	Output is a string representing the simplified Boolean Expression in
	SOP form.

	"""
	"""
	STEP 1 -->> Inputting the variables
	"""
	x=stringIn
	for i in x:
		x=x.replace('(','')
		x=x.replace(')','')

	a=x.find('d')

	nterms = [int(i) for i in x[:a].strip().split(',')]      #nterms = Normal terms
	if x[a+2]=='-':
		dterms =[]                                           #dterms = Don't care terms
	else:
		dterms = [int(i) for i in x[a+1:].strip().split(',')]


	"""
	STEP 2 -->> Generating primary groups
	"""
	aterms = nterms + dterms                                 #aterms = All terms
	aterms.sort()
	#print(aterms)
	pgr = {}                                                 #pgr = Primary grouped implicants on basis of number of 1's
	for x in aterms:
		d2b = bin(x)                                         #d2b = decimal2binary representation of number
		try:
			pgr[d2b.count('1')].append(d2b[2:].zfill(numvar))
		except Exception:
			pgr[d2b.count('1')]=[d2b[2:].zfill(numvar)]


	"""
	STEP 3 -->> Generating Prime Implicants
	"""

	def checker(a,b):
	    """
	    Function for checking if 2 minterms differ by 1 bit only
	    """
	    flag = False
	    for i in range(len(a)):
	    	if a[i]!=b[i] and flag == True:
	    		return False
	    	if a[i]!=b[i]:
	    		flag = True
	    return True
	  


	def mismatch(a,b):
		"""
		Function returns the bit where the two minterms mismatch.
		"""
		for c in range(len(a)):
			if a[c]!=b[c]:
				return c
		return None


	primimpl = set()        # Empty set of prime implicants. Will be used later

	while(True):
		another=pgr.copy()                   #Copy of pgr
		pgr={}
		lok=sorted(list(another.keys()))         #lok = list of keys -->> List of keys of dictionary 'another'
		stopcheck = True                         #A little roadblock if the while loop should stop or not
		count=0
		#noticks=set()
		ticks=set()                  # Empty set of all elements who are ticked down. Will be used later
		for a in range(len(lok)-1):
			for b in another[lok[a]]:                                       # Comparing the element in dictionary 'another'
				for c in another[lok[a+1]]:                                 # with the succeding element(s). 
					#print("b==",b,"c ==",c)
					if checker(b,c) == True:
						stopcheck = False                                   # Signifies that the loop should go on
						try:
							if (b[:mismatch(b,c)]+'-'+b[mismatch(b,c):]) not in pgr[count]:    
								pgr[count].append(b[:mismatch(b,c)]+'-'+b[mismatch(b,c)+1:])    # This basically adds another item to a list key....
							else:
								None
						except KeyError:
							pgr[count] = [b[:mismatch(b,c)]+'-'+b[mismatch(b,c)+1:]]            # ...and this adds element by creating a new key value
						ticks.add(b)
						ticks.add(c)                                                            #The elements which are combined are added to a new set
			count=count+1
		noticks = set(list(itertools.chain.from_iterable(another.values()))).difference(ticks)  #The main part .. the 'noticks' elements are those 
		primimpl = primimpl.union(noticks)         # Prime implicants = Union of implicants which were unticked
		if stopcheck == True:
			break

	"""
	STEP 4 -->> Creating Prime Implicant chart
	"""
	def converter(a):             
		"""
		 Function which returns the corresponding combinations of minterm
		"""
		ndash=a.count('-')
		if ndash == 0:
			return str(int(a,2))                                 # If dashes =0 then return the decimal value of 'a'
		x=[]                                                     # Creating a list
		for i in range(pow(2,ndash)):                            # of all combinations 
			x.append(bin(i)[2:].zfill(ndash))                    # of implicants. eg:100- : 8,9

		result=[]                                                # This list will be returned as the result.
		for i in range(pow(2,ndash)):
			copy=a                                            # Creating a copy of a as being a mutable object the values of list index can be changed.
			idx =-1
			for j in x[0]:                                      # Iterating one '-' at a time
				if idx != -1:
					idx = idx +1 + copy[idx+1:].find('-')        # This essentially gives out the index after the one found in else statement.That's why 1 is added.
				else:
					idx = copy[idx+1:].find('-')                 
				copy=copy[:idx]+j+copy[idx + 1:]                  
			result.append(str(int(copy,2)))                     #Finally when all dashes are analyzed the result is appended in a list.
			x.pop(0)                                            # After this the first element is removed and the cycle starts again.
		return result


	test={}                                                     # This is just a convenient dictionary which combines all the steps upto here.
	for i in list(primimpl):
		for j in converter(i):                                  # It removes all the don't care terms and gives a dictionary of following type for all minterms....
			if j not in dterms:
				try:
					test[i].append(str(j))                      # [[100-]:['8','9'],[1000]:['8']...........and so on]
				except KeyError:
					test[i]=[j]
				
	#print(test)

	y=sorted(list(set(list(itertools.chain.from_iterable(test.values())))))      # Converts a nested list to a normal list aka, flattening of list



	#***Chart maker***
	"""
	This prepares a prime implicant chart in form of a dictionary. Here every prime implicant is presentin form of keys and every corresponding
	block is present in form of values.
	"""
	chart={}
	for i in test:
	    for j in y:
	        if j in test[i]:
	            try:
	                chart[j].append(i)
	            except Exception:
	                chart[j]=[i]


	 
	def EPI(chart):              
		"""
		Function returns Essential Prime Implicants (EPIs) from EPI chart. 
		Logic : The key which has only one value in EPI chart is an EPI.
		"""
		l=[]
		for i,j in chart.items():
			if len(j) == 1 :
				l.append(i)
		return l	


	essenl=[]                                                       #This is an emty list.
	for i in EPI(chart):                                            #It will add append all the values correspong to EPI keys to it.
		essenl.append(chart[i])                                     #This will help in the final step.
	essenl = list(set(list(itertools.chain.from_iterable(essenl)))) #Again flattenig the list. In the middle set was used,to remove duplicate entries.


	def E2w(l):                            
	 	"""
	 	Functions returns word notation of prime implicants.
	 	"""
	 	x=''
	 	for i in range(len(l)):
	 		count = 0
	 		for j in l[i]:
	 			if j == '1':
	 				x = x + chr(ord('w')+count) + ''
	 			if j == '0':
	 				x = x + chr(ord('w')+count) + '\''
	 			count = count + 1
	 		if i != len(l)-1:
		 		x=x + ' + '
	 	return x

	def last(x):
		"""
		This function was just there as my program was showing every possible permutations in the output. This just breaks down a string
		and returns it in lexicographical order.
		"""
		y=x.split()
		y.sort()
		#print(y)
		for i in y:
			try:
				y.remove('+')
			except:
				pass

		s=''
		for i in y:
			s=s+i+'+'
		#print(s)
		s=s[:-1]
		return s
	return last(E2w(essenl))
		

