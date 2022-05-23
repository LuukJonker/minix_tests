#!/bin/bash

name=$1

dd if=/dev/zero of="$name".img bs=1k count=32
mkfs.minix -1 -n 14 "$name".img
