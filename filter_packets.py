import os

def filter() :
	print 'called filter function in filter_packets.py'
	files = ('Node1', 'Node2', 'Node3', 'Node4')
	for f in files:
		if os.path.exists('data/' + f + '_filtered.txt'):
  			os.remove('data/' + f + '_filtered.txt')
		with open('data/' + f + '.txt', 'r') as fp:
			with open('data/' + f + '_filtered.txt', 'w') as op:
				line = fp.readline()
				while line:
					line = line.strip()
					if 'Echo' in line and ('request' in line or 'reply' in line): 
						op.write('No.     Time           Source                Destination           Protocol Length Info\n')
						op.write(line + '\n\n')
						fp.readline()
						temp_line = fp.readline().strip()
						while temp_line != '':
							op.write(temp_line + '\n')
							temp_line = fp.readline().strip()
						op.write('\n')
					line = fp.readline()
