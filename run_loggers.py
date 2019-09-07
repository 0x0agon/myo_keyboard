import libtmux
import signal
import sys
import os

signal.signal(signal.SIGINT, signal_handler)


def signal_handler(sig, frame):
    print('shutdown loggers here!')
    sys.exit(0)


class Runner(object):
    def __init__(self):
        self.server = libtmux.Server()
        # find current tmux session name
        current_session_name = os.popen("tmux display-message -p '#S'").read().strip('\n')
        self.session = self.server.find_where({'session_name': current_session_name})
        self.window_name = 'running_loggers'

    def exit(self):
        self.session.kill_window(self.window_name)

    def run(self):
        # Create a new background tmux window, with 2 panes
        w = self.session.new_window(attach=False, window_name=self.window_name)
        bottom_pane = w.split_window(attach=False)
        print(w.list_panes())

        def find_top_pane(window):
            panes = window.list_panes()
            print(panes[0])
            return panes[0]

        top_pane = find_top_pane(w)
        # top_pane = w.select_pane('%21')

        keylog_filename = 'key_log.txt'
        emglog_filename = 'emg_log.txt'

        print('Starting keylogger in the background.')
        top_pane.send_keys('echo "./keylogger {}"'.format(keylog_filename))

        print('Starting emg logger in the background.')
        bottom_pane.send_keys('echo "python3 log_emg_signals.py"')

        # listen for Ctrl+c, and shut down loggers when the signal is received


if __name__ == '__main__':
        run()
