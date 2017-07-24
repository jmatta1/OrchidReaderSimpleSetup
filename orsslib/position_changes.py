"""File that contains the variables defining the various sets of runs where
the array is in positions other than default"""
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

# list of the file name patterns that match when the array was moved in order
# to facilitate scanning of the magnetic field in the area that PROSPECT will
# occupy
MAGNET_SCAN_PATTERNS = ["Mar29_2017_moved_0000", "Mar24_2017_SecPos_0000"
                        "Mar24_2017_SecPos_0001"]

# list of the file name patterns that match when the array was moved in order
# for changes to the MIF box to be done
MIF_WORK_PATTERNS = ["Jul11_2017_0000.dat", "Jul11_2017_0001.dat",
                     "Jul11_2017_0002.dat", "Jul12_2017_0000.dat",
                     "Jul13_2017_0000.dat", "Jul14_2017_0000.dat",
                     "Jul18_2017_0000.dat"]

# list of array positions for the time series runs, the last is currently
# approximate
EXCEPTION_DATA = [(142.0, 74.0), (240.0, 325.0), (165.0, -124.0),
                  (142.0, 156.0), (240.0, 325.0)]

# list of names for the array positions
EXCEPTION_NAME = ["Default", "PastRxWall", "CloseToColdSrcCtrlRoom",
                  "MovedForBFieldMeasurements", "MifBoxWork"]

# list of position exception patterns (deliberately sans the default)
EXCEPTION_PATTERN = [PAST_RX_WALL_PATTERNS, SURVEYING_PATTERNS,
                     MAGNET_SCAN_PATTERNS, MIF_WORK_PATTERNS]
