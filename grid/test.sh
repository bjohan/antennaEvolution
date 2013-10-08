xterm -e "python server.py"&
server_pid=$!
sleep 0.2
xterm -e "python workGeneratorClientTest.py even"&
sleep 0.2
xterm -e "python workGeneratorClientTest.py odd"&
sleep 0.2
xterm -e "python computeClientTest.py"&
sleep 0.2
xterm -e "python computeClientTest.py"&
sleep 0.2
xterm -e "python computeClientTest.py"&
sleep 0.2
xterm -e "python computeClientTest.py"&

read -p "press enter to kill server and clients"
ps aux | grep "python computeClientTest.py" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python computeClientTest.py" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python computeClientTest.py" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python computeClientTest.py" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python workGeneratorClientTest.py" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
ps aux | grep "python server.py" | grep -v xterm | grep -v grep | cut -f1-2 | nawk {'print $2'} | xargs kill -9
