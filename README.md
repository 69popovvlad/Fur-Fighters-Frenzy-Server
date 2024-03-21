### Before using run command
```
pip install docker
pip install flask
```
to install docker dependency

### Run with
```
python src/main.py
```

### Server setup
```
apt install python3-pip
apt install python3.11-venv
cd project_directory
python3 -m venv venv
```

### Deploy and run
from root directory of this project
```
make deploy DEPLOY_REMOTE=root@<hosting ip>
```

#### offtop:
virtual environment creating
```
source project_directory/venv/bin/activate
```