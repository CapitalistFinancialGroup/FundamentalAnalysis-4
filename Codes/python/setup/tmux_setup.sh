#!/bin/bash

cd ~
cd /home/subora/Documents/github_repository/FundamentalAnalysis/Codes/python/

tmux new-session -s stockAnalysis 'jupyter notebook' \; \
split-window 'spyder' \; \
split-window \; \
select-layout tiled \;

