from docopt import docopt
import copy
import pathlib
import json
import os

# internal
from data.data import dbUpdate, ctCreate
from docopt_util.docopt_utility import elim_apostrophes, o_cond, process_clause
from data.classify import BankClassify
from sql_queries import DB, Query
from db_structure.data_db import FINANCE_TABLES
from db_structure.display_db import DISPLAY_TABLES

# sys.tracebacklimit = 0
# TODO revise usage to make actual sense

usage = """

finance_py CLI.

Usage:
    ct_io.py add_source_fp      <filepath>
    ct_io.py create             ((--a <number> (--TD | --QT | --crypto) (--f | --api) [<description> <adjust>]) | 
                                ( --t <tag_desc> )... | 
                                ( --c <cat_desc> )... |
                                ( --crh <holding_desc> <symbol> [( <parent_chain> <chain_addy> )]))                 
    ct_io.py view <table>       [(--s_col <s_cols>)...
                                (--w <w_cols> <w_conds> <w_vals> [(--j <w_joins>)])...
                                (--or <o_col> (--asc | --desc))
                                (--l <limit>)]                             
    ct_io.py update             (--a (<account> | --all ))
    ct_io.py edit <table>       [(--u <up_cols> <up_vals>)... 
                                (--w <w_cols> <w_conds> <w_vals> [(--j <w_joins>)])...
                                (--t <tag_desc>...)]
    ct_io.py split              (--w <w_cols> <w_conds> <w_vals> [(--j <w_joins>)])...
                                [[ (--p <percent>)  | (--n <new_value>) ] (--u <up_cols> <up_vals>...)]                               
    ct_io.py tag <table>        (--w <w_cols> <w_conds> <w_vals> [(--j <w_joins>)])...
                                (--t <tag_desc>...)                                  
    ct_io.py delete <table>     [(--w <w_cols> <w_conds> <w_vals> [(--j <w_joins>)])...]
    ct_io.py process
    ct_io.py                    [--help]

Arguments:
    <account>               distinct account number or description
    <adjust>                starting value or adjustment if account data incomplete
    <cat_desc>              new category description
    <chain_addy>            chain/contract address for new crypto holding
    <description>           descriptive identifier or reference for new account
    <holding_desc>          new crypto holding description
    <parent_chain>          name of parent chain for new crypto holding e.g. ethereum for chainlink token
    <number>                new account number, wallet address if crypto
    <s_cols>                columns to be filtered in query/selection
    <symbol>                new crypto holding symbol, must match Yahoo ticker for accurate price information
    <tag_desc>              new tag description
    <w_joins>               keyword string to join where clause to the previous where clause, 'AND' or 'OR'
    <limit>

Options:
    --a                     create a new account  
    --all                   update all accounts
    --api                   new account will use api for updates
    --c                     new category
    --crh                   new crypto holding in blockchain wallet
    --crypto                new blockchain wallet
    --f                     new account will create folder and use files to update  
    --QT                    new Questrade account 
    --s_col                 add selected/filtered columns to query selection
    --t                     new tag
    --TD                    new TD account
    --u                     update accounts            
"""

args = docopt(usage)

elim_apostrophes(args=args)
# print(args)

# add filepath for db storage if desired
JSON_SOURCE_FILE = 'db_source.json'
SOURCE_FP = pathlib.Path(__file__).absolute().parent


def add_source_filepath(filepath):
    # path = pathlib.Path(filepath).__str__
    with open(os.path.join(SOURCE_FP, JSON_SOURCE_FILE), 'w') as db_file:
        full_fp = pathlib.Path(SOURCE_FP).joinpath(JSON_SOURCE_FILE)
        # if user updates delete original file
        if os.path.exists(full_fp):
            os.remove(full_fp)
        db_file.write(json.dumps(filepath))


def get_source_fp():
    try:
        with open(os.path.join(SOURCE_FP, JSON_SOURCE_FILE), 'r') as db_file:
            path = pathlib.Path(json.load(db_file))
    except:
        path = None

    return path

# initialize objects to pass to various function calls
# prepare and pass structure to db for initialization
def init_db():
    structure = list()
    for table in FINANCE_TABLES:
        structure.append(table)
    for table in DISPLAY_TABLES:
        structure.append(table)

    source_path = get_source_fp()
    if source_path:
        db = DB(structure=structure, filepath=source_path)
    else:
        db = DB(structure=structure)

    return db


def standard_query():
    query = Query(db=db, table=args['<table>'],
                  s_cols=args['<s_cols>'],
                  in_vals=None, in_cols=None,
                  up_vals=args['<up_vals>'], up_cols=args['<up_cols>'],
                  w_cols=args['<w_cols>'], w_conds=process_clause(args), w_vals=args['<w_vals>'], w_joins=args['<w_joins>'],
                  o_col=args['<o_col>'], o_cond=o_cond(args),
                  limit=args['<limit>'])
    return query


if args['delete']:
    db = init_db()
    query = standard_query()
    db.conn.cursor().execute(query.build_delete())
    db.conn.commit()

if args['process']:
    db = init_db()
    BankClassify(db=db).ask_with_guess()

if args['add_source_fp']:
    add_source_filepath(args['<filepath>'])

if args['edit']:
    db = init_db()
    query = standard_query()

    # add tags to in_vals and rebuild strings
    if args['<tag_desc>']:
        for tag in args['<tag_desc>']:
            update = dbUpdate(db=db)
            update.tag_entry(tagged_query=query, tag_param=tag)

    update = dbUpdate(db=db)
    update.db.update_entry(query=query)
    # data.edit(db=db, query=query)

if args['split']:
    db = init_db()
    query = standard_query()

    query.table = 'transactions'
    update = dbUpdate(db=db)
    update.split_transaction(query=query, percentage=args['<percent>'], amount=args['<new_value>'])

if args['create']:
    db = init_db()
    query = standard_query()

    if args['--a']:
        # convert source option into string
        source = ""
        if args['--f']:
            source = 'file'
        elif args['--api']:
            source = 'api'

        # convert institution into string
        institution = ""
        if args['--TD']:
            institution = 'TD'
        elif args['--QT']:
            institution = 'QT'
        elif args['--crypto']:
            institution = 'crypto'

        query.table = 'accounts'

        query.in_vals = [None, args['<number>'], institution, args['<description>'], None, source, args['<adjust>']]
        query.build_str()

        comp_columns = copy.deepcopy(query.in_cols)
        comp_columns.pop(0)
        comp_columns.pop(-1)

        create = ctCreate(query=query, db=db, drop_cond='MIN', drop_method='inside', comp_columns=comp_columns)
        create.create_item(item_type='account')

    if args['--t']:
        db = init_db()
        query = standard_query()

        for tag in args['<tag_desc>']:
            query.table = 'tags'
            in_vals = [None, tag]
            query.in_vals = in_vals
            query.build_str()

            create = ctCreate(query=query, db=db)
            create.create_item(item_type='tag')

    if args['--c']:
        db = init_db()
        query = standard_query()

        for category in args['<cat_desc>']:
            query.table = 'categories'
            in_vals = [None, category]
            query.in_vals = in_vals
            query.build_str()

            create = ctCreate(query=query, db=db)
            create.create_item(item_type='category')

    if args['--crh']:
        db = init_db()
        query = standard_query()

        query.table = 'crypto_holdings'
        in_vals = [None, args['<holding_desc>'], args['<symbol>'], args['<parent_chain>'], args['<chain_addy>']]
        query.in_vals = in_vals
        query.build_str()

        create = ctCreate(query=query, db=db)
        create.create_item(item_type='crypto_holding')

if args['tag']:
    db = init_db()
    query = standard_query()

    for tag in args['<tag_desc>']:
        # data.tag_entry(db=db, tagged_query=query, tag_param=tag)

        update = dbUpdate(db=db)
        update.tag_entry(tagged_query=query, tag_param=tag)

if args['view']:
    db = init_db()
    query = standard_query()

    if args['<table>'] in db.schema.keys():
        view = db.get_view(query=query)
        print(view)
        # data.view(db=db, query=query)
    else:
        print("Table does not exist")

if args['--help']:
    print(usage)

if args['update']:
    db = init_db()

    if args['--a']:
        if args['<account>']:
            update = dbUpdate(db=db)
            update.update_account(account=args['<account>'])

        elif args['--all']:
            accounts = db.conn.cursor().execute("SELECT num FROM accounts").fetchall()

            for account in accounts:
                update = dbUpdate(db=db)
                update.update_account(account=account[0])
