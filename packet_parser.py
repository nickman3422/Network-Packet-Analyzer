import os
import re

ICMPs = []

class ICMP:
	def __init__(self, time, source, destination, length, ttl, echo_type):
		self.time = time
		self.source = source
		self.destination = destination
		self.length =  length
		self.ttl = ttl
		self.echo_type = echo_type

	def pretty_print(self):
		return 'ICMP(Time: %s,\nSource: %s,\nDestination: %s,\nLength: %d,\nTTL: %d,\nEcho Type: %s)' % (self.time, self.source, self.destination, self.length, self.ttl, self.echo_type)
	
	def __repr__(self):
		return 'ICMP(%s, %s, %s, %d, %d, %s)' % (self.time, self.source, self.destination, self.length, self.ttl, self.echo_type)

def parse():
	print 'called parse function in packet_parser.py'
	new_files = ('Node1_filtered.txt', 'Node2_filtered.txt', 'Node3_filtered.txt', 'Node4_filtered.txt')
	node_count = 0
	global ICMPs
	for f in new_files:
		data = []
		ICMPs.append([])
		with open('data/' + f, 'r') as fp:
			line = fp.readline()
			while line:
				header = re.split('\s+', fp.readline())
				fp.readline()
				data = []
				hex_chunk = fp.readline()
				hex_total = ''
				while hex_chunk.strip():
						hex_total += hex_chunk[4:53].strip()
						hex_chunk = fp.readline()
				new_string = ''
				for s in hex_total.split():
						new_string += s
				hex_list = [new_string[i:i + 2] for i in range (0, len(new_string), 2)]
				ip_src = '%d.%d.%d.%d' % (int(hex_list[26], 16), int(hex_list[27], 16), int(hex_list[28], 16), int(hex_list[29], 16))
				ip_dst = '%d.%d.%d.%d' % (int(hex_list[30], 16), int(hex_list[31], 16), int(hex_list[32], 16), int(hex_list[33], 16))
				ttl = int(hex_list[22], 16)
				echo_type = 'request' if int(hex_list[34], 16) == 8 else 'reply'
				ICMPs[node_count].append(ICMP(header[1], ip_src, ip_dst, int(header[5]), ttl, echo_type))
				line = fp.readline()
		node_count += 1
