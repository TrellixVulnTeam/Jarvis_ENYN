sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
sudo tar zxf Python-3.11.0.tgz
cd Python-3.11.0 || exit
sudo ./configure --enable-optimizations
sudo make -j 4
sudo make install