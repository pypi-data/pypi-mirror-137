import argparse as ap
from os.path import basename, splitext

from pymongo import MongoClient

from srsparser import SRSParser
from srsparser import configs


def init_args_parser() -> ap.ArgumentParser:
    parser = ap.ArgumentParser(
        description='A package for analyzing and uploading text documents '
                    'with software requirements specifications to NoSQL database MongoDB'
    )

    parser.add_argument(
        'docx_path',
        type=str,
        help='path to .docx file containing software requirements specification'
    )

    parser.add_argument(
        'template_name',
        type=str,
        help='template of software requirements specification structure according to which the parsing is performed'
    )

    return parser


def main():
    parser = init_args_parser()
    args = parser.parse_args()

    client = MongoClient(configs.MONGODB_URL)
    db = client[configs.DB_NAME]

    tmpl_coll = db[configs.TMPL_COLL_NAME]
    tree_template = tmpl_coll.find_one({'name': args.template_name})['structure']

    parser = SRSParser(tree_template)
    document_structure = parser.parse_docx(args.docx_path)

    document_name = splitext(basename(args.docx_path))[0]

    results_coll = db[configs.RESULTS_COLL_NAME]
    results_coll.insert_one({'document_name': document_name, 'structure': document_structure})

    client.close()


if __name__ == '__main__':
    main()
