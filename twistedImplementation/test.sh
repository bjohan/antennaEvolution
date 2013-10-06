xterm -e "python server.py"&
server_pid=$!
sleep 0.2
xterm -e "python computeClientTest.py"&
compute_pid=$!
xterm -e "python workGeneratorClientTest.py"&
generator_pid=$!

read -p "press enter to kill server and clients"
ps aux | grep "python computeClientTest.py" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill
ps aux | grep "python workGeneratorClientTest.py" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill
ps aux | grep "python server.py" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill