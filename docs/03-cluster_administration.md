# Kubernetes cluster administration
## Configuration files
The `k8s/` folder of this repo contains configuration files.  
To create a cluster resource we can run the following command on a .yaml file
```sh
>> microk8s kubectl create -f /path/to/file.yaml
```
To change a created resource, after changing its .yaml file use
```sh
>> microk8s kubectl apply -f /path/to/file.yaml
```

**Subdirectories**
* `deployment`: Deployment files define the applications to be installed on cluster. Each deployment file will specify which Docker image to pull from and how many replicas of the pod must be created. If the has some pre-configuration for eg. telegraf.conf or environment variables like database passwords, it should be defined in the deployment file

* `configmap`: These are the configuration files for telegraf (defining input & output) and grafana (influxdb credentials)

* `persistentvolumeclaim`: This is used by InfluxDB to request permenant storage

* `secret`: Here we store the environment variables that is required by the pods. Due to their sensitive nature these are base-64 encrypted. To change these values we can use microk8s dashboard or subsitute the base64 equivalent of the new value

* `service`: Applications need to be run as services to let other applications/users to connect. Service files define the ports these applications run on and the ports they forward to the user

## Cluster Info
```sh
>> microk8s kubectl cluster-info

# OUTPUT
Kubernetes master is running at https://127.0.0.1:16443
Heapster is running at https://127.0.0.1:16443/api/v1/namespaces/kube-system/services/heapster/proxy
CoreDNS is running at https://127.0.0.1:16443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
Grafana is running at https://127.0.0.1:16443/api/v1/namespaces/kube-system/services/monitoring-grafana/proxy
InfluxDB is running at https://127.0.0.1:16443/api/v1/namespaces/kube-system/services/monitoring-influxdb:http/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

## Nodes
Each cluster will have a master node where the core kubernetes API server resides and some slave
nodes which will contact kubernetes through this API
```sh
>> microk8s kubectl get nodes

# OUTPUT
NAME     STATUS   ROLES    AGE   VERSION
hp-lap   Ready    <none>   34d   v1.18.12

```

## Deployments
```sh
>> microk8s kubectl get deployments
# OUTPUT
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
grafana     1/1     1            1           34d
influxdb    1/1     1            1           14d
mosquitto   1/1     1            1           34d
nginx       1/1     1            1           34d
telegraf    1/1     1            1           14d


>> microk8s kubectl describe deployment telegraf
# OUTPUT
Name:                   telegraf
Namespace:              default
CreationTimestamp:      Fri, 20 Nov 2020 21:06:51 +0530
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=telegraf
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        5
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=telegraf
  Containers:
   telegraf:
    Image:      telegraf:1.10.0
    Port:       <none>
    Host Port:  <none>
    Environment Variables from:
      telegraf-secrets  Secret  Optional: false
    Environment:        <none>
    Mounts:
      /etc/telegraf/telegraf.conf from telegraf-config-volume (ro,path="telegraf.conf")
  Volumes:
   telegraf-config-volume:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      telegraf-config
    Optional:  false
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
OldReplicaSets:  <none>
NewReplicaSet:   telegraf-794bc96857 (1/1 replicas created)
Events:          <none>
```

## Services
```sh
>> microk8s kubectl get services
#OUTPUT
NAME         TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
grafana      LoadBalancer   10.152.183.19    <pending>     80:32056/TCP        34d
influxdb     ClusterIP      10.152.183.211   <none>        8086/TCP            34d
kubernetes   ClusterIP      10.152.183.1     <none>        443/TCP             34d
mosquitto    ClusterIP      10.152.183.49    <none>        1883/TCP,9001/TCP   34d
telegraf     NodePort       10.152.183.252   <none>        8125:30546/UDP      34d
# Here grafana runs on 80th port in its pod and 32056 port of the machine that we run the
# cluster on

>> microk8s kubectl describe service telegraf
# OUTPUT
Name:                     telegraf
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 app=telegraf
Type:                     NodePort
IP:                       10.152.183.252
Port:                     <unset>  8125/UDP
TargetPort:               8125/UDP
NodePort:                 <unset>  30546/UDP
Endpoints:                10.1.85.14:8125
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>

```

## Pods
```sh
>> microk8s kubectl get pods
# OUTPUT
NAME                         READY   STATUS    RESTARTS   AGE
grafana-557d5bcbff-g55ft     1/1     Running   22         34d
influxdb-5f4f4f8f44-9hphr    1/1     Running   6          14d
mosquitto-6854cc448f-zkq7m   1/1     Running   22         34d
nginx-f89759699-g6bfl        1/1     Running   22         34d
telegraf-794bc96857-sth9w    1/1     Running   6          14d

>> microk8s kubectl describe pod mosquitto-6854cc448f-zkq7m
# OUTPUT
Name:         mosquitto-6854cc448f-zkq7m
Namespace:    default
Priority:     0
Node:         hp-lap/192.168.43.63
Start Time:   Sat, 31 Oct 2020 12:45:58 +0530
Labels:       io.kompose.service=mosquitto
              pod-template-hash=6854cc448f
Annotations:  kompose.cmd: kompose convert
              kompose.version: 1.21.0 (992df58d8)
Status:       Running
IP:           10.1.85.12
IPs:
  IP:           10.1.85.12
Controlled By:  ReplicaSet/mosquitto-6854cc448f
Containers:
  mosquitto:
    Container ID:   containerd://b3966df5a96348beaab3cdf5c311e4960545bc207453beeb5659cab773b42be9
    Image:          eclipse-mosquitto
    Image ID:       docker.io/library/eclipse-mosquitto@sha256:37375ab459a27275a3af26570b4d9146ea8ee1b94246656a34f509d6f147c301
    Ports:          1883/TCP, 9001/TCP
    Host Ports:     0/TCP, 0/TCP
    State:          Running
      Started:      Fri, 04 Dec 2020 17:55:38 +0530
    Last State:     Terminated
      Reason:       Unknown
      Exit Code:    255
      Started:      Fri, 04 Dec 2020 13:08:17 +0530
      Finished:     Fri, 04 Dec 2020 17:55:05 +0530
    Ready:          True
    Restart Count:  22
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-bgvhb (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  default-token-bgvhb:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-bgvhb
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:          <none>
```

### Executing commands on a pod
Sometimes we may need to run some commands on a pod. For eg. we may need to access the influx shell
to run some queries.  
To execute a command on a pod we can use
```sh
microk8s kubectl exec -it podname -- command
```
For eg:
```sh
>> microk8s kubectl exec -it influxdb-5f4f4f8f44-9hphr -- /bin/bash
# OUTPUT
root@influxdb-5f4f4f8f44-9hphr:/# 
```

## To see all the resources in a cluster
```sh
microk8s kubectl get all --all-namespaces
```