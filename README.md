# simple-terminal-chatserver
A simple POC for terminal chatserver in python

## Pre-requisite:
- Ensure `openssl` is installed and working on Unix-ish terminal for both server and clients.

## Server setup:
1. Generate SSL certificate and private key for encryption:
  ```bash
  openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes
  ```
2. Start the chat server
  ```bash
  python server.py
  ```
3. Take note on the server's IP on the LAN. The startup logs shows something like:
    `Server listening to 192.168.1.XXX:8384`

## Client connection:
1. To connect to the chat server, at terminal input:
   ```bash
   openssl s_client -connect 192.168.1.XXX:8384 -quiet
   ```
   Make sure the IP address is the correct server's IP
2. To play around, have multiple different devices connected to the server and begin chatting!
