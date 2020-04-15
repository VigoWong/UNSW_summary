'''
To run the code ‘peer.py’, please simply run the script ‘test.sh’ in ‘assign.tar’ where content in the script is shown below:
xterm -hold -title "Peer 1" -e "python3 peer.py init 2 4 5 30" &
xterm -hold -title "Peer 3" -e "python3 peer.py  init 4 5 8 30" &
xterm -hold -title "Peer 4" -e "python3 peer.py  init 5 8 9 30" &
xterm -hold -title "Peer 5" -e "python3 peer.py  init 8 9 14 30" &
xterm -hold -title "Peer 8" -e "python3 peer.py init 9 14 19 30" &
xterm -hold -title "Peer 10" -e "python3 peer.py  init 14 19 2 30" &
xterm -hold -title "Peer 12" -e "python3 peer.py  init 19 2 4 30" &

Steps:

1. cd to the directory and type ‘chmod u+x test.sh’
2. run the script by typing ‘./test.sh’, then a DHT network is built
3. to join another peer, cd to the directory and type:
   ‘python3 peer.py join <PEER_ID> <KNOWN_PEER> <PING_INTERVAL>’
4. to kill a peer, simply press ctrl + c, or type ‘Quit’ for graceful leave
5. to store file, simply type ‘Store <FILE>’
6. to request file, simply type ‘Request <FILE>’

'''