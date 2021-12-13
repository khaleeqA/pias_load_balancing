import threading
import os
import Queue

def worker():
	while True:
		try:
			j = q.get(block = 0)
		except Queue.Empty:
			return
		#Make directory to save results
		os.system('mkdir '+j[1])
		os.system(j[0])

q = Queue.Queue()

#sim_end = 100000
sim_end = 10
link_rate = 10
mean_link_delay = 0.0000002
host_delay = 0.000020
queueSize = 240
#load_arr = [0.9, 0.8, 0.7, 0.6, 0.5]
load_arr = [ 0.8]
connections_per_pair = 1
meanFlowSize = 1138*1460
paretoShape = 1.05
flow_cdf = 'CDF_dctcp.tcl'

enableMultiPath = 1
perflowMP = 1
RealisticFailure = 1
sourceAlg = 'DCTCP-Sack'
#sourceAlg='LLDCT-Sack'
initWindow = 70
ackRatio = 1
slowstartrestart = 'true'
DCTCP_g = 0.0625
min_rto = 0.002
prob_cap_ = 5

switchAlg = 'Priority'
DCTCP_K = 65.0
drop_prio_ = 'true'
prio_scheme_ = 2
deque_prio_ = 'true'
keep_order_ = 'true'
prio_num_arr = [1, 8]
ECN_scheme_ = 2 #Per-port ECN marking
pias_thresh_0 = [759*1460, 909*1460, 999*1460, 956*1460, 1059*1460]
pias_thresh_1 = [1132*1460, 1329*1460, 1305*1460, 1381*1460, 1412*1460]
pias_thresh_2 = [1456*1460, 1648*1460, 1564*1460, 1718*1460, 1643*1460]
pias_thresh_3 = [1737*1460, 1960*1460, 1763*1460, 2028*1460, 1869*1460]
pias_thresh_4 = [2010*1460, 2143*1460, 1956*1460, 2297*1460, 2008*1460]
pias_thresh_5 = [2199*1460, 2337*1460, 2149*1460, 2551*1460, 2115*1460]
pias_thresh_6 = [2325*1460, 2484*1460, 2309*1460, 2660*1460, 2184*1460]
#checkCongestionFB = 1   ##khaliq

##khaliq

topology_spt = 4
topology_tors = 4
topology_spines = 4
topology_x = 1
FailureCase = 0
flowBender_ = 1

markedAckPkts_F = 1   ##khaliq
totalAckPkts = 1   ##khaliq
flowBender_T = 1    ##khaliq

ns_path = '/home/khaliq/ns-allinone-2.34/ns-2.34/ns'
sim_script = 'spine_empirical.tcl '

for prio_num_ in prio_num_arr:
	for i in range(len(load_arr)):

		scheme = 'unknown'
		if switchAlg == 'Priority' and prio_num_ > 1 and sourceAlg == 'DCTCP-Sack':
			scheme = 'pias'
		elif switchAlg == 'Priority' and prio_num_ == 1:
			if sourceAlg == 'DCTCP-Sack':
				scheme = 'dctcp'
			elif sourceAlg == 'LLDCT-Sack':
				scheme = 'lldct'

		if scheme == 'unknown':
			print 'Unknown scheme'
			sys.exit(0)

		#Directory name: workload_scheme_load_[load]
		directory_name = 'websearch_%s_%d' % (scheme,int(load_arr[i]*100))
		directory_name = directory_name.lower()
		#Simulation command
		cmd = ns_path+' '+sim_script+' '\
			+str(sim_end)+' '\
			+str(link_rate)+' '\
			+str(mean_link_delay)+' '\
			+str(host_delay)+' '\
			+str(queueSize)+' '\
			+str(load_arr[i])+' '\
			+str(connections_per_pair)+' '\
			+str(meanFlowSize)+' '\
			+str(paretoShape)+' '\
			+str(flow_cdf)+' '\
			+str(enableMultiPath)+' '\
			+str(perflowMP)+' '\
			+str(sourceAlg)+' '\
			+str(initWindow)+' '\
			+str(ackRatio)+' '\
			+str(slowstartrestart)+' '\
			+str(DCTCP_g)+' '\
			+str(min_rto)+' '\
			+str(prob_cap_)+' '\
			+str(switchAlg)+' '\
			+str(DCTCP_K)+' '\
			+str(drop_prio_)+' '\
			+str(prio_scheme_)+' '\
			+str(deque_prio_)+' '\
			+str(keep_order_)+' '\
			+str(prio_num_)+' '\
			+str(ECN_scheme_)+' '\
			+str(pias_thresh_0[i])+' '\
			+str(pias_thresh_1[i])+' '\
			+str(pias_thresh_2[i])+' '\
			+str(pias_thresh_3[i])+' '\
			+str(pias_thresh_4[i])+' '\
			+str(pias_thresh_5[i])+' '\
			+str(pias_thresh_6[i])+' '\
			+str(topology_spt)+' '\
			+str(topology_tors)+' '\
			+str(topology_spines)+' '\
			+str(topology_x)+' '\
                        +str(FailureCase)+' '\
                        +str(flowBender_)+' '\
			+str(markedAckPkts_F)+' '\
                        +str(totalAckPkts)+' '\
                        +str(flowBender_T)+' '\
                        +str('./'+directory_name+'/flow.tr')+'  >'\
			+str('./'+directory_name+'/logFile.tr')

		q.put([cmd, directory_name])



