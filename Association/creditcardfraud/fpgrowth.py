#Projected Database: save the transactions that contain the candidate set, so that when you extend it, it gets faster running down the lis
def load_dataset():
	return [['b', 'a'], 
	['a','c','b'], 
	['b','c','a','e','d'], 
	['d','a','b'], 
	['a','e','b'], 
	['a','c','d'], 
	['a','c','e'], 
	['e','c','d'],
	['c','e'],
	['b']]

def createC1(dataset):
		c1 = []
		for trans in dataset:
			for candidate in trans:
				if not [candidate] in c1:
					c1.append([candidate])
		c1.sort()
		return map(frozenset, c1)

def RecursiveFPGrowth(dataset, num_transactions, prefix, cand_list, support_data, minsupport):

	data_subset={}
	used = []
	for cand in cand_list:
		print 'cand is %s' % cand
		can_count=0
		for trans in dataset:
			if cand.issubset(trans):
				node = prefix | cand
				data_subset.setdefault(node, list())
				data_subset[node].append(trans)
				can_count += 1

		support = can_count/num_transactions
		print 'Support is %s' % support
		support_data[node] = support
		if support > minsupport:
			
			#Extend candidate list by one somehow, pass in transaction table subset
			cand_list_subset = cand_list[cand_list.index(cand)+1:len(cand_list)]
			
			if len(cand_list_subset) > 0: #This might be the cause of it skipping a candidate 
				RecursiveFPGrowth(data_subset[node], num_transactions, node, cand_list_subset, support_data, minsupport)
		else:
			print 'Support not high enough'
	print 'Exiting recursive loop\n'
	return


dataset = load_dataset()
cand_list = createC1(dataset)
support_data = {}
num_transactions = float(len(dataset))
RecursiveFPGrowth(dataset, num_transactions, frozenset(), cand_list, support_data, 0.3)
		
for key in support_data:
	print 'Key (%s) : %s' % (key, support_data[key])