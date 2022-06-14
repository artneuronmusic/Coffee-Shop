# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.synced_folder ".", "/vagrant"
  #config.vm.network "forwarded_port", guest: 3306, host: 3306, host_ip: "127.0.0.1" # MySQL
  config.vm.network "forwarded_port", guest: 5432, host: 5432, host_ip: "127.0.0.1" # PostgreSQL
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"
  #config.vm.network "forwarded_port", guest: 8081, host: 8081, host_ip: "127.0.0.1"
  #config.vm.network "forwarded_port", guest: 8082, host: 8082, host_ip: "127.0.0.1"

  # Work around disconnected virtual network cable.
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get -qqy update

    # Work around https://github.com/chef/bento/issues/661
    # apt-get -qqy upgrade
    DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade

    # Install Packages
    apt-get -qqy install make zip unzip

    # Install Databases
    apt-get -qqy install postgresql

    # Install Languages
    apt-get -qqy install nodejs npm python3 python3-pip
    pip3 install --upgrade pip

    # Install NodeJS Modules
    su vagrant -c "cd /vagrant/frontend && npm install"
    npm install -g @ionic/cli
    
    # Install Python Modules
    apt-get -qqy install python3 python3-pip
    pip3 install flask packaging oauth2client passlib flask-httpauth
    pip3 install sqlalchemy flask-sqlalchemy psycopg2-binary bleach requests
    pip3 install -U flask-cors
    pip3 install Flask-Migrate
    #pip3 install -r requirements.txt

    su postgres -c 'createuser -dRS vagrant'
    # su vagrant -c 'createdb'
    # su vagrant -c 'createdb news'
    # su vagrant -c 'createdb forum'
    # su vagrant -c 'psql forum -f /vagrant/forum/forum.sql'

    vagrantTip=" [35m [1mThe shared directory is located at /vagrant\\nTo access your shared files: cd /vagrant [m"
    echo -e $vagrantTip > /etc/motd

    echo "Done installing your virtual machine!"
  SHELL
end

