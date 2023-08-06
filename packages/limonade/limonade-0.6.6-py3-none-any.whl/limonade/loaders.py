import time
import datetime as dt

from struct import unpack, calcsize
import numpy as np
import limonade.data
from limonade import utils as ut, misc as misc


def native_loader(self, data_path, base_name):
    pass


def g4_loader(self, data_path, base_name):
    """
    Current version of Geant4 data needs a simple loader to fix total time in metadata.
    :param self:
    :param data_path:
    :param base_name:
    :return:
    """
    #make metadata instance
    metadata = limonade.data.Metadata(None, len(self.ch_list))
    # Now the data is on disk. Next it will be loaded and parsed
    data_dict, timing_data = self._load_channel_data(data_path, base_name)

    # Fill metadata
    metadata.run_id = base_name
    metadata.name = self.config.det['name']
    # timing from file timestamp and last timestamp
    metadata.start = metadata.stop - dt.timedelta(seconds=data_dict['time'][-1]*1e-9)
    metadata.events = data_dict['time'].shape[0]
    metadata.counts = np.count_nonzero(data_dict['energy'] > 0, axis=0)
    metadata.input_counts = np.count_nonzero(data_dict['energy'] >= 0, axis=0)
    #metadata.total_time = data_dict['time'][-1]
    for ch in range(len(self.ch_list)):
        metadata.total_time = np.uint64(data_dict[ch]['time'][-1]*self.config.det['sample_ns'])
    metadata.dead_time = [timing_data['dt{}'.format(x)].sum() for x in range(len(self.ch_list))]

    # and save it
    ut.write_channel_metadata(data_path, base_name, -1, metadata.dump())
    return data_dict, timing_data


def dspec_loader(self, data_path, base_name):
    pass


