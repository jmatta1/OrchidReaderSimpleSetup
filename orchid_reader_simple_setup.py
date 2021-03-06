#!/usr/bin/python
"""This script takes some basic input and asks the user some questions before
generating configuration files for OrchidReader and a queue script to run it"""
import sys
import os
import datetime
import struct
from orsslib import sub_batch_handling as sb_hnd
from orsslib import input_sanitizer as inp

FILE_HEADER_SIZE = 4096
BUFFER_SIZE = 2097152

DEFAULT_OUTDIR = "/data1/prospect/ProcessedData/OrchidAnalysis/TimeSeries_2017"

BATCH_SPLIT_TIME_DIFF = 120.0


def main():
    """Entry point for the script"""
    indir, outdir = read_cmdline()
    _, batch_name = os.path.split(indir)
    print "Input Directory is:", indir
    print "Base Output Directory is:", outdir
    print "\nIf this is incorrect use 'Ctrl+C' to stop execution"
    raw_input("Press Enter to continue...")
    # get the list of files and their header info
    print "Getting header & timestamp info"
    file_list = get_and_sort_file_list(indir)
    # now try to figure out where splits need to happen
    sub_batches = split_into_subbatches(file_list)
    # now ask users if they agree with the detector setups configured
    # for each sub batch
    check_sub_batch_info(sub_batches)
    sub_batches = get_proc_folders(outdir, sub_batches, batch_name)
    # now, for each sub batch, create the folder and the files to run the job
    batch_files = build_batch_scripts(sub_batches)
    # now create a small script that submits each of the queue scripts created
    sub_script_name = generate_sub_script(batch_files)
    os.system("chmod -R 774 {0:s}".format(sub_script_name))
    out_str = ("batches to run" if len(batch_files) == 0 else "batch to run")
    print "Created", len(batch_files), out_str
    for number, batch in enumerate(batch_files):
        print "Batch #{0:d}".format(number)
        print "    Output directory:", batch[4]
        print "  Reader Config File:", batch[0]
        print "     Input List File:", batch[2]
        print " Detector Setup File:", batch[1]
        print "   Queue Script File:", batch[3]
        os.system("chmod -R 774 {0:s}".format(batch[4]))
    print ""
    print "Generated", sub_script_name
    print "  It will automatically submit the generated batch scripts"


def generate_sub_script(batch_files):
    """This function takes the list of batch files and makes a simple batch
    script that jumps into each directory it generated, and submits the output
    script

    Parameters
    ----------
    batch_files : list
        A list of the files generated for batch processing, in order they are
        Reader config file, Detector Setup File, Input List File, Queue Script
        File, and finally, the Output Directory

    Returns
    -------
    sub_script_name : str
        Path to the script generated to submit the individual files to the
        queue for processing
    """
    outfile = None
    if inp.get_yes_no("Append to existing submit_script", default_value=True):
        outfile = open("./submit_script", 'a')
    else:
        outfile = open("./submit_script", 'w')
        outfile.write("#!/usr/bin/bash\n")
    for num, batch in enumerate(batch_files):
        outfile.write("# Batch number: {0:d}\n".format(num))
        outfile.write("cd {0:s}\n".format(batch[4]))
        outfile.write("qsub ./batch_script\n")
    outfile.close()
    return "./submit_script"


