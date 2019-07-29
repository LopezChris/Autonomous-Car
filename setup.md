# Setup Development Environment

## AWS 

Choose a common keypair for each EC2 instance.

### MiNiFi - AWS EC2 Instance

Launch instance, Ubuntu 18.04, t2.large

Configure security group inbound: All traffic for My IP, All traffic for CDF Private IP

### CDF - AWS EC2 Instance

Launch instance, CentOS7, t3.2xlarge, 16GB RAM or more, Port 10080 open for web UI, Port 8787 open for CoAP

Configure security group inbound: All traffic for My IP, All traffic for CDH Private IP, All traffic for MiNiFi C++ Private IP

### CDH - AWS EC2 Instance

Launch instance, CentOS7, m5a.4xlarge, 16vCPUs/64GB RAM, Root volume OS disk size 100GB, EBS General Purpose (Gp2) SSD 1000GB with 3000 IOPS for Docker device disk

Configure security group inbound: All traffic for My IP, All traffic for CDF Private IP

## Cloudera Platform Installations

### MiNiFi C++



### CDF 

On your local machine terminal, run the commands to install CDF on remote server:

~~~bash
sudo su -
yum install -y git
git clone https://github.com/jdye64/cdf-demos.git
cd cdf-demos/ansible && vi host
# after updating host file, run for cdf installation
ansible-playbook -i host efm-10-install.yml
~~~

### CDH + CDSW

SSH into cloud instance:

~~~
ssh -i /path/to/filename.pem centos@{public-dns}
~~~

Execute commands for CDH installation:

~~~bash
sudo su -
yum install -y git
git clone https://github.com/fabiog1901/OneNodeCDHCluster.git
cd OneNodeCDHCluster
chmod +x setup.sh

# find docker device mount point with 1000GB
lsblk
# insert result from lsblk into docker-device
./setup.sh aws cdsw_template.json /dev/{docker-device}
~~~

Cloudera Manager can be logged in at `{cdh-public-dns}:7180`
