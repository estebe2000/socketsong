sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip
sudo apt install -y libglib2.0-dev 
sudo apt install -y libgirepository1.0-dev
sudo apt install -y libcairo2-dev
sudo apt install -y mpg321
pip install -r requirements.txt
aplay -l
sudo mv /usr/share/alsa/alsa.conf /usr/share/alsa/alsa.old
sudo cp ./alsa.conf /usr/share/alsa/alsa.conf 
sudo cp ./asound.conf /etc/asound.conf

