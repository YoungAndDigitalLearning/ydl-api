# Setup server manual

Tutorial for setting up a new server for this or a similar project


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

## supervisor
sudo apt install supervisor

## htop
sudo apt install htop

# fix mysql 'mysql_config not found' -> mariadb_config
sudo apt install libmariadb-dev
sudo ln -s /usr/bin/mariadb_config /usr/bin/mysql_config
cd ... /ydl_api 
pipenv sync

## npm
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
cd repos/ydl-front/
npm install
npm run build

cd ~/repos/ydl-front
npm install
npm run build 

cd /usr/share/nginx/
sudo ln -s ~/repos/ydl-front/dist/ ydl

## symlink
sudo nginx -t
sudo service nginx restart
cd /etc/nginx
sudo mkdir modules-available
sudo mkdir modules-enabled
sudo mkdir sites-available
sudo mkdir sites-enabled

# config gunicorn
cd /etc/supervisor/conf.d
ls ~/.virtualenvs
// copy name of env
sudo vim /etc/supervisor/conf.d/gunicorn.conf

sudo vim /etc/supervisor/conf.d/webhook.conf

vim ~/config/hooks.json

mkdir ~/commands/webhooks
cd /home/username/commands/webhooks
vim /home/username/commands/webhooks/release-backend.sh

cd ydl_api/
sudo pipenv run python manage.py makemigrations
sudo pipenv run python manage.py migrate
cd ..
# restart django server
sudo supervisorctl restart gunicorn

sudo mkdir /var/log/gunicorn
sudo mkdir /var/log/webhook
sudo supervisorctl reread
sudo supervisorctl update

cd ~/
vim .bashrc
source ~/.bashrc

# webhook
sudo apt install webhook
