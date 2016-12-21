#!/bin/bash
#installs
sudo apt-get update
#sudo apt-get upgrade
sudo apt-get install python
sudo apt-get install apache2
sudo service apache2 stop
sudo apt-get install libapache2-mod-python
sudo service apache2 stop
sudo apt-get install nginx
sudo service nginx stop
sudo service apache2 stop
sudo apt-get install sysstat
#apache2
sudo rm /etc/apache2/apache2.conf
sudo cp apache/apache2.conf /etc/apache2
sudo rm /etc/apache2/ports.conf
sudo cp apache/ports.conf /etc/apache2
sudo rm /etc/apache2/sites-available/000-default.conf
sudo cp apache/000-default.conf /etc/apache2/sites-available
#nginx
sudo rm /etc/nginx/sites-available/default
sudo cp nginx/default /etc/nginx/sites-available
#python
sudo cp .htaccess /var/www/html
sudo chmod -R 777 .htaccess
sudo cp sysinfo.py /var/www/html
#cron
sudo chmod -R 777 sysinfo.py
sudo chmod -R 777 list
sudo chmod -R 777 script.sh
sudo cp list ~/
sudo cp script.sh ~/
crontab ~/list
sudo service nginx start
sudo service apache2 start

