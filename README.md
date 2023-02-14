# J.A.M.S - Just Another ML Server

gRPC service for serving tree based ML models and sklearn pipelines.

## OVERVIEW
The aim of this project is to allow users to serve trained ML models over gRPC. Place your models in **artefacts** folder and invoke **Deploy** endpoint.

## FEATURES
- Intended to be used as a separate process alongside the core application
- Easy to integrate
- Client controlled model deployments
- Model versioning

## USAGE
```
1. git clone
2. make setup
3. make start-server
```
Once the server is running, the client will be responsible for adding models.

If the user wants to use their own models, simply add the models in the **artefacts** folder.

Alternatively, if your models are stored in some third party storage, the client will be responsible for implementing the following logic:

- connecting to storage
- download model file to **artefacts** folder
- invoke **Deploy** endpoint with **model_name**

## EXAMPLE ARTEFACTS 

By default, there are a few model artefacts present in the artefacts folder. All of them are regressor models, trained on random data. The shape of training data was **(1000000, 125)**.