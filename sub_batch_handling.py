"""This file contains functions and global constants that allow known cases
that need special handling to be addressed"""
import detector_setups as ds

###############################################################################
# information for breaking the batches up based on detector setup
###############################################################################
# list of file name patterns that are contained in all the files that have data
# from the CeBr3 runs
CEBR_RUN_PATTERNS = ["Sept28_0001.dat", "Sept29_0000.dat", "Sept29_0001.dat",
                     "Sept30_0000.dat", "Sept30_0001.dat", "Sept_30_0000.dat",
                     "Oct1_0000.dat", "Oct2_0000.dat", "Oct3_0000.dat",
                     "Oct4_0000.dat"]

# list of the file name patterns that are contained in all the files that have
# data from the time that the 3He tubes had to be removed
NO_HE_RUN_PATTERNS = ["Sept14_0000.dat", "Sept14_0001.dat", "Sept14_0002.dat",
                      "Sept14_0003.dat", "Sept14_0004.dat", "Sept14_0005.dat",
                      "Sept15_0000.dat", "Sept16_0000.dat", "Sept18_0000.dat",
                      "Sept19_0000.dat", "Sept19_0001.dat"]

# list of detector setups for convenient access
DET_SETUPS = [ds.DEFAULT_SETUP, ds.CEBR_SETUP, ds.NO_HE_SETUP]

# list of exception pattern names in the same order as setups, including def
EXCEP_NAMES = ["Default", "CeBr3", "No_3He"]

# list of exception patterns in the same order as the det setups, minus default
EXCEP_PATTERNS = [CEBR_RUN_PATTERNS, NO_HE_RUN_PATTERNS]

###############################################################################
# information for breaking the batches up based on array position
###############################################################################
# list of file name patterns that match when the system was positioned past the
# Reactor wall next to the saphire array cooling setup
PAST_RX_WALL_PATTERNS = ["Jan12_2017_pastRxWall_0000",
                         "Jan13_2017_pastRxWall_0000"]

# list of file name patterns that match when the system was positioned close to
# the door that leads towards the cold source room, due to surveyors 'shooting'
# the area for PROSPECT
SURVEYING_PATTERNS = ["May10_2017_0002.dat", "May11_2017_0000.dat",
                      "May12_2017_0000.dat", "May15_2017_0000.dat",
                      "May16_2017_0000.dat", "May18_2017_0000.dat",
                      "May19_2017_0000.dat", "May21_2017_0000.dat",
                      "May22_2017_0000.dat", "May22_2017_0001.dat"]

# list of array positions for the time series runs
ARRAY_POSITIONS = [(142.0, 74.0), (234.0, 279.0), (165.0, -124.0)]

# list of names for the array positions
POS_NAMES = ["Default", "PastRxWall", "CloseToColdSrcCtrlRoom"]

# list of position exception patterns (deliberately sans the default)
POS_PATTERNS = [PAST_RX_WALL_PATTERNS, SURVEYING_PATTERNS]

def split_sub_batches_det_setup(file_list):
    """Takes a file_list and splits runs if they contain the patterns
    defined above, also tries to guess detector setups from what is known

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
    prev_name = EXCEP_NAMES[0]
    curr_name = EXCEP_NAMES[0]
    for dat in file_list:
        # reset current detector to default
        curr_det = 0
        # check if the file matches one of the exception patterns
        for ind, patterns in enumerate(EXCEP_PATTERNS):
            # check if this is an exception run
            for chk in patterns:
                if chk in dat[0]:
                    curr_det = ind + 1
                    curr_name = EXCEP_NAMES[ind + 1]
                    break
        # check if the file before this one was a different det setup
        if curr_det == prev_det:
            curr_batch.append((dat[0], dat[1][0], dat[1][1], dat[1][2],
                               dat[1][3], dat[1][4]))
        else:
            if len(curr_batch) > 0:
                batch_sets.append((curr_batch, (prev_name,
                                                DET_SETUPS[prev_det])))
            prev_det = curr_det
            prev_name = curr_name
            curr_batch = [(dat[0], dat[1][0], dat[1][1], dat[1][2], dat[1][3],
                           dat[1][4])]
    # we have made it through the list of files, append the last batch with
    # the guessed detector setup
    batch_sets.append((curr_batch, (curr_name, DET_SETUPS[curr_det])))
    return batch_sets


def split_sub_batches_time(sub_batches, threshold):
    """Takes a set of sub batches and splits them further runs if they contain
    time differences between the beginning of a file and the end of a previous
    file greater than threshold

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
        for fdat in file_list:
            if (fdat[1]-prev_time).total_seconds() <= threshold:
                curr_batch.append(fdat)
                last_time = fdat[5]
            else:
                batch_sets.append((curr_batch, setup, (first_time, last_time)))
                first_time = fdat[1]
                last_time = fdat[5]
                curr_batch = [fdat]
            prev_time = fdat[5]
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
    prev_name = POS_NAMES[0]
    curr_name = POS_NAMES[0]
    for file_list, setup, dates in sub_batches:
        curr_batch = []
        for fdat in file_list:
            for ind, patterns in enumerate(POS_PATTERNS):
                # check if this is a position exception run
                for chk in patterns:
                    if chk in fdat[0]:
                        curr_pos = ind + 1
                        curr_name = POS_NAMES[ind + 1]
                        break
            # check if the file before this one was a different position
            if curr_pos == prev_pos:
                curr_batch.append(fdat)
            else:
                if len(curr_batch) > 0:
                    batch_sets.append((curr_batch, setup, dates,
                                       [prev_name, ARRAY_POSITIONS[prev_pos]]))
                prev_pos = curr_pos
                prev_name = curr_name
                curr_batch = [fdat]
        batch_sets.append((curr_batch, setup, dates,
                           [curr_name, ARRAY_POSITIONS[curr_pos]]))
    return batch_sets
