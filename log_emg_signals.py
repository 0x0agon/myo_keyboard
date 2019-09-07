#! /usr/local/bin/python3
import os
import sys
import time
current_dir = os.getcwd()
sys.path.append(current_dir + '/../myo-raw/')
import myo_raw as myolib


class MyoRecorder(object):
    def __init__(self):
        self.myo = myolib.MyoRaw(sys.argv[1] if len(sys.argv) >= 2 else None)
        # TODO: use a csv instead of a txt
        self.file = open('emg_log.txt', 'w')
        print('logfile open: {}'.format(self.file))

        def proc_emg(emg, moving):
            new_line = str(time.time_ns()) + ' ' + str(emg) + '\n'
            self.file.write(new_line)

        self.myo.add_emg_handler(proc_emg)

    def connect(self):
        self.myo.connect()

    def run(self, timeout=None):
        self.myo.run(timeout)

    def clean_up(self):
        self.myo.disconnect()
        self.file.close()


if __name__ == "__main__":
    # setup myo object
    myo = MyoRecorder()
    myo.connect()

    try:
        while True:
            myo.run(1)  # 1s timeout on trying to receive a packet
    except KeyboardInterrupt:
        pass
    finally:
        myo.clean_up()

