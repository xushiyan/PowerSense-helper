from location_utils import *


if __name__ == '__main__':
    try:
        datafile = sys.argv[1]
    except IndexError:
        datafile = pathjoin(dirname(abspath(__file__)), 'commonwealth.csv')
    loc_file = gen_loc_file(datafile)
    print('generated location data file at\n', loc_file)
    print('loc_file is sorted chronologically: ', is_chrono_sorted(loc_file))
    print(get_loc_by_time_range(loc_file, 1501240257, 1501240276))