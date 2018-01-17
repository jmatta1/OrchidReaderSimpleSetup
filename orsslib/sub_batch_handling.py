"""This file contains functions and global constants that allow known cases
that need special handling to be addressed"""
import fnmatch  # for file name pattern matching
import orsslib.position_changes as pc
import orsslib.setup_changes as sc

MIN_TS_THRESH = 140737488355
MAX_TS_THRESH = 140596750866972
TS_MISORDER_THRESH = 5000000000


def split_sub_batches_det_setup(file_list):
    """Takes a file_list and splits runs if they contain the patterns
    defined in setup_changes.py, also tries to guess detector setups from what
    is known

    Parameters
    ----------
    file_list : list
        list of file data

    Returns
    -------
    batch_sets : list
        list of sets of files for each sub batch, also contains the detector
        setup for that sub batch
    """
    batch_sets = []
    curr_batch = []
    prev_det = 0
    curr_det = 0
    prev_name = sc.EXCEPTION_NAME[0]
    curr_name = sc.EXCEPTION_NAME[0]
    for dat in file_list:
        # reset current detector to default
        curr_det = 0
        # check if the file matches one of the exception patterns
        for ind, patterns in enumerate(sc.EXCEPTION_PATTERN):
            # check if this is an exception run
            for chk in patterns:
                if chk in dat[0]:
                    curr_det = ind + 1
                    curr_name = sc.EXCEPTION_NAME[ind + 1]
                    break
        # check if the file before this one was a different det setup
        if curr_det == prev_det:
            curr_batch.append((dat[0], dat[1][0], dat[1][1], dat[1][2],
                               dat[1][3], dat[1][4], dat[1][5], dat[1][6]))
        else:
            if len(curr_batch) > 0:
                batch_sets.append((curr_batch, (prev_name,
                                                sc.EXCEPTION_DATA[prev_det])))
            prev_det = curr_det
            prev_name = curr_name
            curr_batch = [(dat[0], dat[1][0], dat[1][1], dat[1][2], dat[1][3],
                           dat[1][4], dat[1][5], dat[1][6])]
    # we have made it through the list of files, append the last batch with
    # the guessed detector setup
    batch_sets.append((curr_batch, (curr_name, sc.EXCEPTION_DATA[curr_det])))
    return batch_sets


def split_sub_batches_time(sub_batches, threshold):
    """Takes a set of sub batches and splits them further runs if they contain
    time differences between the beginning of a file and the end of a previous
    file greater than threshold, also checks for new runs from digitizer
    timestamp resets using a heuristic and breaks the run if there is a
    timestamp reset that is not due to running past the end of ~281000 seconds

    Parameters
    ----------
    sub_batches : list
        list of lists where each list is a sub-batch of file data
    threshold : int
        minimum number of seconds between end and beginning of two files to
        force a split into two different batches

    Returns
    -------
    batch_sets : list
        list of sets of files for each sub batch, also contains the detector
        setup for that sub batch, and a begin and end time for that sub batch
    """
    batch_sets = []
    curr_batch = []
    for file_list, setup in sub_batches:
        curr_batch = []
        prev_time = file_list[0][5]
        first_time = file_list[0][1]
        last_time = file_list[0][5]
        prev_ts = file_list[0][7]
        count = 0
        for fdat in file_list:
            maintain_batch = True
            # determine if the batch needs to be broken
            if (fdat[1]-prev_time).total_seconds() > threshold:
                maintain_batch = False
            if count != 0 and (fdat[6] + TS_MISORDER_THRESH) < prev_ts:
                if not (prev_ts > MAX_TS_THRESH and fdat[6] < MIN_TS_THRESH):
                    maintain_batch = False
            # break the batch if need be
            if maintain_batch:
                curr_batch.append(fdat)
                last_time = fdat[5]
            else:
                batch_sets.append((curr_batch, setup, (first_time, last_time)))
                first_time = fdat[1]
                last_time = fdat[5]
                curr_batch = [fdat]
            prev_ts = fdat[7]
            prev_time = fdat[5]
            count += 1
        batch_sets.append((curr_batch, setup, (first_time, last_time)))
    return batch_sets


def split_sub_batches_position(sub_batches):
    """This takes a list of sub batches and attempts to split them based on
    position exceptions, kind of like how things were split by detector setup
    exceptions previously

    Parameters
    ----------
    sub_batches : list
        list of lists where each list is a sub-batch of file data

    Returns
    -------
    batch_sets : list
        list of sets of files for each sub batch, also contains the detector
        setup for that sub batch, a begin and end time for that sub batch, and
        the x and y positions for the array for that run
    """
    batch_sets = []
    curr_batch = []
    prev_pos = 0
    curr_pos = 0
    prev_name = pc.EXCEPTION_NAME[0]
    curr_name = pc.EXCEPTION_NAME[0]
    for file_list, setup, dates in sub_batches:
        curr_batch = []
        for fdat in file_list:
            for ind, patterns in enumerate(pc.EXCEPTION_PATTERN):
                # check if this is a position exception run
                for chk in patterns:
                    #if chk in fdat[0]:
                    if fnmatch.fnmatch(fdat[0], chk):
                        curr_pos = ind + 1
                        curr_name = pc.EXCEPTION_NAME[ind + 1]
                        break
            # check if the file before this one was a different position
            if curr_pos == prev_pos:
                curr_batch.append(fdat)
            else:
                if len(curr_batch) > 0:
                    batch_sets.append((curr_batch, setup, dates,
                                       [prev_name,
                                        list(pc.EXCEPTION_DATA[prev_pos])]))
                prev_pos = curr_pos
                prev_name = curr_name
                curr_batch = [fdat]
        batch_sets.append((curr_batch, setup, dates,
                           [curr_name, list(pc.EXCEPTION_DATA[curr_pos])]))
    return batch_sets
