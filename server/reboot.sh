#!/bin/bash
sudo stop server

sudo service nginx stop

sudo start server

sudo service nginx restart