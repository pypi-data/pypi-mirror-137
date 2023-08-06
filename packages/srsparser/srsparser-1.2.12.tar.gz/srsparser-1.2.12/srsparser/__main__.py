import argparse as ap
from os.path import basename, splitext
import logging
import logging.config

from pymongo import MongoClient
from prettytable import PrettyTable

from srsparser import SRSParser
from srsparser.nlp import NLProcessor
from srsparser import configs


def init_logger() -> logging.Logger:
    logging.config.dictConfig(configs.LOGGING_CONFIG)
    logger = logging.getLogger('my_logger')
    return logger


def init_args_parser() -> ap.ArgumentParser:
    parser = ap.ArgumentParser(
        description='A command-line application written in Python that parses unstructured text documents '
                    '(files with .docx extension) with SRS in accordance with GOST standard 34.602-89 and '
                    'saves the structured results to the MongoDB database'
    )

    parser.add_argument(
        'mode',
        type=str,
        help='"parse" — analyzes the input documents and saves the parsing '
             'results (as structures) to MongoDB database; '
             '"keywords" — searches for keywords in the content of the document structure, '
             'which is stored in the resulting MongoDB collection',
    )

    parser.add_argument(
        'mongodb_url',
        type=str,
        help='MongoDB connection string (with the name of the database)'
    )

    parser.add_argument(
        'results_coll',
        type=str,
        help='name of MongoDB collection with parsing results '
             '(contains software requirements specifications structures '
             'filled according to the templates of the SRS structures)'
    )

    parser.add_argument(
        '-tc',
        '--tmpl-coll',
        dest='tmpl_coll',
        type=str,
        help='name of MongoDB collection with templates of software requirements specifications structures'
    )

    parser.add_argument(
        '-t',
        '--tmpl',
        dest='tmpl',
        type=str,
        help='template name of software requirements specification structure '
             'according to which the parsing is performed'
    )

    parser.add_argument(
        '-dp',
        '--docx-path',
        dest='docx_path',
        type=str,
        help='path to .docx file containing software requirements specification'
    )

    parser.add_argument(
        '-dn',
        '--docx-name',
        dest='docx_name',
        type=str,
        help='the name of document that is stored in the resulting collection as structure'
    )

    parser.add_argument(
        '-r',
        '--results',
        dest='results',
        action='store_true',
        help='show a list of document names that are stored in the resulting collection as structures'
    )

    return parser


def main():
    parser = init_args_parser()
    args = parser.parse_args()
    logger = init_logger()

    client = MongoClient(args.mongodb_url)
    db = client.get_default_database()
    logger.info('the connection to the database ("%s") is established', db.name)

    results_coll = db[args.results_coll]
    logger.info('the connection to the results collection ("%s") is established', results_coll.name)

    if args.results:
        logger.info('documents in results collection ("%s"):', args.results_coll)
        logger.info('%s', [structure['document_name'] for structure in results_coll.find({})])

    mode = args.mode.lower()
    logger.info('operating mode: %s', mode)

    if mode == 'parse':
        tmpl_coll = db[args.tmpl_coll]
        logger.info('the connection to the templates collection ("%s") is established', tmpl_coll.name)

        structure_template = tmpl_coll.find_one({'name': args.tmpl})['structure']
        logger.info('a structure template was obtained from the collection with the results: %s', structure_template)

        parser = SRSParser(structure_template)
        document_structure = parser.parse_docx(args.docx_path)
        logger.info('based on the content of the document ("%s"), a section structure was created: %s', args.docx_path,
                    document_structure)

        document_name = splitext(basename(args.docx_path))[0]

        results_coll.insert_one({'document_name': document_name, 'structure': document_structure})
        logger.info('successful! the created section structure is loaded into the results collection ("%s")',
                    results_coll.name)
    elif mode == 'keywords':
        results = list(results_coll.find({}))

        docx_structure_idx = -1
        for idx in range(len(results)):
            if results[idx]['document_name'] == args.docx_name:
                docx_structure_idx = idx
                logger.info('the document "%s" was found in the results collection under the sequence number %s!',
                            args.docx_name, docx_structure_idx + 1)
                break
        if docx_structure_idx < 0:
            logger.error('there is no such document in the results collection with document name "%s"', args.docx_name)
            return

        logger.info('initializing SDK pullenti...')
        nlp = NLProcessor(init_pullenti=True)
        logger.info('OK!')

        tf_idf_keywords = nlp.get_keywords_tf_idf(
            structures=[result['structure'] for result in results],
            structure_idx=docx_structure_idx
        )
        logger.info('keywords are obtained using the TF-IDF model')

        pullenti_keywords = nlp.get_keywords_pullenti(
            structure=results[docx_structure_idx]['structure']
        )
        logger.info('keywords are obtained using the pullenti package')

        keywords_table = PrettyTable()
        keywords_table.add_column('TD-IDF', tf_idf_keywords[:10])
        keywords_table.add_column('Pullenti', pullenti_keywords[:10])

        logger.info('below are the top 10 keywords:\n%s', keywords_table)
    else:
        logger.error('the mode "%s" does not exist!', mode)

    client.close()


if __name__ == '__main__':
    main()
