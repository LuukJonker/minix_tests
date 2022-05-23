#!/bin/bash

name=$1

dd if=/dev/zero of="$name".img bs=1k count=5120
mkfs.minix -1 -n 14 "$name".img
