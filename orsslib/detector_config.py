"""This file contains the definition of the detector and array setup classes"""
import os
import orsslib.input_sanitizer as inp

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
            brd = inp.get_int("New Digitizer Board Number")
            chan = inp.get_int("New Digitizer Channel Number")
            temp = [(brd, chan)]
            brd = inp.get_int("New MPOD Board Number")
            chan = inp.get_int("New MPOD Channel Number")
            temp.append((brd, chan))
            xoff = inp.get_float("New X Offset")
            yoff = inp.get_float("New Y Offset")
            zoff = inp.get_float("New Z Offset")
            temp.append((xoff, yoff, zoff))
            print "Known Detector Types are: NaI, LS, CeBr3, HeMod, HeUnmod"
            new_type = inp.get_str("New Detector Type")
            temp.append(new_type)
            out_str = "New Energy Threshold for PSD Proj"
            en_thresh = inp.get_float(out_str)
            out_str = "New PSD Threshold for Energy Proj"
            psd_thresh = inp.get_float(out_str)
            temp.append((int(en_thresh), psd_thresh))
            det_setup = DetectorSetup((temp[0], temp[1]), temp[2], temp[3],
                                      temp[4])
            os.system('clear')
            det_setup.print_self(detnum)
            if inp.get_yes_no("Is this correct", default_value=True):
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
        if inp.get_yes_no("Change Digitizer Setup", default_value=False):
            brd = inp.get_int("New Board Number")
            chan = inp.get_int("New Channel Number")
            self.digi_pair = (brd, chan)
        if inp.get_yes_no("Change MPOD Setup", default_value=False):
            brd = inp.get_int("New Board Number")
            chan = inp.get_int("New Channel Number")
            self.mpod_pair = (brd, chan)
        if inp.get_yes_no("Change Det. Position Offsets", default_value=False):
            xoff = inp.get_float("New X Offset")
            yoff = inp.get_float("New Y Offset")
            zoff = inp.get_float("New Z Offset")
            self.pos_offset = (xoff, yoff, zoff)
        if inp.get_yes_no("Change Detector Type", default_value=False):
            print "Known Types are: NaI, LS, CeBr3, HeMod, HeUnmod"
            new_type = inp.get_str("New Detector Type")
            self.det_type = new_type
        if inp.get_yes_no("Change Projection Thresholds", default_value=False):
            en_thresh = inp.get_float("New Energy Threshold for PSD Proj")
            psd_thresh = inp.get_float("New PSD Threshold for Energy Proj")
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
        if inp.get_yes_no("Remove dets from the array", default_value=False):
            self.get_removed_dets()
        os.system('clear')
        self.print_array_setup()
        print ""
        if inp.get_yes_no("Add dets to the array", default_value=False):
            self.get_added_dets()
        os.system('clear')
        self.print_array_setup()
        print ""
        if inp.get_yes_no("Modify dets in the array", default_value=False):
            self.get_modded_dets()

    def get_modded_dets(self):
        """Asks the user to modify existing detectors"""
        ans = True
        while ans:
            os.system('clear')
            self.print_array_setup()
            val = inp.get_int("Detector to modify")
            if val in self.det_dict:
                self.det_dict[val].get_user_value_changes(val)
            else:
                print "Detector does not exist"
            ans = inp.get_yes_no("Modify Another Detector",
                                 default_value=False)

    def get_added_dets(self):
        """Asks the user to define new detectors"""
        ans = True
        while ans:
            os.system('clear')
            self.print_array_setup()
            val = inp.get_int("New Detector Number")
            if val in self.det_dict:
                print "Detector number already exists!"
            else:
                new_det = DetectorSetup.build_new_det(val)
                self.det_dict[val] = new_det
            ans = inp.get_yes_no("Add Another Detector", default_value=False)

    def get_removed_dets(self):
        """Asks the user which detectors to remove"""
        ans = True
        while ans:
            os.system('clear')
            self.print_array_setup()
            val = inp.get_int("Detector Number to Remove")
            if val in self.det_dict:
                del self.det_dict[val]
            else:
                print "Detector number not in array setup!"
            ans = inp.get_yes_no("Remove Another Detector",
                                 default_value=False)