def caen_loader(self, data_path, base_name):
    """
    Reads data saved by Caen MCA. Caen data format does not record time and date of data taking, so these are calculated
    from the datafile modification timestamp.

    In case there are several runs on single data (appended to same file) the results may be unpredictable. In the
    future all appends should be recognized and extracted as channel files, but only first one is loaded as data.

    The loaded channel list is compared to one in cfg and if not matching an error is generated.

    Caen loader supports two kinds of bitmask extra data: Pileup and flags. Flags is set whenever there the 'extras'
    data is nonzero. Pileup flag is set whenever the energy for the channel is zero, signaling a pileup event (unless
    set to return energy value).

    :param self: Calling Data instance. This is set when the loader is set as class method.
    :param data_path: path to a file

    :return:

    """

    _DATA_DICT = {0: ('Trigger Time Tag', 't'),
                  1: ('Energy', 'E'),
                  2: ('Extras', 'x'),
                  3: ('Short Energy', 'sE'),
                  4: ('DPP Code', 'DPP'),
                  255: ('Fake', 'f')}
    _TYPE_DICT = {0: '<b',
                  1: '<B',
                  2: '<H',
                  3: '<H',
                  4: '<i',

                  5: '<I',
                  6: '<q',
                  7: '<Q',
                  8: 'string',  # placeholder for the generic string
                  9: '<l',
                  10: '<d',
                  11: '<c',
                  128: '<H',  # placeholder for the 3 byte string
                  255: 'Fake'}

    def _check_time_corruption(vector, last_good_v):
        """
        Check for corrupt timestamps within a readout chunk. return begin, stop and next good indices out of vector.
        :param vector:
        :return:
        """
        stop_idx = vector.shape[0]
        begin_idx = 0
        next_good = -1
        temp = np.zeros_like(vector, dtype='bool')
        #temp[1:] = vector[1:] > last_good_v + 36000000000000  # 10h gap
        temp[1:] = vector[1:] > vector[:-1] + 36000000000000  # 10h gap
        if vector[0] > last_good_v + 72000000000000:
            # first index is corrupt has to be handled as this will be true for the second subrange automatically.
            # Search for a good value to begin the iteration.
            temp[0] = True
            print(vector[0], last_good_v)
            good = np.argmin(temp)
            if vector[1] > last_good_v + 72000000000000 and good == 0:
                # all indices are corrupt
                print('All indices are corrupt')
                raise
            begin_idx = good

        # Check for garbage timestamps
        if np.any(temp[begin_idx:]):
            print('Garbage timestamp event')
            good = np.argmax(temp[begin_idx:])  # points to first bad index or zero if all are good
            if good != 0:
                stop_idx = begin_idx + good  # one past the last good idx
                ng = np.argmin(temp[stop_idx:])  # points to next good index or zero if all bad
                if ng != 0:
                    next_good = stop_idx + ng

        retval = (begin_idx, stop_idx, next_good)
        return retval

    def _read_header(fileid):

        PROTOCOL, NWORDS, EMPTY = unpack('<' + 'B' * 2 + 'H',
                                            fileid.read(4))
        type_list = []
        type_names = []
        for line in range(NWORDS - 1):
            DATA, TYPE, EMPTY = unpack('<' + 'B' + 'H' + 'B', fileid.read(4))
            if _DATA_DICT[DATA] != _DATA_DICT[4]:
                type_list.append(_TYPE_DICT[TYPE])
                type_names.append(_DATA_DICT[DATA])

        return PROTOCOL, type_list, type_names

    def make_streams(ch_list, data_path, base_name, pileup, flags, partnum):
        """
        Spawn a new set of streams with file name modified by the partnum.
        also return matching datavectors

        :param ch_list:
        :param data_path:
        :param base_name:
        :param pileup:
        :param flags:
        :param partnum:
        :return:
        """
        if partnum > 0:
            base_name = base_name + '_part-{}'.format(partnum)
        streams = []
        streams.append(limonade.data.StreamData(data_path, base_name, raw=True, method='event', channels=ch_list))
        if pileup:
            streams.append(limonade.data.StreamData(data_path, base_name, raw=True, method='extra',
                                                    extra_name='pileup', channels=ch_list))
        else:
            streams.append(None)

        if flags:
            streams.append(limonade.data.StreamData(data_path, base_name, raw=True, method='extra',
                                                    extra_name='flags', channels=ch_list))
        else:
            streams.append(None)

        streams.append(
            limonade.data.StreamData(data_path, base_name, raw=True, method='timing', channels=ch_list))

        return streams

    # First find the number of channels
    names = list(data_path.glob(base_name + '_ch???.dat'))
    # It seems that either Path.glob or Windows behavior has changed: The list is no more sorted by filename
    names.sort()
    print('Caen loader list', names, 'While searching', base_name + '_ch???.dat')
    temp_list = []  # list of channel indices found from data_path

    channel_list = self.ch_list  # list of channel indices expected from config
    for name in names:  # find saved channel data
        print(name)
        chnum = int(name.stem.split('_ch')[1])
        temp_list.append(chnum)

    for ch in channel_list:  # check if needed channels are found from the data
        print(channel_list, temp_list)
        temp_list.pop(temp_list.index(ch))

    chunk_num = 100000
    timing_num = 1000

    extras = self.config.det['extras']

    pileup = False
    flags = False
    for extra in extras:
        if extra['name'] == 'pileup':
            pileup = True
        elif extra['name'] == 'flags':
            flags = True

    # make streamers
    streamer, pileup_streamer, flag_streamer, time_streamer = make_streams(self.ch_list, data_path, base_name,
                                                                           pileup, flags, 0)
    stream_list = [(streamer, pileup_streamer, flag_streamer, time_streamer)]
    # make metadata instance
    metadata = limonade.data.Metadata(None, len(self.ch_list))


    # file modification date is the best estimate of run stop. Start is automatically calculated by metadata.
    metadata.stop = dt.datetime.fromtimestamp(names[channel_list[0]].stat().st_mtime)

    # The datafiles are streamed one by one.
    # Caen files have no timing information: timing file will be created after parsing.
    # Caen data can be corrupted by appending multiple runs into same file by accident. This is very bad
    # for timing, because the timestamps are not monotonously increasing anymore. These datafiles should be broken
    # into several one-run files when opened. What is done here is that new files with modified names are spawned
    # when a timestamp is smaller than previous. Only the first run belongs to this data, the others are named with
    # _part-N postfix.

    # Loader can read caen channels in arbitrary order and even skip channels, defined by 'ch_list' in config. limonade
    # channels are consecutive and start from 0.

    for channel, ch_idx in enumerate(self.ch_list):
        # empty lists because Stream data takes the data for all channels. Only current channel is updated, all the
        # other are stored as an empty list when iterating this channel
        E_vecs = [[] for _x in range(self.num_ch)]
        time_vecs = [[] for _x in range(self.num_ch)]
        p_vecs = [[] for _x in range(self.num_ch)]
        f_vecs = [[] for _x in range(self.num_ch)]
        timeout = [[] for _x in range(len(self.ch_list))]

        E_vecs[ch_idx] = np.zeros((chunk_num,), dtype='int16')  # negative is empty so that Caen 0 really corresponds
                                                                  # to an event with energy 0 (pileup event)
        E_vecs[ch_idx].fill(-1)
        time_vecs[ch_idx] = np.zeros((chunk_num,), dtype='uint64')
        p_vecs[ch_idx] = np.zeros((chunk_num,), dtype='uint8')
        f_vecs[ch_idx] = np.zeros((chunk_num,), dtype='uint8')
        timing_vec = np.zeros((timing_num,), dtype=[('idx', '<u8'), ('t', '<u8'), ('dt', '<f4')])

        pdeadtime = self.config.det['ch_cfg'][ch_idx]['pdeadtime']
        sample_ns = self.config.det['sample_ns']

        ch_file = names[channel_list.index(ch_idx)]

        #prev_t = 0  # to check for decreasing timestamp event

        current_split = 0  # counts the decreasing timestamp events -> numbering for split files.
        streamer, pileup_streamer, flag_streamer, time_streamer = stream_list[current_split]  # make sure we write to right stream

        with open(ch_file, 'rb') as df:
            PROTOCOL, type_list, type_names = _read_header(df)

            types = [(type_names[x][1], type_list[x]) for x in range(len(type_list))]
            type_string = '<' + ''.join([x[1] for x in type_list])
            evnt_sz = calcsize(type_string[1:])
            chunk_size = chunk_num * evnt_sz  # prepare to read chunk_num events

            isdata = True  # df.read(evnt_sz)
            chunk_idx = 0
            tf_idx = 1  # timing file starts with row of zeroes, so the first idx is 1
            eventcounter = 0
            last_good_val = 0  # last accepted time value. If this is suddenly overshot by a large margin
                               # the big timestamps are excluded as corrupt

            while isdata:

                buffer = df.read(chunk_size)
                buf_len = len(buffer) // evnt_sz  # number of rows in chunk.
                # isdata = buf_len == chunk_num  # Last data if less than chunk size.
                isdata = len(buffer) == chunk_size  # Last data if less than chunk size.
                chunk = np.frombuffer(buffer, dtype=types, count=-1, offset=0)

                # the data chunk can be split into sub ranges if there is a timestamp reset or corrupt time data.
                # Indices relating to these are set here
                cur_begin_idx = 0  # where we start, usually 0
                cur_end_idx = chunk_num  # one past last idx of range, usually end of chunk
                next_begin_idx = -1  # where to start next range, negative if no next range

                # split_idx = 0  # the first index in the chunk that belongs to current data stream. Usually 0.
                # end_idx = buf_len  # the first index in the chunk that belongs to next data stream or buf_len.

                # we use indices for splitting, but the data is read out to arrays before the loop
                time_ch = (chunk['t'][cur_begin_idx:cur_end_idx] * sample_ns)
                E_ch = (chunk['E'][cur_begin_idx:cur_end_idx] & 0x7FFF)
                if pileup:
                    # All bad events are included, also those that have an associated energy value which is for
                    # some reason still marked with the pileup bit (like a start of a saturation event, which
                    # is flagged as a pileup event if a trigger is detected during the veto period). The first
                    # part is not needed, because PU bit is on if pileup has been seen (e=0). If e = 1 and pu-bit
                    # is set there is a saturation event, otherwise it is a generic bad event for unknown reason.
                    p_ch = np.logical_or(chunk['E'][cur_begin_idx:cur_end_idx] == 0,
                                         (chunk['E'][cur_begin_idx:cur_end_idx] & 0x8000) != 0)

                if flags:
                    # flags signify specific events found from EXTRAS. Existence of an extra does not signify much, as
                    # such. It is a bitmask with a load of different data.
                    # Bit 0: LOST EVENT - Events have been lost due to buffer full or preceding saturation. These
                    #        should still be recorded.
                    # bit 1: ROLL-OVER - The DPP-PHA algorithm creates a fake event with Time Stamp = 0, Energy = 0,
                    #        PU = 1, bit[3] and bit[1] of EXTRAS = 1
                    # bit 2: RESERVED
                    # bit 3: FAKE_EVENT
                    # bit 4: INPUT_SATURATION - An event saturated the input dynamics. The event that saturates
                    #        the dynamics has Energy = 0x7FFFF, while the PU flag is set to 1 only if there is also
                    #        a pile-up event in the trigger veto period of 2*rise time.
                    # bit 5: LOST_TRG - Set to 1 whenever 1024 lost events have been detected
                    # bit 6: TOT_TRG - set to 1 whenever 1024 total events have been detected
                    # bit 7: MATCH_COINC

                    f_ch = chunk['x'][cur_begin_idx:cur_end_idx] != 0

                # Check for corruption and splits
                while True:
                    # Check against timestamp corruption events. If one is found, then the data is streamed
                    # up to last good and next iteration starts from next good.
                    corrupt_tuple = _check_time_corruption(time_ch[cur_begin_idx:cur_end_idx],
                                                           last_good_val)
                    if corrupt_tuple is not None:
                        cur_begin_idx = cur_begin_idx + corrupt_tuple[0]
                        cur_end_idx = cur_begin_idx + corrupt_tuple[1]
                        next_begin_idx = cur_begin_idx + corrupt_tuple[2]
                        #print('prev good', last_good_val)
                        last_good_val = time_ch[cur_end_idx - 1]  # end idx points to one past last good
                        #print('last good', last_good_val)
                        #print('tuple', corrupt_tuple)
                        #print('prevs', time_ch[cur_begin_idx], time_ch[cur_end_idx - 1])

                    # We need to check the monotonousness of time vector for every chunk. If not, then
                    # good data is written, new streamers are spawned and rest of the data is iterated
                    # again. The while loop only quits after all data has been streamed.
                    # The possibly multiple splits complicate indexing so we use split_idx to mark the
                    # start position of the current split and end_idx to mark the end of current
                    # split. Normally these would be 0 and buf_len respectively.
                    split_idx = misc.check_monotonousness(time_ch[cur_begin_idx:cur_end_idx])
                    if split_idx is not None:
                        cur_end_idx = cur_begin_idx + split_idx
                        next_begin_idx = cur_end_idx

                    # write to disk
                    time_vecs[ch_idx] = time_ch[cur_begin_idx:cur_end_idx]
                    E_vecs[ch_idx] = E_ch[cur_begin_idx:cur_end_idx]
                    streamer.write((time_vecs, E_vecs))  # stream to .dat file to speed up

                    if pileup:
                        p_vecs[ch_idx] = p_ch[cur_begin_idx:cur_end_idx]
                        pileup_streamer.write(p_vecs)
                    if flags:
                        f_vecs[ch_idx] = f_ch[cur_begin_idx:cur_end_idx]
                        flag_streamer.write(f_vecs)

                    # Dead time is just guessed using pdeadtime (rise-time + flat-top + trigger holdoff).
                    counts_in_range = (cur_end_idx - cur_begin_idx)
                    eventcounter += counts_in_range
                    timing_vec[tf_idx] = (eventcounter - 1, time_vecs[ch_idx][cur_end_idx - 1],
                                          counts_in_range * pdeadtime * 1e-9)
                    tf_idx += 1


                    if split_idx is not None:
                        # New vecs and streamers are initialized if there was a split. Eventcounter is reset too
                        current_split += 1
                        print("Timestamps not monotonous!!!", len(stream_list), current_split, split_idx)

                        timeout[ch_idx] = timing_vec[:tf_idx]
                        time_streamer.write(timeout)  # stream old timing data

                        if len(stream_list) <= current_split:
                            print('Spawning new files.')
                            streamer, pileup_streamer, flag_streamer, time_streamer = make_streams(self.ch_list,
                                                                                                   data_path,
                                                                                                   base_name,
                                                                                                   pileup, flags,
                                                                                                   current_split)
                            stream_list.append((streamer, pileup_streamer, flag_streamer, time_streamer))
                        else:
                            print('Writing to existing files')
                            streamer, pileup_streamer, flag_streamer, time_streamer = stream_list[current_split]
                        eventcounter = 0
                        tf_idx = 1  # continue filling timing data from 1 (idx 0 is zeros)

                    if cur_end_idx < buf_len:  # still iterating
                        if next_begin_idx < 0:
                            # here we are in a middle of a chunk, but there is no good events left. Go to next
                            print('End of chunk corruption event!')
                            break
                        else:
                            cur_begin_idx = next_begin_idx
                            cur_end_idx = buf_len
                    else:  # Through the chunk
                        if next_begin_idx > 0:
                            # there is a next range after end of chunk!
                            print('Unhandled end of Chunk!')
                        break
                    #else:
                    #    #eventcounter += counts_in_range
                    #    break

                # eventcounter += buf_len
                chunk_idx += 1

                if tf_idx == timing_num:  # double the timing vector if it runs out
                    timing_vec = np.concatenate((timing_vec, np.zeros((timing_num,),
                                                                      dtype=[('idx', '<u8'),
                                                                             ('t', '<u8'),
                                                                             ('dt', '<f4')])), axis=0)
                    timing_num = timing_vec.shape[0]

                if isdata == False:
                    print('Operation is normal!')
            timeout[ch_idx] = timing_vec[:tf_idx]
            time_streamer.write(timeout)
        print('ch done')

    for split in stream_list:
        print('In split close')
        for astream in split:
            # Empty extras are None
            if astream is not None:
                astream.close()

    #

    # Now the data is on disk. Next it will be loaded and parsed
    data_dict, timing_data = self._load_channel_data(data_path, base_name)
    # Fill metadata 
    metadata.run_id = base_name
    metadata.name = self.config.det['name']
    # timing from file timestamp and last timestamp
    metadata.start = metadata.stop - dt.timedelta(seconds=data_dict['time'][-1]*1e-9)
    metadata.events = data_dict['time'].shape[0]
    metadata.counts = np.count_nonzero(data_dict['energy'] > 0, axis=0)
    metadata.input_counts = np.count_nonzero(data_dict['energy'] >= 0, axis=0)
    metadata.total_time = data_dict['time'][-1]
    metadata.dead_time = [timing_data['dt{}'.format(x)].sum() for x in range(len(self.ch_list))]

    # and save it
    ut.write_channel_metadata(data_path, base_name, -1, metadata.dump())
    return data_dict, timing_data


