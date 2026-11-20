#!/bin/bash
cd "$(dirname "$0")"
git pull
sudo systemctl restart lady-devils-hub