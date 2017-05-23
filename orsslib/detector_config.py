"""This file contains the definition of the detector setup class and several
default setups"""
import copy
import os


COL_HEADERS = """Column Headings:
 0 - detector number, not "slot number" but instead a unique detector ID
 1 - digitizer board number, 2 - digitizer channel number
 3 - mpod board number,      4 - mpod channel number
 5 - Det X offset,           6 - Det Y offset,             7 - Det Z offset
 8 - Det Type (Options are: NaI, LS, CeBr3, HeMod, HeUnmod)
 9 - Det PSD Projection Energy Threshold (projection will go from 0 to Thres)
10 - Det Energy Projection PSD Threshold (projection will go from 0 to Thres)
 0, 1,  2, 3,  4,   5,    6,    7,       8,       9,   10
----------------------------------------------------------"""


COL_HEADERS_FILE = """#  0 - detector number, not "slot number" but instead a unique detector ID
#  1 - digitizer board number
#  2 - digitizer channel number
#  3 - mpod board number
#  4 - mpod channel number
#  5 - Det X offset
#  6 - Det Y offset
#  7 - Det Z offset
#  8 - Det Type (Options are: NaI, LS, CeBr3, HeMod, HeUnmod)
#  9 - Det PSD Projection Energy Threshold (projection will go from 0 to Thres)
# 10 - Det Energy Projection PSD Threshold (projection will go from 0 to Thres)
#0, 1,  2, 3,  4,   5,    6,    7,       8,       9,   10"""


DET_FORMAT_STR = "{0:2d}, {1:1d}, {2:2d}, {3:1d}, {4:2d}, {5:3.1f}, {6:4.1f},"\
    " {7:4.1f}, {8:>7s}, {9:5.1f}, {10:4.2f}"

DET_FORMAT_STR_FILE = "\n{0:2d}, {1:1d}, {2:2d}, {3:1d}, {4:2d}, {5:3.1f}, "\
    "{6:4.1f}, {7:4.1f}, {8:>7s}, {9:5.1f}, {10:4.2f}"


