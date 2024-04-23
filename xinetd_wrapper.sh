#!/bin/bash
# setup limits
LIMIT_NPROC=
LIMIT_MEM=
. /opt/scripts/service_ulimit.sh

dir=$(dirname $0)
cd $dir
exec timeout -s9 300s uwsgi --protocol=http --plugin python3 -p 1 -w server:app --logto /dev/null