def build_batch_scripts(sub_batches):
    """This function takes the list of sub batch data and uses it to create
    folders, orchid reader config files, and other material necessary to run
    the first step of the analysis chain.

    Parameters
    ----------
    sub_batches : list
        This is a list of tuples where each tuple contains the following:
            list of file information
            ArraySetup name and object
            Run start and stop time
            Batch name and folder name

    Returns
    -------
    file_information : list of tuples
        A list of the tuples of the information of generated files for each
        sub_batch, including: orchid cfg file path, detector setup file path,
        orchid raw data file list, queue sub script, and output directory
    """
    out_data = []
    email = inp.get_str("What email should failures be sent to")
    # iterate through the list of sub batches, handling each individually
    for files, setup, _, pos, folder in sub_batches:
        # first ensure that the folder for the output exists
        if not os.path.exists(folder[1]):
            os.makedirs(folder[1])
        elif not os.path.isdir(folder[1]):
            print "Output Path Exists and is NOT a Directory"
            print "  Unrecoverable error, run setup again with "\
                "different base dir"
            sys.exit()
        # now write the raw data list file
        file_list_name = os.path.join(folder[1], "input_file_list")
        write_file_list(file_list_name, files)
        # now write the detector setup file
        det_setup_name = os.path.join(folder[1], "detector_setup")
        setup[1].write_array_setup(det_setup_name)
        # now write the config file
        cfg_name = os.path.join(folder[1], "batch_cfg")
        write_cfg_file(cfg_name, file_list_name, det_setup_name, folder[1],
                       pos)
        script_name = os.path.join(folder[1], "batch_script")
        write_qsub_script(script_name, folder[1], email)
        out_data.append((cfg_name, det_setup_name, file_list_name, script_name,
                         folder[1]))
    return out_data


def write_qsub_script(script_name, folder, email):
    """Takes the name of the output script and the batch directory and writes
    the qsub script there after asking the user for their email address

    Parameters
    ----------
    script_name : str
        The path to the file the script will be written to
    folder : str
        The path to the batch directory
    email : str
        The email address to supply to the batch script(s)
    """
    fmt_dict = {}
    fmt_dict["email"] = email
    fmt_dict["reader_dest"] = os.path.join(folder, "ORCHIDReader")
    fmt_dict["batch_dir"] = folder
    outfile = open(script_name, 'w')
    outfile.write(SCRIPT_TMPL.format(**fmt_dict))
    outfile.close()


def write_cfg_file(cfg_name, file_list_name, det_setup_name, folder, pos):
    """This function takes the path of the output file, list file, det setup
    file, and the output folder, asks the user for the position of the array
    in this run and then writes the OrchidReader config file

    Parameters
    ----------
    cfg_name : str
        The path to the config file to be written
    file_list_name : str
        The path to the list of input files that was written
    det_setup_name : str
        The path to the detector setup file that was written
    folder : str
        the output folder for the run
    pos : tuple
        The X and Y position pair
    """
    # first get the user input for array position and integration time
    fmt_dict = {}
    fmt_dict["root_file"] = os.path.join(folder, "batch_hists.root")
    fmt_dict["batch_data_csv"] = os.path.join(folder, "batch_data.csv")
    fmt_dict["det_data_csv"] = os.path.join(folder, "det_meta_data.csv")
    fmt_dict["run_data_csv"] = os.path.join(folder, "run_data.csv")
    fmt_dict["input_list"] = file_list_name
    fmt_dict["array_data_in"] = det_setup_name
    fmt_dict["array_x_pos"] = pos[1][0]
    fmt_dict["array_y_pos"] = pos[1][1]
    cfile = open(cfg_name, 'w')
    cfile.write(CONFIG_TMPL.format(**fmt_dict))
    cfile.close()


def write_file_list(out_name, files):
    """This function takes an output file name and a list of files and writes
    a list of file names to the output file name

    Parameters
    ----------
    out_name : str
        The name of the file that will contain the list of files
    """
    outfile = open(out_name, 'w')
    outfile.write("{0:s}".format(files[0][0]))
    for fdat in files[1:]:
        outfile.write("\n{0:s}".format(fdat[0]))
    outfile.write("\n")


def get_proc_folders(outdir, sub_batches, batch_name):
    """Takes the list of sub_batches and calculates a seperate batch name
    for each

    Parameters
    ----------
    outdir : std
        Name of the base output directory
    sub_batches : list
        list of lists where each list is a sub-batch of file data
    batch_name : str
        string containing the batch name of the overall batch

    Returns
    -------
    batch_sets : list
        list of sets of files for each sub batch, also contains the detector
        setup for that sub batch, a begin and end time for that sub batch,
        and a sub_batch_name and sub_batch folder for that sub batch
    """
    # short circuit for the special case of only one sub batch
    if len(sub_batches) == 1:
        temp = sub_batches[0]
        return [(temp[0], temp[1], temp[2], temp[3],
                 (batch_name, os.path.join(outdir, batch_name)))]
    # otherwise there is more than one batch, name them
    out_batches = []
    for ind, batch in enumerate(sub_batches):
        sub_name = "{0:s}_{1:d}".format(batch_name, ind)
        out_path = os.path.join(outdir, sub_name)
        out_batches.append((batch[0], batch[1], batch[2],
                            batch[3], (sub_name, out_path)))
    return out_batches


