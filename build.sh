apt-get update
apt-get install -y ffmpeg python3.10 python3.10-venv python3.10-dev

# Set python 3.10 as default
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

python3 --version

pip install -r requirements.txt
