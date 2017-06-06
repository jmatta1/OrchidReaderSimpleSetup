"""File that contains the variables defining the various sets of runs where
the array detector setup is different from default"""
import orsslib.detector_setups as ds

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

# list of the file name patterns that are contained in all the files that have
# data from the time that only the moderated 3He tube was present
MOD_HE_RUN_PATTERNS = ["Jun05_2017_0001.dat", "Jun06_2017_0000.dat"]

# list of detector setups for convenient access
EXCEPTION_DATA = [ds.DEFAULT_SETUP, ds.CEBR_SETUP, ds.NO_HE_SETUP,
                  ds.MOD_HE_SETUP]

# list of exception pattern names in the same order as setups, including def
EXCEPTION_NAME = ["Default", "CeBr3", "No_3He", "Mod_3He"]

# list of exception patterns in the same order as the det setups, minus default
EXCEPTION_PATTERN = [CEBR_RUN_PATTERNS, NO_HE_RUN_PATTERNS,MOD_HE_RUN_PATTERNS]
