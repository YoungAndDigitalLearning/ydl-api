# Setup server manual

## Install Python 3.6.5
https://www.rosehosting.com/blog/how-to-install-python-3-6-4-on-debian-9/
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm
sudo apt-get install -y libncurses5-dev  libncursesw5-dev xz-utils tk-dev
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
tar xvf Python-3.6.5.tgz
cd Python-3.6.5
./configure --enable-optimizations
make -j8
sudo make altinstall
python3.6

## upgrade pip3
sudo pip3.6 install --upgrade pip

## Install pipenv
sudo pip3.6 install pipenv==2018.5.18

## git
sudo apt install git-core
git config --global user.name "Sammy Shark"
git config --global user.email sammy@example.com

## mariadb
apt update && apt upgrade
apt install dirmngr
curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
apt update
sudo apt install mariadb-server

## create database
mysql -u root -pip
create database skb;

## nginx 
http://nginx.org/keys/nginx_signing.key
sudo apt-key add nginx_signing.key
cd /etc/apt/sources.list.d/
sudo vim nginx.list
## add to file 
deb http://nginx.org/packages/debian/ codename nginx
deb-src http://nginx.org/packages/debian/ codename nginx
sudo apt update
sudo apt install nginx