class DetectorSetup(object):
    """This class contains the information for a single detector's setup in
    the array for OrchidReader"""
    def __init__(self, connect, pos, det_type, threshs):
        """Initializes the detector setup

        Parameters
        ----------
        connect[0] : (int, int)
            The digitizer board number and digitizer channel number as a tuple
        connect[1] : (int, int)
            The MPOD HV board number and MPOD HV channel number as a tuple
        pos : (float, float, float)
            The X, Y, and Z offsets (in inches) of the detector from the array
            position
        det_type : str
            The string identifying the detector type, current options are:
            NaI, LS, CeBr3, HeMod, HeUnmod
        threshs : (float, float)
            The maximum energy to be included in the PSD projection and the
            maximum PSD to include in the energy projection of the 2D spectrum
            for the detector, written as a tuple.
        """
        self.digi_pair = connect[0]
        self.mpod_pair = connect[1]
        self.pos_offset = pos
        self.det_type = det_type
        self.thresh_pair = threshs

    def change_params(self, connect=None, pos=None, threshs=None):
        """Allows one or more parameter sets to be changed

        Parameters
        ----------
        connect[0] : (int, int)
            The digitizer board number and digitizer channel number as a tuple
        connect[1] : (int, int)
            The MPOD HV board number and MPOD HV channel number as a tuple
        pos : (float, float, float)
            The X, Y, and Z offsets (in inches) of the detector from the array
            position
        threshs : (float, float)
            The maximum energy to be included in the PSD projection and the
            maximum PSD to include in the energy projection of the 2D spectrum
            for the detector, written as a tuple.
        """
        if connect is not None:
            self.digi_pair = connect[0]
            self.mpod_pair = connect[1]
        if pos is not None:
            self.pos_offset = pos
        if threshs is not None:
            self.thresh_pair = threshs

    def change_type(self, det_type):
        """Change the type of the detector

        Parameters
        ----------
        det_type : str
            The string identifying the detector type, current options are:
            NaI, LS, CeBr3, HeMod, HeUnmod
        """
        self.det_type = det_type

    def get_tuple(self):
        """Returns a tuple for pretty printing"""
        return (self.digi_pair[0], self.digi_pair[1], self.mpod_pair[0],
                self.mpod_pair[1], self.pos_offset[0], self.pos_offset[1],
                self.pos_offset[2], self.det_type, self.thresh_pair[0],
                self.thresh_pair[1])

    def print_self(self, detnum):
        """Prints the detector setup in a pretty way

        Parameters
        ----------
        detnum : int
            The detector number this detector is stored as
        """
        print "Detector Number:", detnum
        print "                Digitizer Board:", self.digi_pair[0]
        print "              Digitizer Channel:", self.digi_pair[1]
        print "                     MPOD Board:", self.mpod_pair[0]
        print "                   MPOD Channel:", self.mpod_pair[1]
        print "                       X Offset:", self.pos_offset[0]
        print "                       Y Offset:", self.pos_offset[1]
        print "                       Z Offset:", self.pos_offset[2]
        print "                  Detector Type:", self.det_type
        print "  Energy Threshold for PSD Proj:", self.thresh_pair[0]
        print "  PSD Threshold for Energy Proj:", self.thresh_pair[1]

    @staticmethod
    def build_new_det(detnum):
        """Static method to make a new detector from user input

        Parameters
        ----------
        detnum : int
            The detector number this detector is stored as

        Returns
        -------
        det_setup : DetectorSetup
            A newly initialized detector setup
        """
        is_good = 'n'
        while is_good in ['n', 'N']:
            brd = int(raw_input("New Digitizer Board Number?> "))
            chan = int(raw_input("New Digitizer Channel Number?> "))
            temp = [(brd, chan)]
            brd = int(raw_input("New MPOD Board Number?> "))
            chan = int(raw_input("New MPOD Channel Number?> "))
            temp.append((brd, chan))
            xoff = float(raw_input("New X Offset?> "))
            yoff = float(raw_input("New Y Offset?> "))
            zoff = float(raw_input("New Z Offset?> "))
            temp.append((xoff, yoff, zoff))
            print "Known Detector Types are: NaI, LS, CeBr3, HeMod, HeUnmod"
            new_type = raw_input("New Detector Type?> ")
            temp.append(new_type)
            out_str = "New Energy Threshold for PSD Proj?> "
            en_thresh = float(raw_input(out_str))
            out_str = "New PSD Threshold for Energy Proj?> "
            psd_thresh = float(raw_input(out_str))
            temp.append((int(en_thresh), psd_thresh))
            det_setup = DetectorSetup((temp[0], temp[1]), temp[2], temp[3],
                                      temp[4])
            os.system('clear')
            det_setup.print_self(detnum)
            is_good = raw_input("Is this correct(Y,n)?> ")
            if is_good not in ['n', 'N']:
                return det_setup

    def get_user_value_changes(self, detnum):
        """Goes through individual settings and asks the user if things are
        correct

        Parameters
        ----------
        detnum : int
            The detector number this detector is stored as
        """
        self.print_self(detnum)
        ans = raw_input("Change Digitizer Setup(y/N)?> ")
        if ans in ['y', 'Y']:
            brd = int(raw_input("New Board Number?> "))
            chan = int(raw_input("New Channel Number?> "))
            self.digi_pair = (brd, chan)
        ans = raw_input("Change MPOD Setup(y/N)?> ")
        if ans in ['y', 'Y']:
            brd = int(raw_input("New Board Number?> "))
            chan = int(raw_input("New Channel Number?> "))
            self.mpod_pair = (brd, chan)
        ans = raw_input("Change Detector Position Offset(y/N)?> ")
        if ans in ['y', 'Y']:
            xoff = float(raw_input("New X Offset?> "))
            yoff = float(raw_input("New Y Offset?> "))
            zoff = float(raw_input("New Z Offset?> "))
            self.pos_offset = (xoff, yoff, zoff)
        ans = raw_input("Change Detector Type(y/N)?> ")
        if ans in ['y', 'Y']:
            print "Known Types are: NaI, LS, CeBr3, HeMod, HeUnmod"
            new_type = raw_input("New Detector Type?> ")
            self.det_type = new_type
        ans = raw_input("Change Projection Thresholds(y/N)?> ")
        if ans in ['y', 'Y']:
            out_str = "New Energy Threshold for PSD Proj?> "
            en_thresh = float(raw_input(out_str))
            out_str = "New PSD Threshold for Energy Proj?> "
            psd_thresh = float(raw_input(out_str))
            self.thresh_pair = (int(en_thresh), psd_thresh)


