import argparse as ap
from os.path import basename, splitext

from pymongo import MongoClient
from prettytable import PrettyTable

from srsparser import SRSParser
from srsparser.nlp import get_keywords_pullenti, get_keywords_tf_idf


def init_args_parser() -> ap.ArgumentParser:
    parser = ap.ArgumentParser(
        description='A command-line application written in Python that parses unstructured text documents '
                    '(files with .docx extension) with SRS in accordance with GOST standard 34.602-89 and '
                    'saves the structured results to the MongoDB database.'
    )

    parser.add_argument(
        'mode',
        type=str,
        help='"parse" — analyzes the input documents and saves the parsing '
             'results (as structures) to MongoDB database; '
             '"keywords" — searches for keywords in the content of the document structure, '
             'which is stored in the resulting MongoDB collection.',
    )

    parser.add_argument(
        'mongodb_url',
        type=str,
        help='MongoDB connection string (with the name of the database).'
    )

    parser.add_argument(
        'results_coll',
        type=str,
        help='name of MongoDB collection with parsing results '
             '(contains software requirements specifications structures '
             'filled according to the templates of the SRS structures).'
    )

    parser.add_argument(
        '-tc',
        '--tmpl-coll',
        dest='tmpl_coll',
        type=str,
        help='name of MongoDB collection with templates of software requirements specifications structures.'
    )

    parser.add_argument(
        '-t',
        '--tmpl',
        dest='tmpl',
        type=str,
        help='template name of software requirements specification structure '
             'according to which the parsing is performed.'
    )

    parser.add_argument(
        '-dp',
        '--docx-path',
        dest='docx_path',
        type=str,
        help='path to .docx file containing software requirements specification.'
    )

    parser.add_argument(
        '-dn',
        '--docx-name',
        dest='docx_name',
        type=str,
        help='the name of document that is stored in the resulting collection as structure.'
    )

    parser.add_argument(
        '-r',
        '--results',
        dest='results',
        action='store_true',
        help='show a list of document names that are stored in the resulting collection as structures.'
    )

    return parser


def main():
    parser = init_args_parser()
    args = parser.parse_args()

    client = MongoClient(args.mongodb_url)
    db = client.get_default_database()

    results_coll = db[args.results_coll]
    if args.results:
        print(f'Document names in MongoDB results collection ({args.results_coll}):')
        docx_structures = results_coll.find({})
        for structure in docx_structures:
            print(structure['document_name'])

    mode = args.mode.lower()
    if mode == 'parse':
        tmpl_coll = db[args.tmpl_coll]
        tree_template = tmpl_coll.find_one({'name': args.tmpl})['structure']

        parser = SRSParser(tree_template)
        document_structure = parser.parse_docx(args.docx_path)

        document_name = splitext(basename(args.docx_path))[0]

        results_coll.insert_one({'document_name': document_name, 'structure': document_structure})
        print('OK')
    elif mode == 'keywords':
        docx_structures = list(results_coll.find({}))

        docx_structure_idx = -1
        for idx in range(len(docx_structures)):
            if docx_structures[idx]['document_name'] == args.docx_name:
                docx_structure_idx = idx
                break
        if docx_structure_idx < 0:
            print('there is no such document in the database: ', args.docx_name)
            return

        tf_idf_keywords = get_keywords_tf_idf(docx_structures, docx_structure_idx)

        docx_structure = docx_structures[docx_structure_idx]['structure']
        pullenti_keywords = get_keywords_pullenti(docx_structure)

        mytable = PrettyTable()
        mytable.add_column('TD-IDF', tf_idf_keywords[:10])
        mytable.add_column('Pullenti', pullenti_keywords[:10])

        print(mytable)
    else:
        print('the mode does not exist')

    client.close()


if __name__ == '__main__':
    main()
