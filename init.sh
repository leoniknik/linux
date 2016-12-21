#!/bin/bash
#installs
sudo apt-get update
sudo apt-get install python
sudo apt-get install apache2
sudo apt-get install libapache2-mod-python
sudo apt-get install nginx
sudo apt-get install sysstat
#apache2
sudo cp apache/apache2.conf /etc/apache2
sudo cp apache/ports.conf /etc/apache2
sudo cp apache/000-default.conf /etc/apache2/sites-enabled
#nginx
sudo cp nginx/default /etc/nginx/sites-enabled
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

