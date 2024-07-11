import time
import csv
from PetoiRobot import *
from datetime import datetime
import platform


def read_sensors(sensors: list, read_time: int, label: str = ''):
    """
    Function to read all sensors and return it in a dataframe format (-1 if no data is available for the sensor).
    * sensors[list]: list of connected sensors
    * read_time[int]: time (in seconds) for the acquisition
    * label[str]: label for AI

    Returns data as a pandas dataframe.
    """

    if len(sensors) == 0:
        raise ValueError('Please specify at least one sensor.')

    for sensor in sensors:
        if sensor not in ['pir', 'touch', 'light', 'ir']:
            raise ValueError(
                'Specified an unknown sensor type. Available sensors include: pir, touch, light, ir.')

    if 'touch' in sensors and 'pir' in sensors:
        raise ValueError('Please specify only one type of digital sensor.')

    # Constants definition:
    wait_for = 1

    if read_time < wait_for:
        raise ValueError('Please specify a read_time >= 1')

    # Pre-allocate a list to store the data:
    data = []

    print('----------------------------')
    print('Starting data acquisition...')
    for _ in range(round(read_time/wait_for)):

        # Temporary dictionary to store the data point (including the timestamp):
        tmp = {}
        tmp['timestamp'] = datetime.now()

        # Loop through the sensors:
        if 'pir' in sensors:
            tmp['pir'] = readDigitalValue(6)
        else:
            tmp['pir'] = -1

        if 'touch' in sensors:
            tmp['touch_right'] = readDigitalValue(6)
            tmp['touch_left'] = readDigitalValue(7)
        else:
            tmp['touch_right'] = -1
            tmp['touch_left'] = -1

        if sensor == 'light':
            tmp['light_right'] = readAnalogValue(16)
            tmp['light_left'] = readAnalogValue(17)
        else:
            tmp['light_right'] = -1
            tmp['light_left'] = -1

        if sensor == 'ir':
            tmp['ir_right'] = readAnalogValue(16)
            tmp['ir_left'] = readAnalogValue(17)
        else:
            tmp['ir_right'] = -1
            tmp['ir_left'] = -1

        # Add the label:
        tmp['label'] = label

        print('Acquired a data point from the following sensors: {}'.format(sensors))

        # Save the data point:
        data.append(tmp)

        # Wait a little in between acquisitions:
        time.sleep(wait_for)

    print('Finished data acquisition')
    print('----------------------------')

    return data


def save_sensor_data(data: list, filename: str):
    """
    Function to save the data locally in csv format.
    """

    if len(data) == 0:
        raise ValueError('Please provide some data')

    # Constants definition:
    file_ext = '.csv'

    # Check if we are on windows, mac or linux:
    if platform.system() == "Windows":
        sep = '\\'
        home_dir = os.getenv('HOMEDRIVE')
        home_path = os.getenv('HomePath')
        config_dir = home_dir + home_path
    else:  # for Linux & macOS
        sep = '/'
        home = os.getenv('HOME')
        config_dir = home

    # Create the data directory:
    data_dir = config_dir + sep + 'sensor_data'

    # Check if it exists:
    if not os.path.exists(data_dir):

        # Create the directory if it does not exist
        os.makedirs(data_dir)

    # Check if the file name already exists and if yes make it unique:
    file_dir = data_dir + sep + filename + file_ext

    # Get the column names:
    keys = data[0].keys()

    # Check if the file already exists:
    if os.path.exists(file_dir):

        # Change the file name:
        cnt = 1
        file_dir = data_dir + sep + '{}-{}{}'.format(filename, cnt, file_ext)
        while os.path.exists(file_dir):
            cnt += 1
            file_dir = data_dir + sep + \
                '{}-{}{}'.format(filename, cnt, file_ext)

    print('Saving data...')
    with open(file_dir, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print('File saved successfully at {}'.format(file_dir))

    return None


def main():
    # Define the sensors to read:
    sensors = ['pir', 'light']

    # Define the read time:
    read_time = 10

    # Define the label:
    label = 'test'

    # Read the sensors:
    data = read_sensors(sensors, read_time, label)

    # Save the data:
    save_sensor_data(data, 'test')


if __name__ == '__main__':
    main()
