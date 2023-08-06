import re
import datetime as dt
from pathlib import Path
import numpy as np
import sys


def make_run_id(base_path, base_name):
    """
    Make sure old data is never overwritten. Adds an incremented number to base name. If a datafile with the same name
    already exists, then the number is incremented.


    :param base_path:
    :param base_name:
    :return:
    """
    base_dir = Path(base_path) / (base_name + '-')
    dirlist = Path(base_path).glob(base_name + '-*')
    meas_numlist = [-1]
    for name in dirlist:
        namestr = str(name)
        if name.is_dir():
            meas_numlist.append(int(namestr[len(str(base_dir)):]))
    meas_num = max(meas_numlist) + 1
    return str(base_dir)+'{:03d}'.format(meas_num), base_name+'-{:03d}'.format(meas_num)


def parse_time(args):
    """
    Parses command line time slice with optional timebase argument. Timebase argument is one of 's', 'm', 'h' or 'd'.
    Timebase argument, if it exists, is the last value in the list or tuple of (start, [stop], [timebase]) that defines
    the slice.

    :param args: A list or tuple of (start, [stop], [timebase]). All input arguments are strings.
    :return: returns parsed time slice (start, stop) in integer nanoseconds.

    """

    if len(args) > 3:
        print('Invalid time range!')
        raise ValueError
    time_slice = [None, None]
    timebase, new_args = parse_timebase(args)
    time_slice[:len(new_args)] = [int(new_args[x]) * timebase for x in range(len(new_args))]
    return time_slice

def parse_timebase(args):
    """
    Parses the timebase string if it exists, supplies default if it does not and returns the timebase multiplier
    with the other arguments.

    :param args: A list or tuple of (start, [stop], [timebase]). All input arguments are strings.
    :return: timebase multiplier for ns-transformation and list of the other arguments.

    """

    if args[-1].isnumeric():  # no timebase character added
        timebase = 60e9
        return timebase, args
    else:
        units = {'ns': 1, 'us': 1000, 'ms': 1e6, 's': 1e9, 'm': 60e9, 'h': 3600e9, 'd': 24 * 3600e9}
        if args[-1] in units.keys():
            timebase = units[args[-1]]
            new_args = args[:-1]
        else:
            print('Invalid time unit. Timebase in {}!'.format(units))
            raise ValueError
    return timebase, new_args