class ArraySetup(object):
    """This class contains the information for a full array of detectors setup
    for OrchidReader"""
    def __init__(self):
        """Initializes the detector id dictionary"""
        self.det_dict = {}

    def add_detector(self, det_num, det_setup):
        """Adds a detector to the detector dictionary

        Parameters
        ----------
        det_num : int
            The id number for the detector
        det_setup : DetectorSetup
            The detector setup for the detector being added to the list
        """
        self.det_dict[det_num] = det_setup

    def print_array_setup(self):
        """Prints the array setup in a pretty way"""
        temp = [(key, self.det_dict[key]) for key in self.det_dict]
        temp.sort(key=lambda x: x[0])
        print COL_HEADERS
        for idnum, val in temp:
            print DET_FORMAT_STR.format(idnum, *val.get_tuple())

    def write_array_setup(self, out_name):
        """Writes the array setup to a file in the correct format

        Parameters
        ----------
        out_name : str
            Output name of the file to be written
        """
        temp = [(key, self.det_dict[key]) for key in self.det_dict]
        temp.sort(key=lambda x: x[0])
        out_file = open(out_name, 'w')
        out_file.write(COL_HEADERS_FILE)
        for idnum, val in temp:
            out_file.write(DET_FORMAT_STR_FILE.format(idnum, *val.get_tuple()))
        out_file.close()

    def get_array_changes(self):
        """Asks the user for changes in the setup"""
        os.system('clear')
        self.print_array_setup()
        print ""
        ans = raw_input("Remove detectors from the array (y,N)?> ")
        if ans in ['y', 'Y']:
            self.get_removed_dets()
        os.system('clear')
        self.print_array_setup()
        print ""
        ans = raw_input("Add detectors to the array (y,N)?> ")
        if ans in ['y', 'Y']:
            self.get_added_dets()
        os.system('clear')
        self.print_array_setup()
        print ""
        ans = raw_input("Modify detectors in the array (y,N)?> ")
        if ans in ['y', 'Y']:
            self.get_modded_dets()

    def get_modded_dets(self):
        """Asks the user to modify existing detectors"""
        ans = 'y'
        while ans in ['y', 'Y']:
            os.system('clear')
            self.print_array_setup()
            val = int(raw_input("Detector to modify?> "))
            if val in self.det_dict:
                self.det_dict[val].get_user_value_changes(val)
            else:
                print "Detector does not exist"
            ans = raw_input("Modify Another Detector (y,N)?> ")

    def get_added_dets(self):
        """Asks the user to define new detectors"""
        ans = 'y'
        while ans in ['y', 'Y']:
            os.system('clear')
            self.print_array_setup()
            val = int(raw_input("New Detector Number?> "))
            if val in self.det_dict:
                print "Detector number already exists!"
            else:
                new_det = DetectorSetup.build_new_det(val)
                self.det_dict[val] = new_det
            ans = raw_input("Add Another Detector (y,N)?> ")

    def get_removed_dets(self):
        """Asks the user which detectors to remove"""
        ans = "y"
        while ans in ['y', 'Y']:
            os.system('clear')
            self.print_array_setup()
            val = int(raw_input("Detector Number to Remove?> "))
            if val in self.det_dict:
                del self.det_dict[val]
            else:
                print "Detector number not in array setup!"
            ans = raw_input("Remove Another Detector (y,N)?> ")


# Below are the detector setup creations, For each new type of detector I
# create a detector of the appropriate type and position and digitizer and mpod
# channels and add it, I then modify it to the correct position and electronic
# channels for another detector of the same type and add that as well.

