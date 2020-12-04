# Setting up the Kubernetes cluster
## Installation
1) Install docker
2) Install microk8s
```sh
sudo snap install microk8s --classic --channel=1.18/edge
```
If already installed remove it by running
```
microk8s.reset
sudo snap remove microk8s
```

3) Make sure microk8s & docker is running
```
sudo snap start microk8s
```
```
sudo systemctl start docker

OR

sudo service start docker
```

Add your current user to microk8s user group so that you now longer have to use sudo on subsequent commands
```
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
su - $USER
```


4) Check the status
```
microk8s status --wait-ready
```

5) Test the cluster by deploying nginx
```
microk8s kubectl create deployment nginx --image=nginx
```
Make sure nginx pod is in RUNNING state (takes 2-5 mts)
```
microk8s kubectl get pods
```

6) Enable add-ons
```
microk8s enable dashboard dns storage
```
* Dashboard: microk8s provides us a GUI dashboard to manage our cluster
* DNS: Each pod on the cluster runs on its virtual enviroment. So if we need them to communicate with each other we may have to use the local/external IPs of the container unless we use a DNS. If the DNS add-on is enabled queries like http://grafana:3000/ will automatically resolve to access the 3000 port of grafana service.
* Storage: InfluxDB needs to access the storage of the machine to save data


## Setting Up
```
git clone https://github.com/adwaith2000/Phorena-ML
cd Phorena-ML
chmod +x install.sh
./install.sh
```

# Testing set up
1)
```
microk8s kubectl get pods --all-namespaces
```
Make sure all pods are RUNNING (It may take time upto 15mts)

2) Open Grafana
Run
```
microk8s kubectl get services
```
Open the CLUSTER-IP:PORT in a web browser and make sure you get to Grafana login page
```