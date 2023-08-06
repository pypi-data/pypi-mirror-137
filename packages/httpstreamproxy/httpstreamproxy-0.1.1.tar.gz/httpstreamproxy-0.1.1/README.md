# http streaming proxy
This project implements HTTP streaming proxy that can be used to proxy webcam streams.

To run this software you may use Docker or [PIP](https://realpython.com/what-is-pip/) package manager such as shown below

**Docker approach**
```
docker run -p 8080:8080 -e target_url="https://192.168.1.70/anonymous/jpeg/stream=0" -e verify="False" grro/httpstreamproxy:0.1.0
```

**PIP approach**
```
sudo pip install httpstreamproxy
```

After this installation you may start the proxy inside your python code or via command line using
```
sudo httpproxy --command listen --port 8080 --target_url https://192.168.1.70/anonymous/jpeg/stream=0 --verify False
```
Here, the proxy  will be bind to on port 8080. 

By running a *systemd-based Linux distribution* you may use the *register* command to register and start the proxy as systemd unit.
By doing this the proxy will be started automatically on boot. Starting the server manually using the *listen* command is no longer necessary.
```
sudo httpproxy --command register --port 8080 --target_url https://192.168.1.70/anonymous/jpeg/stream=0 --verify False
```  
