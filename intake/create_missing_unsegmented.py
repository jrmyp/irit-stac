"""Re-create an unsegmented csv file given an existing segmented file.

This script re-creates a file "unsegmented/[file_name].soclog.csv" from
an existing "segmented/[file_name].soclog.seg.csv" file.
This enables to regenerate missing unsegmented files that are required
by the weaving scripts.
"""

from __future__ import print_function

import argparse
import csv
from glob import glob
import os

from csvtoglozz import utf8_csv_reader


def create_unsegmented_file(dir_corpus, doc, seg_path=''):
    """remove empty lines and ampersands and write contents to unsegmented/

    Parameters
    ----------
    dir_corpus : string
        Folder of the corpus
    doc : string
        Name of the document/game
    seg_path : string, optional
        Path to the segmented file we should use ; This is necessary when
        there are more than one file under segmented/.
    """
    dir_corpus = os.path.abspath(dir_corpus)
    game_dir = os.path.join(dir_corpus, doc)
    if not os.path.isdir(game_dir):
        err_msg = 'Unable to find corpus files {}'.format(game_dir)
        raise ValueError(err_msg)

    # segmented: in ./segmented
    seg_dir = os.path.join(game_dir, 'segmented')
    if seg_path:
        seg_file = os.path.abspath(seg_path)
        if not os.path.isfile(seg_file):
            raise ValueError('Unable to locate segmented file {}'.format(
                seg_path))
    else:
        seg_file = glob(os.path.join(seg_dir,
                                     doc + '*.soclog.seg.csv'))
        if len(seg_file) != 1:
            err_msg = 'Unable to locate segmented file {}'.format(seg_file)
            raise ValueError(err_msg)
        seg_file = seg_file[0]
    # paranoid check
    if not os.path.isfile(seg_file):
        err_msg = 'Weird error on locating segmented file {}'.format(
            seg_file)
        raise ValueError(err_msg)

    useg_dir = os.path.join(game_dir, 'unsegmented')
    if not os.path.isdir(useg_dir):
        os.mkdir(useg_dir)

    useg_file = os.path.join(useg_dir, doc + '.soclog.csv')

    with open(seg_file, 'rb') as incsvfile:  # bytestring
        csvreader = utf8_csv_reader(incsvfile, delimiter='\t')
        with open(useg_file, 'wb') as outcsvfile:
            outcsv = csv.writer(outcsvfile, dialect='excel', delimiter='\t',
                                lineterminator='\n')
            for row in csvreader:
                if ''.join(row).strip():
                    outcsv.writerow([cell.replace('&', '') for cell in row])


def main():
    """Main"""
    # parse command line
    parser = argparse.ArgumentParser(
        description='Re-create an unsegmented csv file from segmented')
    parser.add_argument('dir_corpus', metavar='DIR',
                        help='folder of the corpus')
    parser.add_argument('doc', metavar='DOC',
                        help='document')
    # explicitly point to segmented (in case there is more than one in
    # the segmented/ folder)
    parser.add_argument('--segmented', metavar='FILE',
                        help='segmented file to use (if >1 in segmented/)')
    args = parser.parse_args()
    # do the job
    create_unsegmented_file(args.dir_corpus, args.doc, seg_path=args.segmented)


if __name__ == '__main__':
    main()
