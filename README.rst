=========
kube_test
=========


Goal of the project was to set up an application and deploy it to Kubernetes.

For this, a very small web scraper was written that fetches headline, date and category for the articles listed on https://www.zeit.de/ (example: https://www.zeit.de/news/index?date=2021-02-21) for the current day and some days before.

It is implemented as a FastApi (https://fastapi.tiangolo.com/) that runs a job every 60 seconds triggering the scraping logic.
There is a Swagger UI implemented where a endpoint can be used to fetch information about the last scrape (timestamp of scrape triggered and number of articles fetched). You can check this after deploying everything to the local Kubernetes cluster under the URL listed later.

The focus was put on a deployment of the app, so it is lacking some features (logging is mediocre and the data is saved nowhere).

The deployment itself consists of one replica of the scraping app and a service that routes traffic to the app itself.


Set up
===========

Build Docker image
docker build . --tag kube_test

Run the image locally
docker run --publish 8000:8000 --name kube kube_test

Deploy to cluster
kubectl apply -f kube_test.yaml

Check deployment
kubectl get deployments

Check logs (caution, very verbose!)
kubectl logs kube-test

Check running services
kubectl get services

Check if service is running and responding
http://localhost:30163/

Delete everything
kubectl delete -f kube_test.yaml


Note
====

This project has been set up using PyScaffold 3.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

Resources used:
https://docs.docker.com/get-started/kube-deploy/
https://matthewpalmer.net/kubernetes-app-developer/articles/service-kubernetes-example-tutorial.html#:~:text=What's%20the%20difference%20between%20a,running%20in%20the%20Kubernetes%20cluster.

TODO
====

- Improve logging
- Save data somewhere
- Remove unneeded packages from requirements.txt
- Clean up Dockerfile