def check_sub_batch_info(sub_batches):
    """Takes a list of sub batches, asks the user about them, and if the user
    desires this will allow them to modify the detector setup for that batch

    Parameters
    ----------
    sub_batches : list
        list of lists where each list is a sub-batch of file data
    """
    count = len(sub_batches)
    for batch, setup, times, position in sub_batches:
        print DET_MOD_STR.format(count)
        check_sub_batch(batch, setup, times, position)


def check_sub_batch(batch, setup, times, pos):
    """Takes a specific sub batch, displays information about it and allows the
    user to modify it if they wish

    Parameters
    ----------
    batch : list
        list of file data tuples
    setup : tuple
        Name of setup and ArraySetup in a pair
    times : tuple
        Header time of the first file and last modification time of the last
        file
    pos : tuple
        X-Y position pair
    """
    start_time = times[0].strftime("%Y-%m-%d %H:%M:%S.%f")
    stop_time = times[1].strftime("%Y-%m-%d %H:%M:%S.%f")
    print SUB_BATCH_INFO.format(batch[0][0], batch[-1][0], start_time,
                                stop_time, setup[0], pos[0],
                                pos[1][0], pos[1][1])
    setup[1].print_array_setup()
    print ""
    ans = inp.get_yes_no("Do you wish to edit the array position",
                         default_value=False)
    while ans:
        xpos = inp.get_float("New X Position")
        ypos = inp.get_float("New Y Position")
        pos[1][0] = xpos
        pos[1][1] = ypos
        print SUB_BATCH_INFO.format(batch[0][0], batch[-1][0], start_time,
                                    stop_time, setup[0], pos[0], pos[1][0],
                                    pos[1][1])
        setup[1].print_array_setup()
        ans = inp.get_yes_no("Do you wish to edit the array position",
                             default_value=False)
    ans = inp.get_yes_no("Do you wish to edit the detector setup",
                         default_value=False)
    while ans:
        setup[1].get_array_changes()
        print SUB_BATCH_INFO.format(batch[0][0], batch[-1][0], start_time,
                                    stop_time, setup[0], pos[0], pos[1][0],
                                    pos[1][1])
        setup[1].print_array_setup()
        ans = inp.get_yes_no("Do you wish to edit the detector setup",
                             default_value=False)


def split_into_subbatches(file_list):
    """Takes a list of files and the special handling data and figures out how
    to split the files into sub-batches due to time differences or special
    handling cases

    Parameters
    ----------
    file_list : list
        List of file names and file header info pairs

    Returns
    -------
    sub_batches : list
        List where each sub_list is a set of files and file header info that
        belongs together in a single list
    """
    sub_batches = sb_hnd.split_sub_batches_det_setup(file_list)
    sub_batches = sb_hnd.split_sub_batches_time(sub_batches,
                                                BATCH_SPLIT_TIME_DIFF)
    sub_batches = sb_hnd.split_sub_batches_position(sub_batches)
    return sub_batches


def get_and_sort_file_list(indir):
    """Retrieves the list of files in the input directory and gather statistics
    on them

    Parameters
    ----------
    indir : str
        The directory given as an input directory for the raw data

    Returns
    -------
    file_list : list
        A list where each sublist contains file information
    """
    data_files = [os.path.join(indir, fn) for fn in os.listdir(indir)
                  if os.path.isfile(os.path.join(indir, fn))]
    files = [[fn, get_file_header_data(fn)] for fn in data_files]
    files.sort(key=lambda x: x[1][0])
    return files


