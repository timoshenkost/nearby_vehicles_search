#!/usr/bin/env bash

chown -R nobody:nogroup /code

celery --app nearbyVehiclesSearch worker\
  --beat \
  --uid nobody --gid nogroup