def panda_loader(self, data_path, base_name):

    """
    Reads PANDA data. Even though PANDA data is already reconstructed in event mode, it will still be broken down
    to channel files for the pipeline. PANDA clock is used for dead time and timing. DSSSD will be handled as two
    detectors with associated coordinate extra. Due to this and the capability of the multi-hit processor to combine
    data from several channels the DSSSD data will be strip calibrated when read from the raw file. If strip calibration
    needs to be redone later one has to make a dummy calibration to access the uncalibrated strip values.

    If PANDA data is divided into several files, only one is converted and loaded. In this case either start_time,
    stop_time or both are undefined and will be calculated from data length and, in worst case, file modification
    time.

    :param self: Calling Data instance. This is set when the loader is set as class method.
    :param data_path: path to a file

    :return:

    """

    BUFFER_TYPES = {1: 'DATABF',
                    2: 'SCALERBF',
                    3: 'SNAPSBF',
                    4: 'STATEVARBF',
                    5: 'RUNVARBF',
                    6: 'PKTDOCBF',
                    11: 'BEGRUNBF',
                    12: 'ENDRUNBF',
                    13: 'PAUSEBF',
                    14: 'RESUMEBF',
                    30: 'PARAMDESCRIP'}

    # init vars
    dead_time = 0.
    total_time = 0.
    evsum = 0

    #
    ch_list = np.array(self.config.det['ch_list'])
    # strip calibration
    strip_cal = ut.load_strip_cal(self.config)


    ch_file = data_path / (base_name + self.data_ext)

    # init
    f_head_sz = 4  # frame header size of adc buffer

    chunk_over = 2000  # single buffer should have no more events. Max I've seen is ~1500.
    chunk_size = 250000  # Going for fewer array concatenations.
    # array_size = 250000  # current size of array
    big_time = 0  # incremented when timestamp overflowsf
    start_time = None
    stop_time = None
    prevtstamp = 0
    min_tstamp = 0

    # path, data_name, method = 'event', raw = False, channels = None, extra_name = None
    streamer = limonade.data.StreamData(data_path, base_name, raw=True, method='event', channels=self.ch_list)
    time_streamer = limonade.data.StreamData(data_path, base_name, raw=True, method='timing', channels=self.ch_list)
    timing_datas = [np.zeros((2000,), dtype=[('idx', 'u8'), ('t', 'u8'), ('dt', 'f4')]) for _x in range(self.num_ch)]
    # defining the out arrays

    time_vecs = [np.zeros((chunk_size + chunk_over,), dtype='uint64') for _x in range(self.num_ch)]  # for timestamp.
    e_mats = [np.zeros((chunk_size + chunk_over,), dtype='uint16') for _x in range(self.num_ch)]  # Energy data
    [e_mats[_x].fill(-1) for _x in range(self.num_ch)]
    # PANDA has coord extra. Coord should be signed integer so that we can put empty as -1.
    extras = self.config.det['extras']
    for idx in range(len(extras)):
        ex = limonade.data.data_info(extras[idx], ch_list)
        if ex['name'] == 'coord':
            c_dtype = ex['type']
            c_chmask = np.array(ex['ch_mask'], dtype='bool')

    coord_streamer = limonade.data.StreamData(data_path, base_name, raw=True, method='extra',
                                              extra_name='coord', channels=ch_list[c_chmask])
    coord_datas = [np.zeros((chunk_size + chunk_over,), dtype=c_dtype) for _x in range(self.num_ch)]
    [coord_datas[_x].fill(-1) for _x in (0, 1)]

    total_counter = np.zeros((self.num_ch,), dtype='uint64')  # events already written
    empty_counter = np.zeros((self.num_ch,), dtype='uint64')  # zero energy events (using these?)
    events = 0  # total number of recorded accepted events
    chunk_counter = np.zeros((self.num_ch,), dtype='uint64')  # ch indices of event in current chunk
    ev_counter = np.zeros((self.num_ch,), dtype='uint64')  # ch indices of event in current event
    timing_idx = 1  # scalers are the same for every channel, so single idx instead of counter
    first = False
    first_time_of_file = 0  # This is needed to reset the timestamps on a continuation file
    with open(ch_file, 'rb') as df:

        while True:
            #reading next buffer
            buf_counter = 0
            buf_idx = 0  # Byte offset of current buffer
            buffer = df.read(26656)

            if len(buffer) != 26656:
                print('Buffer size only {} / 26656'.format(len(buffer)))

                if np.any(chunk_counter > 0):
                    # save whatever is in the buffer
                    streamer.write(([(time_vecs[x][:chunk_counter[x]] - first_time_of_file) *
                                     self.config.det['sample_ns'] for x in self.ch_list],
                                    [e_mats[x][:chunk_counter[x]] for x in self.ch_list]))
                    coord_streamer.write([coord_datas[x][:chunk_counter[x]] for x in (0, 1)])
                    total_counter += chunk_counter  # total counter used to calculate metadata
                    print(total_counter, 'events')
                    # here the timing index is zero, if a save has just happened
                    if timing_idx > 0:
                        if timing_datas[0]['idx'][timing_idx - 1] < int(total_counter[0] - 1):  # check if need timing data
                            for ch in self.ch_list:
                                print('Data stop without scaler buffer!')
                                timing_datas[ch][timing_idx] = (int(total_counter[ch] - 1),
                                                                chunk_counter[ch] *
                                                                self.config.det['ch_cfg'][ch]['pdeadtime'] * 1e-9)
                            timing_idx += 1
                    time_streamer.write([timing_datas[x][:timing_idx] for x in self.ch_list])

                break

            #data_sz, data_type, num_evt = self._read_header(buffer[:28])
            datatuple = unpack('<' + 'h' * 4 + 'i' + 'h' * 6 + 'i', buffer[:28])
            buf_idx += 28
            data_sz = datatuple[0] * 2  # data size in bytes
            data_type = datatuple[1]
            num_evt = datatuple[5]

            if BUFFER_TYPES[data_type] == 'DATABF':
                buf_idx += f_head_sz  # offset the frame header
                eventno = 0
                evsum += num_evt  # full event size is added to evsum, but rejected events are subtracted later
                while eventno < num_evt:
                    eventno += 1
                    last_ev_idx = buf_idx
                    # First content is the amount of 2-byte words for event
                    num_words = unpack('<h', buffer[buf_idx:buf_idx + 2])[0]
                    buf_idx += 2
                    #matr_idx = chunk_counter + buf_counter
                    if num_words == 6:  # empty event, not counted
                        evsum -= 1  # remove empty events from total sum
                        buf_idx += (num_words) * 2  # go to end of event
                        continue

                    # read the rest of the event
                    # event = st.unpack('<' + 'H' * num_words, buffer[buf_idx:buf_idx + num_words * 2])
                    ev_idx = 0  # index in the current event data words
                    tstamp = 0

                    ev_counter.fill(0)
                    while buf_idx < last_ev_idx + (num_words)*2:   # looping through adcs in the event
                        # the adc data is organized as:
                        # word 0: number of hits
                        # word 1: ADC number. 0 for x, 1 for y and 2 for hpge + beta
                        # word 2: Energy
                        # word 3: Channel number
                        # [word 4: next hit energy]
                        # [word 5: next hit channel]
                        # next to last 2 words: adc timestamp 1 and 2
                        # last 2 word: end of adc data (0xFFFF, 0xFFFF)

                        #read number of hits and adc id
                        nhits, adc = unpack('<' + 'H'*2, buffer[buf_idx:buf_idx + 4])
                        buf_idx += 4
                        if nhits == 0xFFFF:
                            # WTF? Empty ADC frame? Result of diital threshold, I presume. Skip!
                            # print('empty adc frame')
                            continue
                        nhits -= 0x2001  # fourteenth bit is always 1, 1 means 0
                        adc = adc & 0x3  # first two bits code detector

                        # energy/channel pairs, timestamp and footer
                        event = unpack('<' + 'H'*nhits*2 + 'I'*2, buffer[buf_idx:buf_idx + nhits*4 + 8])
                        buf_idx += nhits*4 + 8

                        # take first tstamp in the event. This structure completely screws up the timestamp
                        # reset detection so it is checked first...
                        if tstamp == 0:
                            t_val = (event[-2] & 0x3FFFFFFF)  # bits 30 and 31 always on
                            if t_val < (prevtstamp - 1000):  # clock overflow when timestamp goes backwards.
                                print('Clock overflow event!', t_val, prevtstamp-1000, min_tstamp)
                                big_time += 2 ** 30  # 30 bit clock overflow
                                prevtstamp = 0
                                min_tstamp = 0

                            # t_val can be smaller than previous tstamp. This is due to
                            # differences between adc clocks. Using min_tstamp to ensure monotonous time in this case.
                            #
                            tstamp = max(min_tstamp, t_val)

                        if adc < 2:  # hit to the dsssd
                            # loop through hits.
                            for hit_idx in range(nhits):
                                E = event[2 * hit_idx]
                                ch = (event[2 * hit_idx + 1] & 0x3ff)  # - 0x400
                                try:
                                    if E > 0:
                                        matr_idx = chunk_counter + ev_counter
                                        e_mats[adc][matr_idx[adc]] = (strip_cal[adc, ch, 0] +
                                                                      strip_cal[adc, ch, 1] * E +
                                                                      strip_cal[adc, ch, 2] * E**2)
                                        time_vecs[adc][matr_idx[adc]] = tstamp + big_time
                                        coord_datas[adc][matr_idx[adc]] = ch
                                        ev_counter[adc] += 1
                                    else:
                                        print('empty')
                                        empty_counter[adc] += 1
                                except:
                                    print('Error in strip calibration!')
                                    print('matr_idx', matr_idx[adc])
                                    print('ch', ch, 'chunk', chunk_counter, 'ev', ev_counter)
                                    print('shapes', e_mats[adc].shape, time_vecs[adc].shape, coord_datas[adc].shape)
                                    raise
                        else:
                            # hpge and beta otherwise straightforward, but the ADC channels for beta and hpge
                            # are 16 channels apart. The detector is incremented for beta detector.
                            # Timing can get hairy on events with no tstamp in adc1 or 2, as adc 3 has smaller ticks
                            # which can sometimes overlap nastily with the next hit in adc 1 or 2.
                            for hit_idx in range(nhits):  # loop through hits
                                ch = event[2 * hit_idx + 1] & 0xff
                                E = event[2 * hit_idx]
                                if E > 0:
                                    matr_idx = chunk_counter + ev_counter
                                    if ch == 0:
                                        detector = 2
                                    if ch == 16:
                                        detector = 3
                                    #e_mat[matr_idx, detector] = E
                                    e_mats[detector][matr_idx[detector]] = E
                                    # make sure there is no time overlap with adc 1 or 2
                                    time_vecs[detector][matr_idx[detector]] = tstamp + big_time
                                    ev_counter[detector] += 1
                                else:
                                    print('empty')
                                    empty_counter[detector] += 1

                        buf_counter += 1  # buffer counter incremented once per event

                    if tstamp == 0:
                        print()
                        print('zero time event!')
                        raise

                    min_tstamp = tstamp + 1
                    prevtstamp = t_val
                    # tstamp=0

                    chunk_counter += ev_counter  # chunk counter incremented for every count in event

                    # NOTE! indenting this to the buffer loop to try to fix overflow problems!!!
                    #buf_counter = 0
                    if np.any(chunk_counter >= chunk_size):  # Write data when chunk overflows
                        # save whatever is in the buffer
                        print('save buffer', chunk_counter, 'timing idx', timing_idx)
                        if not first:
                            first_time_of_file = min([time_vecs[x][0] for x in self.ch_list])
                            first = True
                        streamer.write(([(time_vecs[x][:chunk_counter[x]] - first_time_of_file) *
                                          self.config.det['sample_ns'] for x in self.ch_list],
                                        [e_mats[x][:chunk_counter[x]] for x in self.ch_list]))
                        coord_streamer.write([coord_datas[x][:chunk_counter[x]] for x in (0, 1)])

                        time_streamer.write([timing_datas[x][:timing_idx] for x in self.ch_list])
                        [x.fill(0) for x in time_vecs]
                        [x.fill(-1) for x in e_mats]
                        [x.fill(-1) for x in coord_datas]
                        [x.fill(0) for x in timing_datas]

                        total_counter += chunk_counter
                        chunk_counter.fill(0)
                        timing_idx = 0
                        events += buf_counter

            elif BUFFER_TYPES[data_type] == 'SCALERBF':
                # Scaler buffer gives the total and dead by the DAQ
                buf_idx += f_head_sz  # offset the frame header
                sc_header = unpack('<IIhIIh', buffer[buf_idx:buf_idx + 20])
                buf_idx += 20

                # dead time and total time counts in scalers. The scalers don't signal clock overflow, but seem to
                # track dead time at least
                sc_data = unpack('<'+'I'*num_evt, buffer[buf_idx:buf_idx + num_evt*4])

                dtime = sc_data[0]*1.0e-6  # scaler data in s (has internal divisor, timeCalibration, of 1000)
                dead_time += dtime

                # new timing data has (idx, t, dead time in seconds as a float)
                for ch in self.ch_list:
                    timing_datas[ch][timing_idx] = (int(total_counter[ch] + chunk_counter[ch] - 1),
                                                    tstamp + big_time, dtime)
                #print('t:',timing_datas[0][timing_idx], timing_datas[1][timing_idx])
                total_time += sc_data[1]*1.0e-6
                timing_idx += 1


            elif BUFFER_TYPES[data_type] == 'BEGRUNBF':
                print('BEGRUNBUF found - start datetime read!')
                # Control buffers [BEG- and ENDRUNBF have 80 character title for the run and the date and time
                buf_idx += f_head_sz  # offset the frame header

                title = bytes(buffer[buf_idx:buf_idx + 80]).decode()  # the text is handled by bytes
                cdata = unpack('<I7h', buffer[buf_idx + 80:buf_idx + 98])

                # There is a possibility that month begins from 0. Dates seem to be consistently off
                start_time = dt.datetime(cdata[3]+1900, cdata[1] + 1, cdata[2],
                                              cdata[4], cdata[5], cdata[6], int(cdata[7]*1e5))
                first = True  # used to decide whether to cut timestamps by the first time entry

            elif BUFFER_TYPES[data_type] == 'ENDRUNBF':
                print('ENDRUNBUF found - stop datetime read!')
                buf_idx += f_head_sz  # offset the frame header

                title = bytes(buffer[buf_idx:buf_idx + 80]).decode()  # the text is handled by bytes
                cdata = unpack('<I7h', buffer[buf_idx + 80:buf_idx + 98])
                stop_time = dt.datetime(cdata[3]+1900, cdata[1] + 1, cdata[2],
                                              cdata[4], cdata[5], cdata[6], int(cdata[7]*1e5))
            else:
                print('Unhandled buffer type found!')
                print(BUFFER_TYPES[data_type])

    streamer.close()
    coord_streamer.close()
    time_streamer.close()
    print()
    print('Events read:', total_counter)
    print('Discarded', empty_counter, 'empty events.')
    print()
    print('Starting parsing the events.', data_path, base_name)

    # make metadata instance
    metadata = limonade.data.Metadata(None, len(self.ch_list))

    # channel data is parsed and events reconstructed. Next it will be loaded
    data_dict, timing_data = self._load_channel_data(data_path, base_name)

    # metadata is created here. We set everything as fully as we can. Metadata is then saved and we are ready.
    metadata.total_time = int(total_time*1e9)
    metadata.dead_time = [timing_data['dt{}'.format(x)].sum() for x in range(len(self.ch_list))]
    # live and dead times are automatically got from t_cache. No need to worry.
    metadata.run_id = base_name
    metadata.name = self.config.det['name']
    metadata.notes = "Converted from .evt file at {}.".format(dt.datetime.fromtimestamp(time.time()))

    metadata.counts = total_counter
    metadata.input_counts = total_counter + empty_counter
    metadata.events = data_dict['time'].shape[0]
    print('events', data_dict['time'].shape[0], events)

    if start_time is None and stop_time is None:
        # no end or start run buffers
        print('Calculating start time from file timestamp')
        metadata.notes = metadata.notes + ' No start or end buffer - calculating time from file timestamp.'
        metadata.notes = metadata.notes + ' Recorded {} original events.'.format(events)
        start_time = dt.datetime.fromtimestamp(ch_file.stat().st_mtime) - dt.timedelta(seconds=total_time)

    if start_time is None:
        # For some reason there was no BEGUNBUF but ENDRUNBUF exists
        print('Calculating start time from stop time')
        metadata.notes = self.metadata.notes + ' No start buffer - calculating time from end time.'
        start_time = stop_time - dt.timedelta(seconds=total_time)

    if stop_time is None:
        # There was no ENDRUNBUF
        print('Calculating stop time from start time')
        metadata.notes = metadata.notes + ' No end buffer - calculating time from start buffer.'
        stop_time = start_time + dt.timedelta(seconds=total_time)

    metadata.start = start_time
    metadata.stop = stop_time
    ut.write_channel_metadata(data_path, base_name, -1, metadata.dump())
    return data_dict, timing_data

    '''
    class DSPECData(Data):
        def __init__(self, config, **kwargs):
            super().__init__(config, **kwargs)
            self.data_ext = 'Lis'
            self.name = 'DSPEC data'

        def _read_raw_data(self, data_path, save_metadata):
            """

            :param data_file:
            :return:
            """
            data_file = self.base_name + '.{}'.format(self.data_ext)

            chunk_size = 10000
            streamer = StreamData(data_path, self.base_name, 1, max_data_sz=chunk_size)

            livetime = 0
            rt_word = 0
            input_counts = 0

            self.data_mat = np.zeros((0, self.num_ch), dtype='uint16')
            self.data_dict['time'] = np.zeros((0,), dtype='uint64')

            E_chunk = np.zeros((chunk_size, self.num_ch), dtype='uint16')
            t_chunk = np.zeros((chunk_size,), dtype='uint64')
            input_counts = np.zeros((1,), dtype='uint64')
            counts = np.zeros((1,), dtype='uint64')

            with (data_path / data_file).open('rb') as df:
                header = df.read(256)
                total_time, live_time, start, stop = self._parse_header(header)
                evnt = True
                while evnt:
                    eventcounter = 0
                    while eventcounter < chunk_size:
                        try:
                            data_word = st.unpack('<I', df.read(4))[0]
                        except st.error:
                            print('{} events'.format(eventcounter))
                            evnt = False
                            break
                        except:
                            raise

                        if data_word & 0xc0000000 == 0xc0000000:  # data word
                            E_chunk[eventcounter, 0] = (data_word & 0x3fff0000) >> 16
                            t_chunk[eventcounter] = ((data_word & 0xffff) | rt_word) * 200  # to ns
                            eventcounter += 1
                        elif data_word & 0xc0000000 == 0x80000000:  # counter for 50000 ticks rollover
                            rt_word = (data_word & 0x3fffffff)*50000
                        elif data_word & 0xc0000000 == 0x40000000:  # live time in ns, 10 ms resolution
                            livetime = (data_word & 0x3fffffff)*1e7
                        elif data_word & 0xffff0000 == 0x4000000:  # ADC counts per 10 ms
                            input_counts[0] += data_word & 0xffff

                    self.data_mat = np.concatenate((self.data_mat, E_chunk[:eventcounter]))
                    self.data_dict['time'] = np.concatenate((self.data_dict['time'], t_chunk[:eventcounter]))
                    streamer.write([eventcounter], [(t_chunk[:eventcounter], E_chunk[:eventcounter])])  # stream to .dat file to speed up

            self.events = self.data_mat.shape[0]
            counts[0] = self.events


        def _parse_header(self, header):
            headerinfo = st.unpack('<iid', header[:16])
            if headerinfo[0] != -13:
                print('Invalid header for .Lis file')
                sys.exit()
            if headerinfo[1] != 2:
                print('List mode format {} not supported!'.format(headerinfo[1]))

            total_time = np.zeros((self.num_ch,), dtype='int64')
            live_time = np.zeros((self.num_ch,), dtype='int64')
            start_time = []
            stop_time = []

            stringinfo = st.unpack('<80c9c16c80cc4c', header[16:206])
            #ecal = st.unpack('<3f', header[206:218])
            #is_shapecal = st.unpack('<?', header[218:219])[0]
            #shapecal = st.unpack('<fff', header[219:231])
            gain, det_id, r_t, l_t = st.unpack('<iiff', header[231:247])
            total_time[0] = int(r_t*1e9)
            live_time[0] = int(l_t*1e9)
            # Stupid OLE Automation date format starts from 0 at 30.12.1899
            start_time.append(dt.datetime(1899, 12, 30, 00, 00, 00) + dt.timedelta(days=headerinfo[2]))
            stop_time.append(start_time[0] + dt.timedelta(seconds=r_t))

            return total_time, live_time, start_time, stop_time
    '''