def get_file_header_data(fname):
    """Takes a file name, reads the file header data and returns date time data

    Parameters
    ----------
    fname : str
        Full path to the file

    Returns
    -------
    date : datetime.datetime object
        The date as stated by the file header
    run_name: str
        The run name as stated by the file header
    run_num: int
        The run number as stated by the file header
    seq_num: int
        The file sequence number as stated by the file header
    mod_time: datetime.datetime object
        The date of last modification given by the OS
    first_ts : int
        The timestamp of the first event in the first buffer of the file
    last_ts : int
        The timestamp of the last event in the last buffer of the file
    """
    # first figure out what the file size is
    size = os.path.getsize(fname)
    if size < 2101248:
        print "Invalid file, it has a size < 1 Buffer plus a file header"
        print fname
    # open as binary
    in_file = open(fname, 'rb')
    # check for that strange buffer header at beginning of file bug
    remainder = ((size - FILE_HEADER_SIZE) % BUFFER_SIZE)
    last_buf_offset = 0
    # check for strange buffer header at beginning of file
    if remainder >= 8192:
        rawdata = in_file.read(4)
        start_int = struct.unpack("<I", rawdata[0:])[0]
        in_file.seek(0, 0)
        if start_int == 0xf0f0f0f0:
            last_buf_offset += 8192
            in_file.seek(8192, 0)
    # check if the excess size has been accounted for, if not, assume that
    # there is also a broken buffer at the end
    num_buffers = ((size - FILE_HEADER_SIZE - remainder) / BUFFER_SIZE)
    last_buf_offset += FILE_HEADER_SIZE
    last_buf_offset += (BUFFER_SIZE * (num_buffers-1))
    # now last_buf_offset should point to the start of the last buffer
    # now read the information from the file header
    date, run_name, run_num, seq_num = read_file_header_info(in_file)
    # now read the first DppPsd event of the first buffer and get its timestamp
    first_ts = read_first_time_stamp(in_file)
    # get the last buffer end time
    mod_time = read_last_buffer_end(in_file, last_buf_offset)
    # read the last DppPsd event of the last buffer and get its timestamp
    last_ts = read_last_time_stamp(in_file)
    in_file.close()
    # return everything
    return (date, run_name, run_num, seq_num, mod_time, first_ts, last_ts)


def read_last_time_stamp(in_file):
    """Reads the last digitizer event's timestamp in the last buffer of the
    file

    Parameters
    ----------
    in_file : file object
        The file object for the opened data file

    Returns
    -------
    last_ts : int
        the time stamp associated with the last event of the last file buffer
    """
    in_file.seek(8160, 1)
    rawdata = in_file.read(2088960)
    ind = 0
    last_ts = -1
    end = False
    while not end and ind < 2088958:
        first, second = struct.unpack("<BB", rawdata[ind:ind+2])
        if first == 0x0f and second == 0x02:
            lotime, hitime = struct.unpack("<IH", rawdata[ind+4:ind+10])
            last_ts = ((hitime << 31) + lotime)
        elif first == 0 and second == 0:
            end = True
            break
        else:
            first += (second << 8)
        ind += first
    return last_ts


def read_last_buffer_end(in_file, last_buf_offset):
    """Reads the final modification time of the last buffer in the file

     Parameters
    ----------
    in_file : file object
        The file object for the opened data file
    last_buf_offset : int
        The offset in bytes of the start of the last buffer in the file

    Returns
    -------
    mod_time : datetime.datetime
        the last modification time of the file by ORCHID
    """
    # seek to last buffer start + 24 bytes (so we point at last end buff time)
    in_file.seek((last_buf_offset), 0)
    rawdata = in_file.read(32)
    # first calculate the location of the last buffer
    timestamp = float(struct.unpack("<q", rawdata[24:])[0])/1000000.0
    return datetime.datetime.fromtimestamp(timestamp)


def read_first_time_stamp(in_file):
    """Reads the first digitizer event's timestamp in the first buffer of the
    file

    Parameters
    ----------
    in_file : file object
        The file object for the opened data file

    Returns
    -------
    first_ts : int
        the time stamp associated with the first event of the first file buffer
    """
    in_file.seek(12124, 1)  # skip remainder of file header and buffer header
    rawdata = in_file.read(16384)
    first_ts = -1
    ind = 0
    while first_ts == -1:
        first = struct.unpack("<H", rawdata[ind:ind+2])[0]
        if first == 527:
            # get the timestamp
            lotime, hitime = struct.unpack("<IH", rawdata[ind+4:ind+10])
            first_ts = ((hitime << 31) + lotime)
        else:
            ind += first
    return first_ts


