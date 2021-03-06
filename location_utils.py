import os
import csv
from os.path import join as pathjoin, splitext, basename
from array import array
from bisect import bisect_left, bisect_right


def gen_loc_file(filein: str, dir: str = None) -> str:
    """
    Generate location data file.

    Remove and print out records misplaced by timestamp.

    :param filein: Path to the data file generated from PowerSense.
    :param dir: Target directory to save location data file.
    :return: Path to the generated location data file.
    """

    filename, ext = splitext(basename(filein))
    if not dir:
        dir = os.getcwd()
    fileout = pathjoin(dir, '_'.join([filename, 'location' + ext]))
    with open(fileout, 'wt') as fout:
        writer = csv.writer(fout)
        with open(filein) as fin:
            reader = csv.reader(fin)
            header = next(reader, None)
            assert header, 'data file should have header.'
            writer.writerow((header[-2], header[-7], header[-6]))
            prev = next(reader, None)
            assert prev, 'data file should have at least one line of data.'
            prev = (prev[-2], prev[-7], prev[-6])
            for row in reader:
                r = (row[-2], row[-7], row[-6])
                if all(d for d in r):
                    if float(prev[0]) < float(r[0]):
                        writer.writerow(r)
                        prev = r
                    else:
                        # TODO: numpy.memmap for external sort if file too large
                        print(prev, '>=', r)
    return fileout


def is_chrono_sorted(loc_file: str) -> bool:
    def file_read_gen(loc_file):
        with open(loc_file) as fin:
            reader = csv.reader(fin)
            next(reader)  # skip header
            prev_t = float('-inf')
            for row in reader:
                t = float(row[0])
                yield prev_t <= t
                prev_t = t

    return all(file_read_gen(loc_file))


def get_loc_by_time_range(loc_file: str, start=float('-inf'), end=float('inf')) -> list:

    assert is_chrono_sorted(loc_file), 'loc_file should be sorted by timestamp.'

    if start > end:
        return []

    # TODO: numpy.memmap if file too large

    t = array('d')
    with open(loc_file) as fin:
        reader = csv.reader(fin)
        next(reader)  # skip header
        for row in reader:
            t.append(float(row[0]))

    l = bisect_left(t, start)
    r = bisect_right(t, end)
    print(l, r)

    fin = open(loc_file)
    reader = csv.reader(fin)
    fin.seek(l+1)
    return [next(reader) for _ in range(r-l+1)]
