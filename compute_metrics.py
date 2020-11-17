import sys, os
from packet_parser import *

def get_data(node, ip):
	total_packets=len(ICMPs[node - 1])
	request_sent=0
	request_received=0
	replies_sent=0
	replies_received=0
	total_hops=0
	total_round_trip=0
	total_reply_delay=0
	total_request_sent=0
	total_request_received=0
	request_data_sent=0
	request_data_received=0
	for i in ICMPs[node - 1]:
		
		if str(i.source)==ip:
			if str(i.echo_type)=="reply":
				replies_sent+=1
				time_reply_sent=float(i.time)
				total_reply_delay+=time_request_received-time_reply_sent
			else:
				total_request_sent+=float(i.length)
				request_data_sent+=float(i.length)-42
				time_request_sent=float(i.time)
				request_sent+=1
			
		else:	
			if str(i.echo_type)=="reply":
				replies_received+=1
				time_reply_recieved=float(i.time)
				total_round_trip+=time_request_sent-time_reply_recieved
				total_hops+=129-i.ttl
			else:
				total_request_received+=float(i.length)
				request_data_received+=float(i.length)-42
				request_received+=1
				time_request_received=float(i.time)
	
	total_request_sent=int(total_request_sent)
	total_request_received=int(total_request_received)
	request_data_sent =int(request_data_sent)
	request_data_received=int(request_data_received)
	ave_round_trip=round((total_round_trip/request_sent)*1000*(-1),2)
	request_througput=round((total_request_sent)/(request_sent*ave_round_trip),1)
	request_goodput=round((request_data_sent)/(request_sent*ave_round_trip),1)
	ave_reply_delay=round((total_reply_delay/replies_sent*(-1))*1000000,2)
	ave_hops=round((float(total_hops)/float(replies_received)),2)
	
	with open('metrics.csv', 'a') as file:
		file.write('Node %d\n' % node)
		file.write('Echo Requests Sent, Echo Requests Recieved, Echo Replies Sent, Echo Replies Recieved\n')
		file.write('%d, %d, %d, %d\n' % (request_sent, request_received, replies_sent, replies_received))
		file.write('Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes)\n')
		file.write('%d, %d\n' % (total_request_sent, request_data_sent))
		file.write('Echo Request Bytes Recieved (bytes), Echo Request Data Recieved (bytes)\n')
		file.write('%d, %d\n\n' % (total_request_received, request_data_received))
		file.write('Average RTT (milliseconds),%.2f\n' % ave_round_trip)
		file.write('Echo Request Throughput (kB/sec),%.2f\n' % request_througput)
		file.write('Echo Request Goodput (kB/sec),%.2f\n' % request_goodput)
		file.write('Average Reply Delay (milliseconds),%.2f\n' % ave_reply_delay)
		file.write('Average Echo Request Hop Count,%.2f\n\n' % ave_hops)
	file.close()	
	
def compute():
	print "called compute function in compute_metrics.py"
	if os.path.exists('metrics.csv'):
		os.remove('metrics.csv')
	get_data(1, "192.168.100.1")
	get_data(2, "192.168.100.2")
	get_data(3, "192.168.200.1")
	get_data(4, "192.168.200.2")






