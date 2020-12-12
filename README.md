# Installation
1) Install docker
2) Install microk8s
```
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


# Setting Up
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
