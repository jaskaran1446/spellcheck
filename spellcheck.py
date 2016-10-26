class Node(object):
	def __init__(self):
		self.value = None
		self.pointers = {}
		self.end = False
		

class Trie(object):
	def __init__(self):
		self.root = Node()
	
	def insertWord(self,word):
		self.insert(self.root,word)
	
	def insert(self,node,word):
		if len(word) == 0:
			node.end = True
			return			
		if word[:1] not in node.pointers:
			newnode = Node()
			newnode.value = word[:1]
			node.pointers[word[:1]] = newnode
			self.insert(newnode,word[1:])
		else:
			nextnode = node.pointers[word[:1]]
			self.insert(nextnode,word[1:])
	
	def present(self,word):
		return self.checkPresent(self.root,word)
	
	def checkPresent(self,node,word):
		if len(word) == 0 and node.end == True:
			return True
		if word[:1] in node.pointers:
			return self.checkPresent(node.pointers[word[:1]],word[1:])
		else:
			return False

	def prefix(self,word):
		prefixNode = self.findPrefixNode(self.root,word)
		if prefixNode is None:
			return None
		return self.dfs(prefixNode,word[:len(word)-1],[])
		
	
	def dfs(self,node,currword,words):
		currword += node.value
		if node.end:
			words.append(currword)
		if node.pointers is None:
			return words
		for val in node.pointers.values():
			words = self.dfs(val,currword,words)
		return words		
	
	def findPrefixNode(self,node,word):
		if len(word) == 0:
			return node
		if word[:1] not in node.pointers:
			return None
		else:
			return self.findPrefixNode(node.pointers[word[:1]],word[1:])
		
class SpellCheck(object):
	
	def __init__(self):
		self.t = Trie()
	
	def commonLetters(self,w1,w2):
		return len(set(w1) & set(w2))
		
	def commonPositions(self,word,sug):
		count=0
		for i in xrange(min(len(word),len(sug))):
			if word[i:i+1] == sug[i:i+1]:
				count += 1
		return count
	
	def setDictionary(self):
		fob = open("/home/jaskaran/Documents/OS/ref.txt")
		for line in fob:
			self.t.insertWord(line.rstrip())
		fob.close()
	 
	def checkSpelling(self):
		fin = open("/home/jaskaran/Documents/OS/sample-chk.txt")
		fout = open("/home/jaskaran/Documents/OS/sample-chk1.txt","w")
		for line in fin:
			words = line.split()
			for word in words:
				temp=""
				for char in word:
					if str(char).isalpha():
						temp += char
				word = temp.lower()
				if len(word) == 0:
					continue
				if not self.t.present(word):
					print "_________________________________________________________________________"
					print word + " not found."
					n = 2
					options = self.t.prefix(word[0:n])
					if options is None:
						choice = (int)(raw_input("No suggestions. Enter -1 to keep unchanged, -2 to type new word, -3 to to keep unchanged and add to dictionary:"))
						if choice == -2:
							word = raw_input("Enter replacement:")
						elif choice==-3:
							print "Word added as it is. Word added to dictionary."
							fdict = open("/home/jaskaran/Documents/OS/ref.txt","ab")
							fdict.write(word)
							fdict.close()
							self.t.insertWord(word)
					else:
						commonlist=[]
						for w in options:
							if self.commonLetters(w,word) > len(word)/2 and self.commonPositions(word,w) > 2:
								commonlist.append(w)
						if commonlist is not None:
							options=commonlist
						
						while True:
							n = n+1
							if n == len(word):
								break
							smalleroptions = self.t.prefix(word[0:n])
							if smalleroptions is not None and options != smalleroptions:
								options = smalleroptions
							else:
								break
						print "Possible alternatives:" 
						lim = 25
						if len(options) < 25:
							lim = len(options)
						for i in xrange(lim):
							print str(i) + ":" + options[i] 							
						ch = (int)(raw_input("Enter an index from the list to change, -1 to ignore once, -2 to type new word, -3 to keep unchanged and add to dictionary:"))
						if ch>=0 and ch<len(options):
							word = options[ch]
						elif ch == -2:
							word = raw_input("Enter replacement: ")
						elif ch == -1:
							print "Word added as it is."
						elif ch == -3:
							print "Word added as it is. Word added to dictionary."
							fdict = open("/home/jaskaran/Documents/OS/ref.txt","ab")
							fdict.write(word)
							fdict.close()
							self.t.insertWord(word)
						else:
							print "Invalid choice. Word added as it is."
				fout.write(word + " ") 
		print "Spell Check Completed. You can now open the corrected file."
		fin.close()
		fout.close()
		
s=SpellCheck()
s.setDictionary()
s.checkSpelling()
