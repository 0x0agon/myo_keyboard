import libtmux
import os

server = libtmux.Server()

# find current tmux session name
current_session_name = os.popen("tmux display-message -p '#S'").read().strip('\n')
session = server.find_where({'session_name': current_session_name})
# Create a new background tmux window, with 2 panes
w = session.new_window(attach=False, window_name='running_loggers')
bottom_pane = w.split_window(attach=False)
top_pane = w.select_pane('%21')

print('Starting keylogger in the background.')
top_pane.send_keys('echo "./keylogger key_log.txt"')

print('Starting emg logger in the background.')
bottom_pane.send_keys('echo "python3 log_emg_signals.py"')

# listen for Ctrl+c, and shut down loggers when the signal is received