def read_file_header_info(in_file):
    """Reads the relevant information from the file header

    Parameters
    ----------
    in_file : file object
        The file object for the opened data file

    Returns
    -------
    date : datetime.datetime
        The datetime object representing the start of file writing
    run_name : str
        The name of the run
    run_num : int
        The number of the run
    seq_num : int
        The sequence number of the file
    """
    # read the first 164 bytes
    rawdata = in_file.read(164)
    # convert the raw date string in the header
    date = datetime.datetime.strptime(rawdata[26:56].strip('\x00'),
                                      "%Y-%m-%dT%H:%M:%S.%f")
    # convert the raw run name in the header
    run_name = rawdata[56:156].strip('\x00')
    # convert the raw run and seq numbers in the header
    run_num, seq_num = struct.unpack("<II", rawdata[156:])
    return (date, run_name, run_num, seq_num)


def read_cmdline():
    """Reads command line parameters and returns the input and output
    directories

    Returns
    -------
    indir : str
        String with the path of the batch input directory
    outdir : std
        String with the path of the batch processed output directory
    """
    outdir = ""
    indir = ""
    if not len(sys.argv) in [2, 3]:  # not enough or too much input
        print HELP_STR.format(sys.argv[0], DEFAULT_OUTDIR)
        sys.exit()
    else:  # right number of arguments
        # grab the input path
        indir = grab_and_test_input_dir()
        # check if we need to calculate the output path
        if len(sys.argv) == 2:
            # use default output base directory
            outdir = DEFAULT_OUTDIR
        elif len(sys.argv) == 3:
            # grab the output directory
            outdir = trim_trailing_slash(sys.argv[2])
        # test the output directory
        if not os.path.exists(outdir):
            print "Creating output directory:", outdir
            os.makedirs(outdir)
        elif not os.path.isdir(outdir):
            print "\n  BatchOutputBaseDirectory should be a directory or"\
                  "nonexistent"
            print HELP_STR.format(sys.argv[0], DEFAULT_OUTDIR)
            sys.exit()
    # return the input directory and output directory
    return indir, outdir


def grab_and_test_input_dir():
    """Reads and tests the input directory

    Returns
    -------
    indir : str
        String with the path of the batch input directory
    tail : str
        String with the last part of the indir path
    """
    indir = sys.argv[1]
    indir = trim_trailing_slash(indir)
    # test if the directory exists
    if not os.path.isdir(indir):
        print "\n  BatchInputDirectory needs to be a directory\n"
        print HELP_STR.format(sys.argv[0], DEFAULT_OUTDIR)
        sys.exit()
    return indir


def trim_trailing_slash(path):
    """If path ends in a '/' and is not the root dir this will trim it and
    return the trimmed result

    Parameters
    ----------
    path : str
        String with the path to be checked for trailing slash

    Returns
    -------
    trimmed_path : str
        Path without a trailing slash (unless it is the root directory)
    """
    head, tail = os.path.split(path)
    if tail == "":  # did it end in a '/'?
        return head
    return path


SCRIPT_TMPL = """
#!/bin/bash
#PBS -M {email:s}
READER_DEST={reader_dest:s}
BATCH_DIR={batch_dir:s}
# copy the source code for orchid reader
cp -r $ORCHID_READER_SRC $READER_DEST
cd $READER_DEST
# build our copy
make release
cd $BATCH_DIR
cp $READER_DEST/orchidReader ./orchidReader
# after moving our copy to the primary dir, run it
./orchidReader batch_cfg
chmod -R 774 $BATCH_DIR
# delete our copy of ORCHID Reader
rm -rf $READER_DEST
rm orchidReader
"""


