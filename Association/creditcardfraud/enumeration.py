
class Enum_Tree:
	def __init__(self):
		self.enum_tree = []
		self.enum_tree.append(set())

		self.support_table = {}
		self.height = 0

	def createC1(self,dataset):
		c1 = []
		for trans in dataset:
			for candidate in trans:
				if not [candidate] in c1:
					c1.append([candidate])
		c1.sort()
		return map(frozenset, c1)

	def cand_extend(self, dataset, minsupport):
		extension_list=[]
		used = {}
		if len(self.enum_tree[self.height]) == 0:
			c1 = self.createC1(dataset)
			for can in c1:
				extension_list.append(can)
		else:
			for i in range(len(self.enum_tree[self.height])):
				for j in range(i+1, len(self.enum_tree[self.height])):
					node =self.enum_tree[self.height][i] | self.enum_tree[self.height][j]
					used.setdefault(node, 0)
					if (used[node] == 1 or len(node) - len(self.enum_tree[self.height][i]) > 1): 
						continue
					else:
						extension_list.append(node)
						used[node] += 1
		del used
		cand_list,support_data = self.scan_dataset(dataset, extension_list, minsupport)
		if (len(cand_list) != 0):
			self.support_table.update(support_data)
			self.enum_tree.append(cand_list)
			self.height += 1
			return 1
		else:
			return 0

	def scan_dataset(self, dataset, candidate, minsupport):
		can_count={}
		support_data = {}
		for trans in dataset:
			for canset in candidate:
				if canset.issubset(trans):
					print type(canset)
					can_count.setdefault(canset, 0)
					can_count[canset] += 1
		num_transactions = float(len(dataset))
		for key in can_count:
			support = can_count[key]/num_transactions
			if support < minsupport:
				candidate.remove(key)
			support_data[key] = support
		return candidate,support_data

	def GenericEnumerationTree(self,dataset, minsupport):
		while True:
			if(self.cand_extend(dataset,minsupport)):
				continue
			else:
				break

	def gen_dependency(self, support_data, minconfidence):
		dependency = []
		for i in range(2, len(self.enum_tree)):
			for cand_set in self.enum_tree[i]:
				indiv_cand = [frozenset([candidate]) for candidate in cand_set]
				if (i > 2):
					#Do something when the candidate set is larger
					continue
				else:
					calc_confidence(cand_set, indiv_cand, self.support_table, minconfidence)

	def calc_confidence(cand_set, indiv_cand, support_data, minconfidence):
		for cand in indiv_cand:
			conf = support_data[cand_set]/support_data[cand_set-cand]
			if conf >= minconfidence:
				print cand_set - cand, '--->', cand, 'conf:', conf
				#Storre the rules somewhere


def load_dataset():
	return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

dataset = load_dataset() 
tree = Enum_Tree()
tree.GenericEnumerationTree(dataset, 0.5)
