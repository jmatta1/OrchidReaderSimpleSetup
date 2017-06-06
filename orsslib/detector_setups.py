"""This file contains the definition of all the detector configurations the
array has supported"""
import copy
from orsslib.detector_config import ArraySetup, DetectorSetup
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
# Create a helium detector as unmoderated, add it, then modify it into the
# moderated helium detector and add that as well
TMP = DetectorSetup(((0, 6), (0, 1)), (0.0, 39.0, 75.0), "HeUnmod", (65532, 1.0))
DEFAULT_SETUP.add_detector(6, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 7), (0, 0)), pos=(0.0, 39.0, 50.0))
TMP.change_type("HeMod")
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
# Create a helium detector as unmoderated, add it, then modify it into the
# moderated helium detector and add that as well
TMP = DetectorSetup(((0, 6), (0, 1)), (0.0, 39.0, 75.0), "HeUnmod", (65532, 1.0))
DEFAULT_SETUP.add_detector(6, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 7), (0, 0)), pos=(0.0, 39.0, 50.0))
TMP.change_type("HeMod")
DEFAULT_SETUP.add_detector(7, copy.deepcopy(TMP))
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

###############################################################################
# ***Single, moderated helium tube setup
###############################################################################
# define the 1 mod helium tube setup that existed early June 2017 for a week
MOD_HE_SETUP = ArraySetup()
# Create a liquid scintillator detector, add it, and then use modify add to
# add the other 5 liquid scintillator detectors
TMP = DetectorSetup(((0, 0), (1, 0)), (3.5, 70.0, 73.0), "LS", (65532, 1.0))
MOD_HE_SETUP.add_detector(0, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 1), (1, 1)), pos=(3.5, 9.0, 73.0))
MOD_HE_SETUP.add_detector(1, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 2), (1, 2)), pos=(3.5, 70.0, 60.0))
MOD_HE_SETUP.add_detector(2, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 3), (1, 3)), pos=(3.5, 9.0, 60.0))
MOD_HE_SETUP.add_detector(3, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 4), (1, 4)), pos=(3.5, 70.0, 38.0))
MOD_HE_SETUP.add_detector(4, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 5), (1, 5)), pos=(3.5, 9.0, 38.0))
MOD_HE_SETUP.add_detector(5, copy.deepcopy(TMP))
# Create a helium detector as unmoderated and add it
TMP = DetectorSetup(((0, 7), (0, 0)), (0.0, 39.0, 50.0), "HeMod", (65532, 1.0))
CEBR_SETUP.add_detector(7, copy.deepcopy(TMP))
# create a Sodium Iodide detector, add it, then modify it and add it again 7
# times to create all 8 NaI detectors
TMP = DetectorSetup(((0, 8), (0, 8)), (0.0, 68.0, 81.0), "NaI", (65532, 1.0))
MOD_HE_SETUP.add_detector(8, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 9), (0, 9)), pos=(0.0, 11.0, 81.0))
MOD_HE_SETUP.add_detector(9, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 10), (0, 10)), pos=(0.0, 68.0, 55.0))
MOD_HE_SETUP.add_detector(10, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 11), (0, 11)), pos=(0.0, 11.0, 55.0))
MOD_HE_SETUP.add_detector(11, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 12), (0, 12)), pos=(0.0, 68.0, 33.0))
MOD_HE_SETUP.add_detector(12, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 13), (0, 13)), pos=(0.0, 11.0, 33.0))
MOD_HE_SETUP.add_detector(13, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 14), (0, 14)), pos=(0.0, 68.0, 11.0))
MOD_HE_SETUP.add_detector(14, copy.deepcopy(TMP))
TMP.change_params(connect=((0, 15), (0, 15)), pos=(0.0, 11.0, 11.0))
MOD_HE_SETUP.add_detector(15, copy.deepcopy(TMP))