# It should be noted that I am adding detectors using copy.deepcopy, this is
# because otherwise python will pass a reference to the object and then
# modifications to the object outside of what is stored in the ArraySetup class
# will be seen in the object stored in the class. By using deepcopy, a new
# object identical to what I passed is created and the reference to that is
# what is stored in the ArraySetup class. Since that object is not the same
# as what I am modifying, the scenario I described before will not occur

###############################################################################
# ***Default array setup
###############################################################################
# the default array setup that is present most of the time
DEFAULT_SETUP = ArraySetup()
# Create a liquid scintillator detector, add it, and then use modify add to
# add the other 5 liquid scintillator detectors
TMP = DetectorSetup(((0, 0), (1, 0)), (3.5, 70.0, 73.0), "LS", (65532, 1.0))
DEFAULT_SETUP.add_detector(0, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 1), (1, 1)), pos=(3.5, 9.0, 73.0))
DEFAULT_SETUP.add_detector(1, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 2), (1, 2)), pos=(3.5, 70.0, 60.0))
DEFAULT_SETUP.add_detector(2, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 3), (1, 3)), pos=(3.5, 9.0, 60.0))
DEFAULT_SETUP.add_detector(3, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 4), (1, 4)), pos=(3.5, 70.0, 38.0))
DEFAULT_SETUP.add_detector(4, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 5), (1, 5)), pos=(3.5, 9.0, 38.0))
DEFAULT_SETUP.add_detector(5, copy.deepcopy(TMP))
# Create a helium detector as moderated, add it, then modify it into the
# unmoderated helium detector and add that as well
TMP = DetectorSetup(((0, 6), (0, 0)), (0.0, 39.0, 75.0), "HeMod", (65532, 1.0))
DEFAULT_SETUP.add_detector(6, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 7), (0, 1)), pos=(0.0, 39.0, 50.0))
TMP.change_type("HeUnmod")
DEFAULT_SETUP.add_detector(7, copy.deepcopy(TMP))
# create a Sodium Iodide detector, add it, then modify it and add it again 7
# times to create all 8 NaI detectors
TMP = DetectorSetup(((0, 8), (0, 8)), (0.0, 68.0, 81.0), "NaI", (65532, 1.0))
DEFAULT_SETUP.add_detector(8, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 9), (0, 9)), pos=(0.0, 11.0, 81.0))
DEFAULT_SETUP.add_detector(9, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 10), (0, 10)), pos=(0.0, 68.0, 55.0))
DEFAULT_SETUP.add_detector(10, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 11), (0, 11)), pos=(0.0, 11.0, 55.0))
DEFAULT_SETUP.add_detector(11, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 12), (0, 12)), pos=(0.0, 68.0, 33.0))
DEFAULT_SETUP.add_detector(12, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 13), (0, 13)), pos=(0.0, 11.0, 33.0))
DEFAULT_SETUP.add_detector(13, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 14), (0, 14)), pos=(0.0, 68.0, 11.0))
DEFAULT_SETUP.add_detector(14, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 15), (0, 15)), pos=(0.0, 11.0, 11.0))
DEFAULT_SETUP.add_detector(15, copy.deepcopy(TMP))

###############################################################################
# ***No helium tube setup
###############################################################################
# define the no helium tube setup that existed mid september 2016 for 2 weeks
NO_HE_SETUP = ArraySetup()
# Create a liquid scintillator detector, add it, and then use modify add to
# add the other 5 liquid scintillator detectors
TMP = DetectorSetup(((0, 0), (1, 0)), (3.5, 70.0, 73.0), "LS", (65532, 1.0))
NO_HE_SETUP.add_detector(0, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 1), (1, 1)), pos=(3.5, 9.0, 73.0))
NO_HE_SETUP.add_detector(1, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 2), (1, 2)), pos=(3.5, 70.0, 60.0))
NO_HE_SETUP.add_detector(2, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 3), (1, 3)), pos=(3.5, 9.0, 60.0))
NO_HE_SETUP.add_detector(3, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 4), (1, 4)), pos=(3.5, 70.0, 38.0))
NO_HE_SETUP.add_detector(4, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 5), (1, 5)), pos=(3.5, 9.0, 38.0))
NO_HE_SETUP.add_detector(5, copy.deepcopy(TMP))
# create a Sodium Iodide detector, add it, then modify it and add it again 7
# times to create all 8 NaI detectors
TMP = DetectorSetup(((0, 8), (0, 8)), (0.0, 68.0, 81.0), "NaI", (65532, 1.0))
NO_HE_SETUP.add_detector(8, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 9), (0, 9)), pos=(0.0, 11.0, 81.0))
NO_HE_SETUP.add_detector(9, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 10), (0, 10)), pos=(0.0, 68.0, 55.0))
NO_HE_SETUP.add_detector(10, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 11), (0, 11)), pos=(0.0, 11.0, 55.0))
NO_HE_SETUP.add_detector(11, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 12), (0, 12)), pos=(0.0, 68.0, 33.0))
NO_HE_SETUP.add_detector(12, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 13), (0, 13)), pos=(0.0, 11.0, 33.0))
NO_HE_SETUP.add_detector(13, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 14), (0, 14)), pos=(0.0, 68.0, 11.0))
NO_HE_SETUP.add_detector(14, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 15), (0, 15)), pos=(0.0, 11.0, 11.0))
NO_HE_SETUP.add_detector(15, copy.deepcopy(TMP))

