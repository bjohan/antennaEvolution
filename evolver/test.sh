xterm -e "python ../grid/server.py"&
server_pid=$!
sleep 0.2
xterm -e "python antennaWorkGenerator.py even"&
sleep 0.2
xterm -e "python necComputeClient.py"&
sleep 0.2
xterm -e "python necComputeClient.py"&
sleep 0.2
xterm -e "python necComputeClient.py"&
sleep 0.2
xterm -e "python necComputeClient.py"&
sleep 0.2
xterm -e "python necComputeClient.py"&
sleep 0.2
xterm -e "python necComputeClient.py"&
sleep 0.2
xterm -e "python necComputeClient.py"&
sleep 0.2
xterm -e "python necComputeClient.py"&
sleep 0.2
xterm -e "python necComputeClient.py"&

read -p "press enter to kill server and clients"
ps aux | grep "python necComputeClient" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python necComputeClient" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python necComputeClient" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python necComputeClient" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python necComputeClient" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python necComputeClient" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python necComputeClient" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python necComputeClient" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python necComputeClient" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python antennaWorkGenerator.py" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python ../grid/server.py" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
