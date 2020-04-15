Xterm -hold -title "Peer 1" -e "python3 peer.py init 2 4 5 30" &
Xterm -hold -title "Peer 3" -e "python3 peer.py  init 4 5 8 30" &
Xterm -hold -title "Peer 4" -e "python3 peer.py  init 5 8 9 30" &
Xterm -hold -title "Peer 5" -e "python3 peer.py  init 8 9 14 30" &
Xterm -hold -title "Peer 8" -e "python3 peer.py init 9 14 19 30" &
Xterm -hold -title "Peer 10" -e "python3 peer.py  init 14 19 2 30" &
Xterm -hold -title "Peer 12" -e "python3 peer.py  init 19 2 4 30" &
