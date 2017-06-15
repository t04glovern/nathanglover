#!/bin/bash

## Stop Systemctl service
sudo systemctl stop nathanglover

## Git Pull
git pull

## Restart Systemctl service
sudo systemctl start nathanglover
