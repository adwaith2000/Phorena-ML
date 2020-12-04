# Softwares Used
1. Mosquitto
2. Telegraf
3. InfluxDB
4. Grafana
5. Docker
6. Kubernetes
7. Calico

## Mosquitto
MQTT is a publish-subscriber network protocol that transports
messages between devices.

## Telegraf
* Telegraf is a plugin-driven server agent for collecting and
sending metrics and events from databases, systems and IoT sensors.
* Telegraf is written in Go and compiles into a single binary
with no external dependencies and requires a very minimal memory footprint

### Types of Plugins
* Inputs: Gathers metric from the source
* Outputs: Sends metric to the database
* Aggregators: Aggregators emit new aggregate metrics based on the metrics collected by the input plugins
* Processors: Process metrics as they pass through and immediately emit results based on the values they process

## InfluxDB
InfluxDB is a timeseries database. ie, each record will have a timestamp associated to it. 

### Features of InfluxDB
* Fast ingression rate over time  
Relational databases may need to re-index data for fast access. As our indexes grow our databases slows down. InfluxDB is optimized to retain the ingression rate over time
* Simultaneous read and write
* Retention policies
Our data can be stored infinitely or can be removed periodically
* Continuous Queries

### Terminologies
* Database: Hosts collection of measurements
* Measurements: Similiar to SQL Tables
* Tags: Tags are indexed. So they are optimized to group by in queries. Can be used to store metadata like location of measurement
* Fields: Fields are used to store data we measure. Eg: the value of temperature reading
* Retention Policies: How long do we want to keep data. Default is "autogen" which keeps data forever unless we manually delete it
* Point: Set of fields that has the same timestamp. Equivalent to a row or unique entry in table

## Docker
Docker is used to deliver software in packages called containers. Each container can be isolated from one another and bundle their own software, libraries and configuration files. Each software in containers will ship with all the dependencies it has so that its functionality remains same on any docker supported platform.
Earlier if many people wanted to work on a project, it was very difficult when it comes to the deployment portion as it was challenging to combine these and deploy as a whole. With the advent of docker, all the portions got containerized and this enabled them to be deployed separately.


## Kubernetes
Kubernetes is an platform for container orchestration. It can be used for deployment, scaling, and management of applications. A cluster of kubernetes will have a master node where its API server is located and many slave nodes. Applications in a cluster run on virtualised containers called pods. Each pod is created from deployment file which describe where to pull the image of the appication from, the number of pods it should run on and default environment variables, if any etc. Some applications can also create services which will let them listen to certain ports to communcicate with each other.  

In Kubernetes, there are multiple servers and pods inside each server. A pod is a collection of dockers. There will be a master that redirects the requests to the services. These services then take up the request to the pods inside servers. Pods are a set of dockers along with some Kubernetes files. It is the service that decides which pod is to be chosen as per the availability. Even if one pod fails, there are multiple other pods too. Even if one server fails, there are multiple other servers too. 


## Calico
Calico is an open source networking and network security solution for containers, virtual machines, and native host-based workloads. Calico supports a broad range of platforms including Kubernetes, OpenShift, Docker EE, OpenStack, and bare metal services.
Calico network policy engine formed the original reference implementation of Kubernetes network policy during the development of the API. By using multiple enforcement points Calico policies can provide a run-anywhere solution to implement a zero trust network for your Kubernetes cluster.
