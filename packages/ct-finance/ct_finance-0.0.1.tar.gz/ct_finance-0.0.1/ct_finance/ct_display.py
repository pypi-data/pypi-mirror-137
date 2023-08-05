from docopt import docopt
import ct_data.db_utility as db_utility
import ct_data.data as data
import copy
import graph
from .docopt_util.docopt_utility import elim_apostrophes, o_cond, process_clause

import display

# TODO input category desc or id for displays like budget
# TODO display category name instead of ID for budgets

usage = """

dashboards_py CLI.

Usage:
    dashboards_driver.py show               ((--b <id>) | (--d <id> [<var>]...)...)
    dashboards_driver.py create             ((--cmi (--account <acc_date> | --budget | --goal [--p <profile>]) <target> <cm_res> [--desc <cm_desc>] 
                                             (--sor <s_table> <s_col> <w_col> <w_cond> <w_id> )...) | 
                                            (--dt <g_type> <x_res> <x_res_unit> <x_source_col> 
                                             ([--mm <x_min> <x_max> ]|[ --miw <x_min> <w_size> <w_unit> ]|[ --maw <x_max> <w_size> <w_unit>])
                                             [--p <proj> <proj_res> <proj_res_unit>]) | 
                                            (--d <dash_desc> ))
    dashboards_driver.py add_display        <dashboard_id> <dt_id> (<cm_id>)...

);

Arguments:
    <b_target>                  target maximum for given budget
    <b_type>                    type of budget, current options: yearly, monthly
    <cat_id>                    cat_id indicating budgeted category
    <d_res>                     display resolution (not implemented)
    <end>                       end date of budget, enter date in format 'YYYY-MM-DD' or use 'now' to extend to present (rolling)
    <proj_type>                 projection type for budget, current options: linear 
    <start>                     start date of budget enter date in format 'YYYY-MM-DD', use 'now' to start at present or use 'first' to start at first day of present month
    <window_size>               size of desired display window, combined with w_unit to create display window
    <window_unit>               unit of display size, month or day (e.g. window is 6 months if window size = 6 and unit = month)

Options:
    --b                         budget  
    --cmi                       committed money item 
    --d                         dashboard 
    --dt                        display type
"""

args = docopt(usage)
db = db_utility.DB(db_type='display')
docopt_utility.elim_apostrophes(args=args)
# print(args)


def _prep_insert_query(insert_vals, table, remove_id=True):
    # build query for inserting, and subsequently fetching new display component entry
    in_columns = copy.deepcopy(db.schema[table])
    if remove_id:
        in_columns.pop(0)

    w_cols = []
    w_vals = []
    for i in range(0, len(in_columns)):
        if insert_vals[i]:
            w_cols.append(in_columns[i])
            w_vals.append(insert_vals[i])

    w_conds = []
    w_joins = []
    for val in w_vals:
        w_conds.append('=')
        w_joins.append('AND')

    print(w_cols)
    print(w_vals)

    query = db_utility.Query(db=db,
                             table=table,
                             in_cols=in_columns, in_vals=insert_vals,
                             w_cols=w_cols, w_vals=w_vals, w_conds=w_conds, w_joins=w_joins)

    return query


if args['create']:

    if args['--cmi']:
        cm_type = ""
        if args['--account']:
            cm_type = 'account'
        elif args['--budget']:
            cm_type = 'budget'
        elif args['--goal']:
            cm_type = 'goal'

        in_vals=[args['<target>'], args['<cm_res>'], cm_type, args['<cm_desc>'], args['<profile>'], args['<acc_date>']]
        cm_entry = _prep_insert_query(insert_vals=in_vals, table='cm_records')
        data.create_item(db=db, query=cm_entry, item_type='cm_entry', drop_cond='MIN', drop_method='inside')
        # use same query to fetch new cm_id to use in adding link items
        cm_id = db.conn.cursor().execute(cm_entry.build_select()).fetchall()[0][0]

        # create source entries
        for i in range(0, len(args['<s_table>'])):
            table = 'cm_sources'
            columns = copy.deepcopy(db.schema[table])
            columns.pop(-1)

            in_vals = [cm_id, args['<s_table>'][i], args['<w_col>'][i], args['<s_col>'][i], args['<w_cond>'][i], args['<w_id>'][i]]
            cm_source = db_utility.Query(db=db,
                                         table=table, in_cols=columns,
                                         in_vals=in_vals)
            data.create_item(db=db, query=cm_source, item_type='cm_source', drop_cond='MIN', drop_method='inside',
                             comp_columns=columns, drop_id_col='rowid')

    elif args['--dt']:
        table = 'display_types'
        in_vals = [None, args['<x_min>'], args['<x_res>'], args['<x_res_unit>'], args['<x_max>'], args['<w_size>'], args['<w_unit>'],
                   args['<x_source_col>'], args['<g_type>'],
                   args['<proj>'], args['<proj_res>'], args['<proj_res_unit>']]
        display_type = db_utility.Query(db=db, table=table,
                                        in_vals=in_vals)

        data.create_item(db=db, query=display_type, item_type='display_type', drop_cond='MIN', drop_method='inside')

    elif args['--d']:

        table = 'dashboards'
        in_cols = copy.deepcopy(db.schema[table])
        in_cols.pop(-1)

        in_vals = [None, args['<dash_desc>']]
        display_type = db_utility.Query(db=db, table=table,
                                        in_vals=in_vals, in_cols=in_cols)

        # pop off those columns we dont want to compare in eliminating duplicates like id
        in_cols.pop(0)
        data.create_item(db=db, query=display_type, item_type='dashboard', drop_cond='MIN', drop_method='inside',
                         comp_columns=in_cols)

if args['show']:
    if args['--d']:
        for id in args['<id>']:
            d_id = id
            display.display_dashboard(db=db, dash_id=d_id)
    if args['--b']:
        # single budget requested for display
        # args['<id>'] will always be list because of ellipses but in single instance it is stripped
        b_id = args['<id>'][0]
        # graph.display_dashboard(db=db, d_references=[('b_id', b_id)])

if args['add_display']:
    for cm in args['<cm_id>']:
        # TODO add utility to ensure variables are always the same - pull an existing display in dashboard and compare?
        table = 'cm_dashboards'
        in_vals = [cm, args['<dt_id>'], args['<dashboard_id>']]
        dash_display = db_utility.Query(db=db, table=table,
                                        in_vals=in_vals)

        data.create_item(db=db, query=dash_display, item_type='dashboard cm', drop_cond='MIN', drop_method='inside',
                         comp_columns=db.schema[table], drop_id_col='rowid')

db.conn.commit()