def atoi(text):
    """
    Convert integer text to int, otherwise return the original string. Used to parse long filenames with numbering
    in the filenme.

    :param text: Input string.
    :return: If text is convertible to integer this returns the integer, otherwise the original text.
    """
    #print(text)
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts number strings in human order ('1' before '10') and so on.
    Taken from:
    http://nedbatchelder.com/blog/200712/human_sorting.html

    :param text: input string
    :return:

    """

    nums = re.split(r'(\d+)', text)
    print(nums)
    #print(atoi(nums[-1]))
    #sys.exit()
    print([atoi(x) for x in nums])
    return [atoi(x) for x in nums]
    #return [atoi(c) for c in re.split(r'(\d+)', text)]

def fromisoformat(dt_string):
    """
    Converts string returned by python 3.7+ datetime.toisoformat() into a proper datetime object. This was needed
    because the isoformat seems to be fairly new thing in python and not present in 3.6 or earlier.

    The string to be parsed is of the format: "2020-06-09T04:00:01.434322"

    :param dt_string: isoformat string

    :return: datetime object

    """

    date_p, time_p = dt_string.split('T')
    date_p = date_p.split('-')
    time_p = time_p.split(':')
    secval = float(time_p[2])
    time_p[-1] = int(secval // 1)
    time_p.append(int((secval-time_p[-1]) * 1000000))
    in_list = [int(x) for x in date_p + time_p]
    return dt.datetime(*in_list)


def parse_file(dir_name, file_name, raw_ext=None):
    """
    Finds data files (matching optional file_name prefix) from directory. First event mode data files are searched for, if not
    found, then channel mode files and finally raw data files are searched for. All files in the directory (or matching
    a given base name) are returned

    Problem is that some raw data formats (Caen, native channel data) have multiple files per measurement. This is fixed
    by having a wildcard expression of the postfix of the filename included in the extension
    like ch???.dat for caen data. Unique names are then automatically resolved by saving the base names as keys to a
    dictionary (which is ordered in py3 unlike the set?).

    :param dir_name: The directory containing the data
    :param: file_name: optional base name for data files if they are named differently from directory.
    :param: raw_ext: optional wildcard pattern for raw data files.
    :return: list of base names of data files in the directory (matching file_name prefix)
    """
    #

    # into pathlib object if not already
    directory = Path(dir_name)
    if file_name is not None:  # if filename prefix is given
        prefix = file_name
    else:  # otherwise use the directory name as prefix
        prefix = directory.stem

    suffix = '_events.dat'
    print('Searching for direct match:', directory, prefix + suffix)

    if (directory / (prefix + suffix)).exists():
        # a match
        base_names = [prefix]
    else:
        # list of base names matching the prefix
        base_names = [x.name[:-len(suffix)] for x in directory.glob(prefix + '*' + suffix)]

    print('base names', base_names)

    # if event data is not found the data may be split to several channel- or raw- files. Need to construct list of
    # unique base names.
    if len(base_names) == 0:  # if channel data is present the loading will go on from there
        suffix = '_events_ch?.dat'
        print('Searching for channel data: {}.'.format(prefix + suffix))
        # temp = {x.name[:-len(prefix + suffix)]: None for x in
        temp = {x.name[:-len(suffix)]: None for x in
                directory.glob(prefix + suffix)}
        base_names = list(temp.keys())

    if len(base_names) == 0:  # raw data is checked last
        if raw_ext is not None:
            suffix = raw_ext
            print('Searching for raw data: {}.'.format(prefix + suffix))
            temp = {x.name[:-len(suffix)]: None for x in
                    directory.glob(prefix + suffix)}
            base_names = list(temp.keys())

    if len(base_names) == 0:
        print('No datafiles found from', directory)
        print('Tried to match with base name', prefix)

    return base_names


def check_monotonousness(vector):
    """
    Checks if values in a given vector are monotonously increasing. If they are not, the index of the first element
    that breaks the monotonousness is returned. None.
    :param vector:
    :return: Index of first out-of-place element in vector. None is returned if vector is monotonous.
    """
    retval = None

    # Check for timestamp reset events in good data
    temp = vector[1:] <= vector[:-1]
    if np.any(temp):
        print(np.argmax(temp))
        retval = np.argmax(temp) + 1
        print('vec at', retval, vector[retval], temp[retval])
        print('Time reset event!')

    #for i in range(vector.shape[0]-1):
    #    if (vector[i] > vector[i+1]):
    #        retval = i+1
    #        break
    return retval


def sanitize_for_json(athing):
    int_types = (np.uint8, np.int8, np.uint32, np.int32, np.uint64, np.int64)
    float_types = (np.float32, np.float64)
    if isinstance(athing, list):
        for idx, val in enumerate(athing):
            athing[idx] = sanitize_for_json(val)

    elif isinstance(athing, np.ndarray):
        athing = athing.tolist()

    elif isinstance(athing, dict):
        for key, val in athing.items():
            athing[key] = sanitize_for_json(val)
    else:
        if isinstance(athing, int_types):
            athing = int(athing)
        elif isinstance(athing, float_types):
            athing = float(athing)
        elif isinstance(athing, dt.datetime):
            athing = athing.isoformat()
    return athing


def desanitize_json(athing):
    """
    This is the opposite of sanitize_for_json, so that given keywords are cast back to their proper numpy or datetime
    formats on load. Lists of keywords are maintained here and any new specially typed data should be added to the
    lists to ensure proper operation.

    The function recursively goes through the input dictionary looking for dictionary keywords in the internal type
    tuples. If one is found, the data value of the key is cast into proper format.

    :param athing:  A dictionary that will be sanitized
    :return:        A dictionary with properly cast data
    """

    float_types = ('dead_time', 'live_time', 'quantity')
    date_types = ('start', 'stop', 'collection_start', 'collection_stop')
    int_types = ('input_counts', 'counts', 'events', 'total_time')
    cal_types = ('cal')
    if isinstance(athing, list):
        for idx, val in enumerate(athing):
            athing[idx] = sanitize_for_json(val)
    elif isinstance(athing, dict):
        for key, val in athing.items():
            # check for special keys first
            if key in float_types:
                athing[key] = float(val)
            elif key in int_types:
                print(key,val)
                athing[key] = int(val)
            elif key in date_types:
                athing[key] = fromisoformat(val)
            elif key in cal_types:
                print('got a cal')
                acal = athing[key]
                print(acal)
                for key2, val2 in acal.items():
                    acal[key2] = np.asarray(val2).astype(float)
                athing[key] = acal
                print(athing[key])
            else:
                athing[key] = sanitize_for_json(val)
    else:
        if isinstance(athing, int_types):
            athing = int(athing)
        elif isinstance(athing, float_types):
            athing = float(athing)
        elif isinstance(athing, dt.datetime):
            athing = athing.isoformat()
    return athing


'''
def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from https://stackoverflow.com/a/12643073/190597
    """
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]
'''


