#!/bin/bash
exec celery flower --app hotelbooking --workdir src
