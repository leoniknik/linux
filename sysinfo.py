from mod_python import apache
import commands
 
def handler(req):
	# headers #########################################	
	real_ip = req.headers_in['X-Real-IP']
	nginx_version = req.headers_in['X-Ngx-Version']
	real_port = req.headers_in['X-Real-Port']
	nginx_ip = req.connection.remote_addr[0]
	nginx_port = req.connection.remote_addr[1]
	###################################################

	# LoadAverage #####################################
	load_average = commands.getoutput('uptime').split()
	try:	
		minute1 = load_average[8][:-1]
		minute5 = load_average[9][:-1]
		minute15 = load_average[10]
	except Exception:
		minute1 = load_average[7][:-1]
		minute5 = load_average[8][:-1]
		minute15 = load_average[9]
	if float(minute1) < 0.1:
		minute1 = "<font color=red>"+minute1+" </font>"
	if float(minute5) < 0.1:
		minute5 = "<font color=red>"+minute5+" </font>"
	if float(minute15) < 0.1:
		minute15 = "<font color=red>"+minute15+" </font>"
	####################################################

	# CPU ###########################################
	f = open('/tmp/files/actual')
	for i in range(0, 4):
		line = f.readline()
	cpu = line.split()
	user = float(cpu[0]) + float(cpu[1])
	system = cpu[2]
	iowait = cpu[3]
	idle = cpu[5]
	####################################################

	# iostat ###########################################
	line = f.readline()
	line = f.readline()
	line = f.readline().split()
	disc_info = ""
	while line:
    		device = line[0]
    		r_s = line[3]
    		w_s = line[4]
    		rkB_s = line[5]
    		wkB_s = line[6]
    		await = line[9]
    		util = line[13]
		disc_info += """<tr><td>"""+device+"""</td><td>"""+r_s+"""</td><td>"""+w_s+"""</td><td>"""+rkB_s+"""</td><td>"""+wkB_s+"""</td><td>"""+await+"""</td><td>"""+util+"""</td></tr>"""
    		line = f.readline().split()
		if len(line) < 2:
			break
	####################################################

	# network loading ##################################
	net_str = ""
	line = f.readline()
	line = f.readline()
	line = f.readline().split()
	while line:
		interface = line[0][:-1]
		r_bytes = line[1]
		r_packets = line[2]
		r_errs = line[3]
		r_drop = line[4]
		r_fifo = line[5]
		r_frame = line[6]
		r_compr = line[7]
		r_multi = line[8]
		t_bytes = line[9]
		t_packets = line[10]
		t_errs = line[11]
		t_drop = line[12]
		t_fifo = line[13]
		t_colls = line[14]
		t_carrier = line[15]
		t_compressed = line[16]
		net_str += """<tr><td bgcolor=lightgrey>"""+interface+"""</td><td>"""+r_bytes+"""</td><td>"""+r_packets+"""</td><td>"""+r_errs+"""</td><td>"""+r_drop+"""</td><td>"""+r_fifo+"""</td><td>"""+r_frame+"""</td><td>"""+r_compr+"""</td><td>"""+r_multi+"""</td><td bgcolor=lightgrey>"""+t_bytes+"""</td><td bgcolor=lightgrey>"""+t_packets+"""</td><td bgcolor=lightgrey>"""+t_errs+"""</td><td bgcolor=lightgrey>"""+t_drop+"""</td><td bgcolor=lightgrey>"""+t_fifo+"""</td><td bgcolor=lightgrey>"""+t_colls+"""</td><td bgcolor=lightgrey>"""+t_carrier+"""</td><td bgcolor=lightgrey>"""+t_compressed+"""</td></tr>"""
		line = f.readline().split()
		if len(line) < 2:
			break
	####################################################

	# df ###############################################
	df_str = ""
	list_file = []
	list_inode = []	
	line = f.readline()
	line = f.readline().split()
	while line:
		if len(line) < 2:
			break
		if line[5].find("/sys")!=-1 or line[5].find("/proc")!=-1 or line[5].find("/dev")!=-1:
			line = f.readline().split()
			continue
		else:
			fs = line[0]
			size = line[1]
			used = line[2]
			avail = line[3]
			use_procent = line[4]
			list_file.append(fs)
			list_file.append(size)
			list_file.append(used)
			list_file.append(avail)
			list_file.append(use_procent)
			line = f.readline().split()
	line = f.readline()
	line = f.readline().split()
	while line:
		if len(line) < 2:
			break
		if line[5].find("/sys")!=-1 or line[5].find("/proc")!=-1 or line[5].find("/dev")!=-1:
			line = f.readline().split()
			continue
		else:
			inodes = line[1]
			iused = line[2]
			ifree = line[3]
			iused_procent = line[4]
			mounted = line[5]
			list_inode.append(inodes)
			list_inode.append(iused)
			list_inode.append(ifree)
			list_inode.append(iused_procent)
			list_inode.append(mounted)
			line = f.readline().split()
	while len(list_file)>0:
		df_str += """<tr><td>"""+list_file[0]+"""</td><td>"""+list_file[1]+"""</td><td>"""+list_file[2]+"""</td><td>"""+list_file[3]+"""</td><td>"""+list_file[4]+"""</td><td>"""+list_inode[0]+"""</td><td>"""+list_inode[1]+"""</td><td>"""+list_inode[2]+"""</td><td>"""+list_inode[3]+"""</td><td>"""+list_inode[4]+"""</td></tr>"""
		list_file.pop(0)
		list_file.pop(0)
		list_file.pop(0)
		list_file.pop(0)
		list_file.pop(0)
		list_inode.pop(0)
		list_inode.pop(0)
		list_inode.pop(0)
		list_inode.pop(0)
		list_inode.pop(0)
	####################################################
	
	# state tcp ########################################
	line = f.readline()
	line = f.readline()
	line = f.readline().split()
	established = 0	
	syn_sent = 0
	syn_recv = 0
	fin_wait1 = 0
	fin_wait2 = 0
	time_wait = 0
	close = 0
	close_wait = 0
	last_ask = 0
	listen = 0
	closing = 0
	unknown = 0
	while line:
		if len(line) < 2:
			break
		elif line[5] == "ESTABLISHED":
			established+=1
		elif line[5] == "SYN_SENT":
			syn_sent+=1
		elif line[5] == "SYN_RECV":
			syn_recv+=1
		elif line[5] == "FIN_WAIT1":
			fin_wait1+=1
		elif line[5] == "FIN_WAIT2":
			fin_wait2+=1
		elif line[5] == "TIME_WAIT":
			time_wait+=1
		elif line[5] == "CLOSE":
			close+=1
		elif line[5] == "CLOSE_WAIT":
			close_wait+=1
		elif line[5] == "LISTEN":
			listen+=1
		elif line[5] == "LAST_ASK":
			last_ask+=1
		elif line[5] == "CLOSING":
			closing+=1
		elif line[5] == "UNKNOWN":
			unknown+=1
		line = f.readline().split()
	tcp_state = """<tr><td>"""+str(established)+"""</td><td>"""+str(syn_sent)+"""</td><td>"""+str(syn_recv)+"""</td><td>"""+str(fin_wait1)+"""</td><td>"""+str(fin_wait2)+"""</td><td>"""+str(time_wait)+"""</td><td>"""+str(close)+"""</td><td>"""+str(close_wait)+"""</td><td>"""+str(last_ask)+"""</td><td>"""+str(listen)+"""</td><td>"""+str(closing)+"""</td><td>"""+str(unknown)+"""</td></tr>"""
	####################################################

	### sockets ########################################
	line = f.readline()
	sock_str = ""
	while line:
		sock_str += line
		line = f.readline()
	####################################################
  	req.content_type = 'text/html'
 	req.write("""
	<html>
	<div align=center><p>Real user's ip: """+real_ip+"""</p>
	<p>Real port: """+real_port+"""</p>
	<p>Nginx ip: """+nginx_ip+"""</p>
	<p>Nginx port: """+str(nginx_port)+"""</p>
	<p>Nginx version: """+str(nginx_version)+"""</p></div>
	<hr>
	<table align=center border=1px>
   	<caption>LoadAverage</caption>
	<tr><td>1 minute</td><td>5 minute</td><td>15 minute</td></tr>
   	<tr><td>"""+minute1+"""</td><td>"""+minute5+"""</td><td>"""+minute15+"""</td></tr>
  	</table>
	<hr>
	<table align=center border=1px>
   	<caption>CPU</caption>
	<tr><td>user</td><td>system</td><td>iowait</td><td>idle</td></tr>
   	<tr><td>"""+str(user)+"""</td><td>"""+system+"""</td><td>"""+iowait+"""</td><td>"""+idle+"""</td></tr>
  	</table>
	<hr>
	<table align=center border=1px>
   	<caption>Disc loading</caption>
	<tr><td>Device</td><td>r/s</td><td>w/s</td><td>rkB/s</td><td>wkB/s</td><td>await</td><td>%util</td></tr>
   	"""+disc_info+"""
  	</table>
	<hr>
	<p align=center>Net loading</p>
	<table align=center border=1px>
   	<caption>Recieve&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Transmit</caption>
	<tr><td bgcolor=lightgrey>Interface</td><td>bytes</td><td>packets</td><td>errors</td><td>drop</td><td>fifo</td><td>frame</td><td>compressed</td><td>multicast</td><td bgcolor=lightgrey>bytes</td><td bgcolor=lightgrey>packets</td><td bgcolor=lightgrey>errors</td><td bgcolor=lightgrey>drop</td><td bgcolor=lightgrey>fifo</td><td bgcolor=lightgrey>colls</td><td bgcolor=lightgrey>carrier</td><td bgcolor=lightgrey>compressed</td></tr>
   	"""+net_str+"""
  	</table>
	<hr>
	<table align=center border=1px>
	<caption>Disc info</caption>
	<tr><td>File system</td><td>Size</td><td>Used</td><td>Available</td><td>Used%</td><td>Inodes</td><td>Inodes used</td><td>Inodes available</td><td>Inodes used%</td><td>Mounted on</td></tr>
	"""+ df_str +"""
	</table>
	<hr>
	<table align=center border=1px>
	<caption>TCP states</caption>
	<tr><td>ESTABLISHED</td><td>SYN_SENT</td><td>SYN_RECV</td><td>FIN_WAIT1</td><td>FIN_WAIT2</td><td>TIME_WAIT</td><td>CLOSE</td><td>CLOSE_WAIT</td><td>LAST_ASK</td><td>LISTEN</td><td>CLOSING</td><td>UNKNOWN</td></tr>
	"""+tcp_state+"""
	</table>
	<hr>
	<table align=center>
	<caption>SOCKETS</caption><tr><td><pre>
	"""+sock_str+"""</td><tr></pre>
	</table>
	</html>
	""")
	return apache.OK
	
