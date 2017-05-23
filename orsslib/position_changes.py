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

# list of array positions for the time series runs
EXCEPTION_DATA = [(142.0, 74.0), (234.0, 279.0), (165.0, -124.0)]

# list of names for the array positions
EXCEPTION_NAME = ["Default", "PastRxWall", "CloseToColdSrcCtrlRoom"]

# list of position exception patterns (deliberately sans the default)
EXCEPTION_PATTERN = [PAST_RX_WALL_PATTERNS, SURVEYING_PATTERNS]
