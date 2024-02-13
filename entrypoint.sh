#!/bin/sh

until cd /opt/app
do
    echo "Waiting for server volume..."
done

until python -m studentflow.manage migrate
do
    echo "Waiting for postgres ready..."
    sleep 2
done

python -m studentflow.manage collectstatic --noinput

daphne -b 0.0.0.0 -p 8000 studentflow.project.asgi:application
