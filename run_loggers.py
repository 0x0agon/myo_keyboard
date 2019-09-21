import libtmux
import os
import signal
import sys
import time
from convert_data_to_influx_line import EMGDataFormatter, KeyLoggerDataFormatter

# signal.signal(signal.SIGINT, signal_handler)
# def signal_handler(sig, frame):
#     print('shutdown loggers here!')
#     sys.exit(0)

current_dir = os.getcwd()

class Runner(object):
    def __init__(self):
        signal.signal(signal.SIGINT, lambda signal, frmae: self._signal_handler())
        self.server = libtmux.Server()
        # find current tmux session name
        current_session_name = os.popen("tmux display-message -p '#S'").read().strip('\n')
        self.session = self.server.find_where({'session_name': current_session_name})
        self.window_name = 'running_loggers'

    def _signal_handler(self):
        print('shutting down loggers.')
        self.exit()
        sys.exit(0)

    def exit(self):
        windows = self.session.list_windows()
        print('session\'s windows: {}'.format(windows))
        print('trying to kill the one named {}'.format(self.window_name))
        for window in windows:
            if window.name == self.window_name:
                self.session.kill_window(window.id)
        print('formatting log files')
        keylog_formatter = KeyLoggerDataFormatter(filename=current_dir + '/key_log.txt', output_dir=current_dir + '/output_files')
        keylog_formatter.format()
        emglog_formatter = EMGDataFormatter(filename=current_dir + '/emg_log.txt', output_dir=current_dir + '/output_files')
        emglog_formatter.format()
        # TODO: stick the data into influx on exit

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

        keylog_filename = current_dir + '/key_log.txt'
        emglog_filename = current_dir + '/emg_log.txt'

        print('Starting keylogger in the background.')
        # top_pane.send_keys('echo "./keylogger {}"'.format(keylog_filename))
        top_pane.send_keys('./keylogger {}'.format(keylog_filename))

        print('Starting emg logger in the background.')
        bottom_pane.send_keys('python3 log_emg_signals.py')

        # listen for Ctrl+c, and shut down loggers when the signal is received
        print('Running, press Ctrl+C to kill loggers and exit')
        while True:
            time.sleep(0.2)


if __name__ == '__main__':
    runner = Runner()
    runner.run()