###############################################################################
# ***Cerium Bromide Setup
###############################################################################
# define the cerium bromide detector setup where a 2"x2" CeBr3 detector
# replaced the LS detector on digitizer channel 0 for about a week at the end
# of the september 2016 reactor cycle
CEBR_SETUP = ArraySetup()
# create the CeBr3 detector that was on the center-top of the top rail
TMP = DetectorSetup(((0, 0), (0, 2)), (0.0, 39.0, 80.0), "CeBr3", (65532, 1.0))
CEBR_SETUP.add_detector(16, copy.deepcopy(TMP))
# Create a liquid scintillator detector, add it, and then use modify add to
# add the other 4 liquid scintillator detectors
TMP = DetectorSetup(((0, 1), (1, 1)), (3.5, 9.0, 73.0), "LS", (65532, 1.0))
CEBR_SETUP.add_detector(1, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 2), (1, 2)), pos=(3.5, 70.0, 60.0))
CEBR_SETUP.add_detector(2, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 3), (1, 3)), pos=(3.5, 9.0, 60.0))
CEBR_SETUP.add_detector(3, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 4), (1, 4)), pos=(3.5, 70.0, 38.0))
CEBR_SETUP.add_detector(4, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 5), (1, 5)), pos=(3.5, 9.0, 38.0))
CEBR_SETUP.add_detector(5, copy.deepcopy(TMP))
# Create a helium detector as moderated, add it, then modify it into the
# unmoderated helium detector and add that as well
TMP = DetectorSetup(((0, 6), (0, 0)), (0.0, 39.0, 75.0), "HeMod", (65532, 1.0))
CEBR_SETUP.add_detector(6, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 7), (0, 1)), pos=(0.0, 39.0, 50.0))
TMP.change_type("HeUnmod")
CEBR_SETUP.add_detector(7, copy.deepcopy(TMP))
# create a Sodium Iodide detector, add it, then modify it and add it again 7
# times to create all 8 NaI detectors
TMP = DetectorSetup(((0, 8), (0, 8)), (0.0, 68.0, 81.0), "NaI", (65532, 1.0))
CEBR_SETUP.add_detector(8, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 9), (0, 9)), pos=(0.0, 11.0, 81.0))
CEBR_SETUP.add_detector(9, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 10), (0, 10)), pos=(0.0, 68.0, 55.0))
CEBR_SETUP.add_detector(10, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 11), (0, 11)), pos=(0.0, 11.0, 55.0))
CEBR_SETUP.add_detector(11, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 12), (0, 12)), pos=(0.0, 68.0, 33.0))
CEBR_SETUP.add_detector(12, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 13), (0, 13)), pos=(0.0, 11.0, 33.0))
CEBR_SETUP.add_detector(13, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 14), (0, 14)), pos=(0.0, 68.0, 11.0))
CEBR_SETUP.add_detector(14, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 15), (0, 15)), pos=(0.0, 11.0, 11.0))
CEBR_SETUP.add_detector(15, copy.deepcopy(TMP))
