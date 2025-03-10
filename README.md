# podInfo
A lightweight Python API that renders Kubernetes Pod and Node data in a clean web interface.
 - exposes /v1/whoami to display the pod and node info.
 - exposes /health/local for kubelet health checks.



#### Development (non-prod use-case only)

- start minikube cluster
``` 
    minikube start
    eval $(minikube docker-env)
```
Build the image using:

```docker build -t system-info:1.0.0 -f Dockerfile .```

Deploy the service using the provided bare-minimum deployment.yaml

``` kubectl apply -f ./deployment/* ```

check status of pods via:

```kubectl get pods ```

Port-forward to access the systeminfo service like this:

```kubectl port-forward deployments/system-info-service 8080:8080```

Open a Browser tab and then access the url as below :
```http://localhost:8080/v1/whoami```

### Production 

Image is publicly available at dockerhub `inspiremirnal/system-info`
Deploy using `kubectl apply -f deployment/*`
Access : `kubectl port-forward deployments/system-info-service 8080:8080`

#### Example

![img](assets/system-info.png)

