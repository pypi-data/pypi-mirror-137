import json
import time
import datetime as dt

from pathlib import Path
from types import SimpleNamespace

import numpy as np
from limonade import misc
import limonade.exceptions as ex

"""
Utils is a repository for generally useful functions and classes for thing such as reading and writing.

"""

def delete_channel_data(data_path, base_name, cfg):
    """
    Used to delete channel files after parsing.
    :param data_path:
    :param base_name:
    :param cfg:
    :return:
    """
    timenames, enames, tnames, xnames = find_data_files(data_path, base_name, cfg, mode='channel')
    for fname in timenames + enames + tnames:
        if fname.exists():
            fname.unlink()
    for chnamelist in xnames:
        for fname in chnamelist:
            if fname is not None:
                if fname.exists():
                    fname.unlink()

def find_data_files(data_path, base_name, cfg, mode):
    """
    Generate filenames (paths) of all the data produced by config. You can select either 'event' or 'channel'
    type names.

    :param data_path:
    :param base_name:
    :param cfg:
    :param mode:
    :return: timing, energy, time and extras filenames as lists. For event data the first (and only) item in the list
             is the relevant filename. For channel data there is a single name for every channel. Extra names are given
             as a list of names, one per extra (for each channel as in other data).
    """

    extras = cfg.det['extras']

    if mode == 'event':
        timenames = [data_path / (base_name + '_timestamps.dat')]
        enames = [data_path / (base_name + '_events.dat')]
        tnames = [data_path / (base_name + '_timing.dat')]
        xnames = []
        try:
            for extra in extras:
                xnames.append([data_path / (base_name + '_{}.dat'.format(extra['name']))])
        except TypeError:
            pass

    elif mode == 'channel':
        timenames = [data_path / (base_name + '_timestamps_ch{}.dat'.format(x)) for x in cfg.det['ch_list']]
        enames = [data_path / (base_name + '_events_ch{}.dat'.format(x)) for x in cfg.det['ch_list']]
        tnames = [data_path / (base_name + '_timing_ch{}.dat'.format(x)) for x in cfg.det['ch_list']]
        xnames = []
        if extras is not None:
            for extra in extras:
                xnames.append([])  # all extras get a position in list
                if extra['name'] not in ['latency', 'multihit']:
                    # this extra is present in channel data and will be combined either as
                    # a bit in a bitmask or a column in a matrix.
                    try:  # channel mask default is ones
                        ch_mask = np.array(extra['ch_mask'], dtype='bool')
                    except:
                        ch_mask = np.ones((len(cfg.det['ch_cfg']),), dtype='bool')

                    # Extra names are retrieved by channel index. In cases there is no extra defined
                    # for a channel we need to put something in to the list. Let it be None then.
                    for ch_idx in range(len(cfg.det['ch_cfg'])):
                        xnames[-1].append(None)
                        if ch_mask[ch_idx]:
                            efil = data_path / (base_name + '_{}_ch{}.dat'.format(extra['name'], ch_idx))
                            #assert(efil.exists())
                            xnames[-1][-1] = efil

    return timenames, enames, tnames, xnames


def write_channel_metadata(data_path, base_name, channel, metadata):
    """
    Writes the metadata to disk. Some data entries in metadata dictionary are not directly serializable into json,
    so some parsing happens when reading/writing.

    :param data_path:       Path to data
    :param base_name:       Base name
    :param channel:         Channel to write. Writes all data if negative number.
    :param metadata:        List of metadata dictionaries, one per channel. Result of Metadata.dump().
    """
    # make sure no datetime objects or numpy numerical values end up in the json serializer.
    metadata = misc.sanitize_for_json(metadata)

    #datetime_type = ['start', 'stop']
    # make sure data_path is a pathlib Path
    data_path = Path(data_path)

    if channel >= 0:  # if saving single channel only
        channels = (channel, metadata[channel:channel+1])
    else:
        channels = enumerate(metadata)

    for ch_idx, meta_d in channels:
        try:
            temp_for_file = {key: value for key, value in meta_d.items()}  # if key not in datetime_type}
        except:
            print(meta_d.items())
            raise ex.LimonadeException('Error in write metadata')
        
        if 'notes' in meta_d:
            temp_for_file['notes'] = meta_d['notes']
        else:
            temp_for_file['notes'] = 'Metadata defined by raw files.'

        if meta_d['start'] is None:
            temp_for_file['notes'] += 'Missing start time substituted by compile time.'
            meta_d['start'] = dt.datetime.fromtimestamp(time.time())

        if meta_d['stop'] is None:
            temp_for_file['notes'] += 'Missing stop time calculated from timestamps.'
            meta_d['stop'] = meta_d['start'] + \
                                        dt.timedelta(seconds=int(meta_d['total_time']*1e-9))

        #for key in datetime_type:
        #    temp_for_file[key] = meta_d[key].isoformat()

        with (data_path / (base_name + '_metadata_ch{:02d}.json'.format(ch_idx))).open('w') as fil:
            #json.dump(temp_for_file, fil, indent=0, default=int)
            json.dump(temp_for_file, fil, indent=0)


