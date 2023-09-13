#!/bin/bash
mkfifo /tmp/fifo
/tmp/dlt-project/rootfs/bin/dlt-daemon &
/tmp/dlt-project/rootfs/bin/dlt-receive -a 127.0.0.1 > /tmp/fifo
