import time
import os

current_dir = os.getcwd()

def add_header(output_file, database):
    output_file.seek(0)
    output_file.write("# DDL\nCREATE DATABASE {}\n\n".format(database))
    output_file.write("# DML\n# CONTEXT-DATABASE: {}\n\n".format(database))


class EMGDataFormatter(object):
    def __init__(self, filename, output_dir=None):
        self.filename = filename
        self.output_dir = output_dir if output_dir else current_dir

    def format(self):
        formatted_data = []
        with open(self.filename, 'r') as raw_emg_file:
            for line in raw_emg_file:
                new_line = line.split('(')
                timestamp = str(new_line[0]).strip(' ')
                emg_data = new_line[1].strip(')\n')
                emg_data = [int(v) for v in emg_data.split(',')]

                formatted_data.append('emg_signals'
                                      + ',hand=left'  # TODO: Figure out how to get this info from the myo
                                      + ' '
                                      + 'emg1=' + str(emg_data[0]) + ','
                                      + 'emg2=' + str(emg_data[1]) + ','
                                      + 'emg3=' + str(emg_data[2]) + ','
                                      + 'emg4=' + str(emg_data[3]) + ','
                                      + 'emg5=' + str(emg_data[4]) + ','
                                      + 'emg6=' + str(emg_data[5]) + ','
                                      + 'emg7=' + str(emg_data[6]) + ','
                                      + 'emg8=' + str(emg_data[7])
                                      + ' ' + str(timestamp)
                                      )

        print('formatted data: {}'.format(formatted_data[-1]))
        output_filename = self.output_dir + '/formatted_emg_' + str(time.time()) + '.txt'
        with open(output_filename, 'w+') as output_file:
            add_header(output_file, 'emg_signals')
            for line in formatted_data:
                output_file.write("%s\n" % line)
        return output_filename


class KeyLoggerDataFormatter(object):
    def __init__(self, filename, output_dir=None):
        self.filename = filename
        self.output_dir = output_dir if output_dir else current_dir

    def format(self):
        formatted_data = []
        with open(self.filename, 'r') as raw_key_file:
            for line in raw_key_file:
                # TODO: make this data extraction less fragile
                stripped_line = line.strip('\n').split()
                if len(stripped_line) == 3:
                    # TODO: handle special keys like return, ctrl, etc.
                    key_pressed = stripped_line[2].strip('[').strip(']')
                    if len(key_pressed) == 1:
                        formatted_data.append('key_log'
                                              + ',stroke=' + str(stripped_line[1]) + ','
                                              + 'key=' + str(key_pressed)
                                              + ' '
                                              + 'keyVal=' + str(ord(key_pressed))
                                              + ' ' + str(stripped_line[0])
                                              )

        print('formatted data: {}'.format(formatted_data[-1]))
        output_filename = self.output_dir + '/formatted_keys_' + str(time.time()) + '.txt'
        with open(output_filename, 'w') as output_file:
            add_header(output_file, 'key_log')
            for line in formatted_data:
                output_file.write("%s\n" % line)
        return output_filename


if __name__ == '__main__':
    emg_formatter = EMGDataFormatter(filename=current_dir + '/emg_log.txt')
    emg_formatter.format()

    key_formatter = KeyLoggerDataFormatter(filename=current_dir + '/keylog.txt')
    key_formatter.format()