def read_channel_metadata(data_path, base_name, channel):
    try:
        with (data_path / (base_name + '_metadata_ch{:02d}.json'.format(channel))).open('r') as fil:
            temp_from_file = json.load(fil)
    except FileNotFoundError:
        raise ex.LimonadeDataNotFoundError('No metadata found!')
    metadata = misc.desanitize_json(temp_from_file)
    #datetime_type = ['start', 'stop']
    #metadata = {key: value for key, value in temp_from_file.items() if key not in datetime_type}
    #for key in datetime_type:
    #    #metadata[key] = dt.datetime.fromisoformat(temp_from_file[key]) # not present in python 3.6
    #    metadata[key] = misc.fromisoformat(temp_from_file[key])
    return metadata


def find_path(config, name, suffix):
    """
    Used to locate a given config file. The home directory of the data is automatically searched before
    the config path so that local changes stick.
    """
    home = Path(config.path['home'])
    #print('Find path =======', config.path)
    #print(name)
    #print(suffix)
    filename = Path(name + suffix)  #name of the file
    if (home / filename).exists():
        loadpath = home / filename
        print('Found local file', loadpath)
    else:
        loadpath = Path(config.path['cfg_dir']) / suffix.split('.')[0][1:] / filename
    return loadpath


def load_plot_config(config, plot_name):
    """
    Loads a plot configuration from a json file.

    :param config: Config data that has the config.path in it
    :param plot_name_list: plot config name without the _plotcfg.json postfix or a list of names
    :return: a plot config dictionary
    """
    print(plot_name)
    try:
        with find_path(config, plot_name, '_plotcfg.json').open('r') as fil:
            plot_config = json.load(fil)
    except FileNotFoundError:
        raise ex.LimonadeConfigurationError('Could not find plot configuration.')
    plot_config = misc.desanitize_json(plot_config)
    return plot_config


def load_style_sheet(config, style_name_list):
    """
    Loads a matplotlib style sheet written as a json file.

    :param config: Detector configuration object
    :param style_name_list: style path or a list of paths
    :return: list of style dictionaries
    """
    style_cfg_list = []
    if isinstance(style_name_list, str):  # single stylesheet if string is given
        style_name_list = [style_name_list]
    while len(style_name_list) > 0:
        style_name = style_name_list.pop(0)
        try:
            with find_path(config, style_name, '_stylecfg.json').open('r') as fil:
                style_config = json.load(fil)
            style_cfg_list.append(style_config)
        except FileNotFoundError:
            raise ex.LimonadeConfigurationError('Could not find stylesheet.')

    return style_cfg_list


def load_effcal(config, eff=None):
    if eff is None:
        eff = config.det['effcal']

    with find_path(config, eff, '_effcal.json').open('r') as fil:
        temp = json.load(fil)
        effcal = temp
    return effcal


def load_strip_cal(config):
    """
    Load strip calibration files if they exist.
    """

    strips = []
    for ch in config.det['ch_cfg']:
        try:
            if ch['cal_array'] is not None:
                strips.append(ch['cal_array'])
        except KeyError:
            pass

    if strips:
        strip_cal = []
        try:
            for cal in strips:
                with find_path(config, cal, '_stripcal.json').open('r') as fil:
                    strip_cal.append(json.load(fil)['calibration'])
        except FileNotFoundError:
            print('Strip calibration file not found!')
            raise ex.LimonadeConfigurationError('Strip calibration file not found!')
        out = np.stack(strip_cal, axis=0)
        return out
    return None


def old_config(config: dict)->SimpleNamespace:
    """ 
    Makes new style dict-config into old-style namespace config.

    :param config:      A new style dictionary config with, at the minimum, path, det, channel, readout and cal 
                        keywords defined.
    :result:            An old style config namespace with matching members to the input dict 
    """
    print('############################################')
    # check that the config dict is complete
    field_names = ['path', 'det', 'readout', 'ch', 'cal']
    if not all([fn in config.keys() for fn in field_names]):
        for key, item in dict.items():
            print(key, item)
        raise TypeError('Not a complete configuration dictionary!')

    old_cfg = SimpleNamespace()
    for a_field in config.keys():
        setattr(old_cfg, a_field, config[a_field])
    #for ch in range(len(old_cfg.metadata)):
    #    print(type(old_cfg.metadata[ch]['start']))
    #    old_cfg.metadata[ch]['start'] = dt.datetime.fromisoformat(old_cfg.metadata[ch]['start'])
    #    old_cfg.metadata[ch]['stop'] = dt.datetime.fromisoformat(old_cfg.metadata[ch]['stop'])
    return old_cfg
        