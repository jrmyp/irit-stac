# Author: Eric Kow
# License: CeCILL-B (French BSD3-like)

"""
Dump the text in documents with segment annotations
"""

import copy

import educe.stac

from stac.edu import sorted_first_widest
from stac.util.annotate import annotate
from stac.util.args import add_usual_input_args, read_corpus
from stac.util.glozz import is_dialogue

NAME = 'text'


def config_argparser(parser):
    """
    Flags for the text subcommand.
    You should create and pass in the subparser to which the flags
    are to be added.
    """
    add_usual_input_args(parser)
    parser.add_argument('--edges', action='store_true',
                        help='First/last dialogues only')
    parser.set_defaults(func=main)


def main(args):
    """
    Subcommand main.

    You shouldn't need to call this yourself
    if you're using `config_argparser`
    """
    corpus = read_corpus(args, verbose=True)
    for k in sorted(corpus, key=educe.stac.id_to_path):
        doc = corpus[k]

        def anno(span=None):
            """
            Return pretty string for annotations within a given span
            """
            if span:
                units_ = [u for u in doc.units if span.encloses(u.span)]
                units = copy.deepcopy(units_)
                for unit in units:
                    unit.span = unit.span.relative(span)
            else:
                units = doc.units
            return annotate(doc.text(span), units).strip()
        print "========== %s ============" % k
        print
        if args.edges:
            dialogues = sorted_first_widest(filter(is_dialogue, doc.units))
            if dialogues:
                d_first = dialogues[0]
                print anno(d_first.text_span())
                if len(dialogues) > 1:
                    d_last = dialogues[-1]
                    print "...\n"
                    print anno(d_last.text_span()).encode('utf-8')
        else:
            print anno().encode('utf-8')
        print