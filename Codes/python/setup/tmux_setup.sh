#! /bin/bash

# go inside the requisite folder
cd /home/subora/Documents/github_repository/FundamentalAnalysis/Codes/python/

#create a tmux session
session_name="FundamentalAnalysis"

#a new session is created which currently has only one pane
# important point , do not give commands between these lines
tmux new-session -s $session_name \; \
send-keys 'source /home/subora/anaconda3/etc/profile.d/conda.sh' C-m \; \
send-keys 'conda activate stockAnalysis' C-m \; \
send-keys 'jupyter notebook' C-m \; \
split-window \; \
send-keys 'source /home/subora/anaconda3/etc/profile.d/conda.sh' C-m \; \
send-keys 'conda activate stockAnalysis' C-m \; \
send-keys 'spyder' C-m \; \
select-layout tiled \; \
new-window \; \
send-keys 'source /home/subora/anaconda3/etc/profile.d/conda.sh' C-m \; \
send-keys 'conda activate stockAnalysis' C-m \; \
