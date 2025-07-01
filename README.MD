# active

## about

`active` is a relatively simple python script that acts as a port scanner for TCP and UDP protocols. `psutil` is used here as a means to find out the exact name of the proccess that's listening for connection by using its [PID](https://en.wikipedia.org/wiki/Process_identifier).

attached is an example of the script. a minecraft server is running on my local machine and tried to search for ports listening on 25560-25570. It managed to successfully find 25565, the port minecraft uses, and correctly identified it as a java process. ![Alt text](/example.png)

## how-to (linux)
- ensure that python is installed on your distro 
- start a venv in a folder by running ```python3 -m venv ./``` or any folder of your choosing
- change the source to the venv by running ```source bin/activate```
- ensure the script is inside the venv folder
- install the dependency by running ```pip3 install -r requirements.txt``` or ```pip3 install psutil```

## how-to (windows)
- ensure that python is [installed](https://www.python.org/downloads/release/python-3131/)
- ensure that the dependency is installed ```pip3 install -r requirements.txt``` or ```pip3 install psutil```
- as windows does not handle packages like linux does, the project can probably be just executed in powershell or vsc terminal by running active.py.

## commands
- to let active do its thing, do ```python3 ./active.py```

## note
since the UDP protocol involves no actual handshake, it's best to either `sudo` the script, or start the script with elevated privileges on windows when looking for UDP ports.