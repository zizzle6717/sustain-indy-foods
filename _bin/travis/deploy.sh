#!/bin/bash

set -e

CURRENT_BRANCH=${TRAVIS_PULL_REQUEST_BRANCH:-$TRAVIS_BRANCH}
echo "Current branch is $CURRENT_BRANCH"

# TRAVIS_BRANCH represents the destination branch for PR builds
if [ ! -z "$TRAVIS_PULL_REQUEST_BRANCH" ]; then
  echo "Destination branch is $TRAVIS_BRANCH"
fi

# Only build the docker images when the source branch is stage or master
if [[ ("$CURRENT_BRANCH" != "stage") && ("$CURRENT_BRANCH" != "master") ]]; then
  echo "Skipping post build stage."
  exit 0
fi

[[ "$CURRENT_BRANCH" = "stage" ]] && SUFFIX="-stage" || SUFFIX=""

docker build -t riliadmin/sustain-indy-foods-client$SUFFIX:latest -t riliadmin/sustain-indy-foods-client$SUFFIX:$GIT_SHA -f ./client/Dockerfile --build-arg NODE_VERSION=${NODE_VERSION} ./client
docker build -t riliadmin/sustain-indy-foods-server$SUFFIX:latest -t riliadmin/sustain-indy-foods-server$SUFFIX:$GIT_SHA -f ./server/Dockerfile --build-arg NODE_VERSION=${NODE_VERSION} ./server
docker push riliadmin/sustain-indy-foods-client$SUFFIX:latest
docker push riliadmin/sustain-indy-foods-client$SUFFIX:$GIT_SHA
docker push riliadmin/sustain-indy-foods-server$SUFFIX:latest
docker push riliadmin/sustain-indy-foods-server$SUFFIX:$GIT_SHA
kubectl apply -f k8s
kubectl set image deployments/server-deployment server=riliadmin/sustain-indy-foods-client:$GIT_SHA
kubectl set image deployments/server-deployment server=riliadmin/sustain-indy-foods-server:$GIT_SHA