#####################################################
       
        
#if  RealisticFailure==1: 
 #   if FailureCase==1:  
  #      FailureStartTime = '$ns bandwidth $leaf($FailedLeaf) $spine($FailedLinkIndex) [expr $bw_torAgg/$FailureRatio]Mb bandwidth n0 n2 =  0.1Mb "duplex"'
   #     can_drive = True
#        puts = 'Debug: Reset bandwidth at $FailureStartTime to [expr $bw_torAgg/$FailureRatio] Mb!!'
 #   if  MultipleFailure==1: 
  #       FailureStartTime = '$ns bandwidth $leaf($SecondFailedLinkLeaf) $spine($SecondFailedLinkSpine) [expr $bw_torAgg/$FailureRatio]Mb "duplex"'  
        # print "yes"
   # if  FailureDuration > 0.0:
    #       FailureDuration = '$ns bandwidth $leaf($FailedLeaf) $spine($FailedLinkIndex) [expr $bw_torAgg]Mb "duplex"'
   # if  MultipleFailure==1: 
    #   FailureDuration = '$ns bandwidth $leaf($SecondFailedLinkLeaf) $spine($SecondFailedLinkSpine) [expr $bw_torAgg]Mb "duplex"'  




#PortionOfCode that will allow us to enable Realistic Failure Mechanism of creating partial failure on the run 

#if  RealisticFailure==1: 
   #   if  FailureCase==1:  
# 	## Partial failure
	# FailureStartTime = '$ns bandwidth $leaf($FailedLeaf) $spine($FailedLinkIndex) [expr $bw_torAgg/$FailureRatio]Mb' bandwidth n0 n2 =  0.1Mb 'duplex':
    #                 can_drive = True
  	# puts "Debug: Reset bandwidth at $FailureStartTime to [expr $bw_torAgg/$FailureRatio] Mb!! "
 	# if  MultipleFailure==1: 
	 #   ns at FailureStartTime "$ns bandwidth $leaf($SecondFailedLinkLeaf) $spine($SecondFailedLinkSpine) [expr $bw_torAgg/$FailureRatio]Mb 'duplex'" ; ## 18-Feb-17
	
	# if  FailureDuration > 0.0:
	  #  ns at [expr FailureStartTime+FailureDuration] "$ns bandwidth $leaf($FailedLeaf) $spine($FailedLinkIndex) [expr $bw_torAgg]Mb 'duplex'";

   # if  MultipleFailure==1: 
	#	ns at [expr FailureStartTime+FailureDuration] "$ns bandwidth $leaf($SecondFailedLinkLeaf) $spine($SecondFailedLinkSpine) [expr $bw_torAgg]Mb 'duplex'" ; ## 18-Feb-17
          
	


#Create all worker threads
threads = []
number_worker_threads = 20

#Start threads to process jobs
for i in range(number_worker_threads):
	t = threading.Thread(target = worker)
	threads.append(t)
	t.start()

#Join all completed threads
for t in threads:
	t.join()

