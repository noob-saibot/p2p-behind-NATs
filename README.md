# p2p-behind-NATs
Peer to peer connection for users behind NATs.

####Signal_server.py
Talking name isn't it? This is Signal server for saving information about Message server and providing info about it to Clients.
Signal server involve only in process peer finding, not a proxy like TURN.

####Mess_server.py
This server chatting with STUN and Signal servers. Clients will connect on it through NAT.

####Mess_client.py
Directly the client. Nothing else.

####Instruction:
Starting Signal server with **public IP**.
Message server and client should be started with parameters of Signal server's ip. 
Also for client we should describe ID of message server.

####Howto
1. After starting message server are connecting to STUN server.
2. STUN serv describe in response info (Type of NAT, public IP, public port).
3. This information retranslated to Signal server. Sign_s writing this info to log file.
4. Finally Mess_s recieving positive response from Sign_s
and starting support connection between them for saving public port number. If port are changing again STUN-Sign_s-Connection support.
5. Client initiate request to Sign_s like "Where server Number", in response message it get info for connection.
6. Client connected to Mess_s.