CONFIG_TMPL = """[StartConfig]
# This area has the list of files that will have data output to them or
# the option to activate and deactivate certain outputs

# this is the path to the file that will hold all the root histograms and base
# run data
RootFilePath="{root_file:s}"

# this is the path to a csv file that will hold the batch summary data
BatchMetaDataPath="{batch_data_csv:s}"

# this is the path to a csv file that will hold the detector summary data for
# this batch
DetMetaDataPath="{det_data_csv:s}"

# this is the path to a csv file that will hold run summary data
RunCsvPath="{run_data_csv:s}"

# this option controls if a root tree of the events will be generated
# while the tree is supremely flexible, it takes a great deal of space and
# searches in the tree take a great deal of time, additionally, activating this
# option will cause the program to run much more slowly
GenerateRootTree = False

# This is the path to the root tree output file.
# this option only needs to be set if GenerateRootTree is True
# RootTreeFilePath = ""


# Below here is input to the program

# this is the path to the file that contains the list of paths of raw input
# files to be parsed for this batch
ListFilePath="{input_list:s}"

# this is the file that contains information about the array configuration
# and detector setup
# Included is:
#   Position mapping (offsets of detectors in inches, from the array position)
#   HV Channel Mapping, which HV channels apply to which detectors
#   Detector Types
#   Energy Projection PSD Threshold
#   PSD Projection Energy Threshold
ArrayDataPath="{array_data_in:s}"

# X and Y positions of the array, 0,0 is the hinge corner of the back door of
# the MIF, positive X is towards the reactor wall, positive Y is towards the
# big door to the outside, and positive Z is up
ArrayXPosition={array_x_pos:4.1f} #Normal=142.0 Out of the way=234.0 or 165.0
ArrayYPosition={array_y_pos:4.1f} #Normal=74.0  Out of the way=279.0 or -124.0

# sometimes, if there is a substantial lab between the run being changed and a
# new run being started, processing the first buffer of the first file of the
# run can seriously affect rates, this affects position scans almost
# exclusively anyways, this variable allows the system to skip the first buffer
# of the first file in its scan, if it is true, the buffer is processed, if it
# is false, the buffer is skipped
ProcessFirstBuffer = True

# this is the nominal number of seconds to integrate files for
HistIntegrationTime=600.0

# The channel buffer length needs to be long enough that the number of events
# that are produced by the detector across the length of time that it takes for
# the slowest detector pair to push a single buffer. Since the normal setup
# has the maximum 1023 events per buffer and the slowest detector pair is the
# two 3He detectors looking at the different detector configurations in both
# reactor on and reactor off shows that the worst mismatch comes in reactor off
# The main position had a combined 3He rate of 4.79 Hz. This gives 213.6 seconds
# per 3He buffer. Padding buffers to handle the time required for 5 3He buffers
# to arrive, gives, when checked across several cases, gives the following
# buffer sizes, which should be plenty large enough since the system will only
# try to get 4 3He buffers at a time
BufferLength = [1275000, 1350000, 500000, 1500000, 950000, 1325000, 100000, 25000, 2775000, 6175000, 4325000, 4475000, 2025000, 2775000, 2050000, 2200000]

[EndConfig]
"""


SUB_BATCH_INFO = """    First File: {0:s}
     Last File: {1:s}
    Start Time: {2:s}
      End Time: {3:s}
Det Setup Name: {4:s}
 Position Name: {5:s}
      Position: X={6:4.1f}, Y={7:4.1f}

Detector Setup:"""


DET_MOD_STR = """
Found {0:d} batches in the folder
  Information about the batches will be displayed one by one. You will be
  able to see more complete information and modify detector setups per batch"""


HELP_STR = """
Usage:
  {0:s} BatchInputDirectory [BatchOutputDirectory]
  The default output root directory is: {1:s}

 Ex:
  {0:s} /data1/prospect/Data/ORCHID_Data/Batch7
   Calculates BatchOutputDirectory to be: {1:s}/Batch7

  {0:s} /data1/prospect/Data/ORCHID_Data/Batch7 /data1/prospect/ProcessedData"
   Calculates BatchOutputDirectory to be: /data1/prospect/ProcessedData

"""

if __name__ == "__main__":
    main()
