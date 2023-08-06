from __future__ import print_function

import os.path
import sys

import sqlparse
from ddlparse import DdlParse

from snowfinch.constants import *
from snowfinch.logger import log
from snowfinch.utils import *

logger = log.get_logger()


def parse_lines(in_filename, out_filename, start_kw, end_kw, skip_kw):
    try:
        inp = open(in_filename, 'r', encoding='utf-8', errors='ignore')
        out = open(out_filename, 'w+', encoding='utf-8', errors='ignore')
    except FileNotFoundError as err:
        print(f"File {in_filename} not found", err)
        raise
    except OSError as err:
        print(f"OS error occurred trying to open {in_filename}", err)
        raise
    except Exception as err:
        print(f"Unexpected error opening {in_filename} is",  repr(err))
        raise
    else:
        with inp, out:
            copy = False
            for line in inp:
                if not any(w in line.strip().lower() for w in skip_kw):
                    # first IF block to handle if the start and end on same line
                    if line.lstrip().lower().startswith(start_kw) and line.rstrip().endswith(end_kw):
                        copy = True
                        if copy:  # keep the starts with keyword
                            out.write(line)
                        copy = False
                        continue
                    elif line.lstrip().lower().startswith(start_kw):
                        copy = True
                        if copy:  # keep the starts with keyword
                            out.write(line)
                        continue
                    elif line.rstrip().endswith(end_kw):
                        if copy:  # keep the ends with keyword
                            out.write(line)
                        copy = False
                        continue
                    elif copy:
                        # write
                        out.write(line)


def get_volatile_table_list(filename):
    vt_list = []
    vt_kw = ["create"]
    # bad_keys = ['create', 'volatile', 'table', 'multiset', 'set', 'no fallback', ',']
    # re_bad_keys = re.compile(r"\b(" + "|".join(bad_keys) + ")\\W", re.I)
    # print(re_bad_keys)
    with open(filename, 'r', encoding='utf-8', errors='ignore') as inpt:
        for line in inpt:
            if any(line.lower().lstrip().startswith(kw) for kw in vt_kw):
                split_words = line.strip().upper().split()
                line = split_words[split_words.index('TABLE') + 1]
                vt_list.append(line.strip())
    return list(set(vt_list))


def get_source_table_list(filename):
    table_list = []
    stmt_kw = ["merge", "insert", "update", "delete"]

    with open(filename, 'r', encoding='utf-8', errors='ignore') as inpt:
        for line in inpt:
            if any(line.lower().lstrip().startswith(kw) for kw in stmt_kw):
                if line.lower().lstrip().startswith("update"):
                    split_words = line.strip().upper().split()
                    update_table = split_words[split_words.index('UPDATE') + 1]\
                        .replace("(", "")\
                        .replace(";", "")
                    table_list.append(update_table.strip().upper())
                elif line.lower().lstrip().startswith("delete from"):
                    split_words = line.strip().upper().split()
                    del_from = split_words[split_words.index('FROM') + 1]\
                        .replace("(", "")\
                        .replace(";", "")
                    table_list.append(del_from.strip().upper())
                elif line.lower().lstrip().startswith("insert"):
                    split_words = line.strip().upper().split()
                    print(split_words)
                    insert_into = split_words[split_words.index('INTO') + 1]\
                        .replace("(", "")\
                        .replace(";", "")
                    table_list.append(insert_into.strip().upper())
                elif line.lower().lstrip().startswith("merge into"):
                    split_words = line.strip().upper().split()
                    merge_into = split_words[split_words.index('INTO') + 1]\
                        .replace("(", "")\
                        .replace(";", "")
                    table_list.append(merge_into.strip().upper())
    remove_table_list = ['$', 'LL', 'LLK']
    table_list = [sa for sa in table_list if not any(sb in sa for sb in remove_table_list)]
    return list(set(table_list))


def get_table_name(line=None, stmt=None, schma=None):
    table_name = None
    full_table_name = None
    if line.lower().lstrip().startswith(stmt):
        split_words = line.strip().upper().split()

        # get table name
        if stmt.lower() in ('drop', 'create'):
            table_name = split_words[split_words.index('TABLE') + 1]\
                .replace("(", "")\
                .replace(";", "")

        if stmt.lower() == 'update':
            split_words = line.strip().upper().split()
            table_name = split_words[split_words.index('UPDATE') + 1] \
                .replace("(", "") \
                .replace(";", "")

        elif stmt.lower() == 'delete':
            split_words = line.strip().upper().split()
            table_name = split_words[split_words.index('FROM') + 1] \
                .replace("(", "") \
                .replace(";", "")

        elif stmt.lower() in ('merge', 'insert'):
            split_words = line.strip().upper().split()
            print(split_words)
            table_name = split_words[split_words.index('INTO') + 1] \
                .replace("(", "") \
                .replace(";", "")

        # assign schema
        if table_name.startswith(tuple(STG_SCHEMA_PRFX_LIST)):
            schema = f"{schma}_STG"
        elif table_name.endswith(tuple(QA_SCHEMA_PRFX_LIST)):
            schema = f"{schma}_QADATA"
        else:
            schema = schma

        # get the full table b=name
        full_table_name = f"{schema}.{table_name}"
    return [table_name, full_table_name]


def parse_sql(_input, _output, sfdb, sfschema):
    try:
        inp = open(_input, 'r', encoding='utf-8', errors='ignore')
        out = open(_output, 'w+', encoding='utf-8', errors='ignore')
    except FileNotFoundError as err:
        print(f"File {_input} not found", err)
        raise
    except OSError as err:
        print(f"OS error occurred trying to open {input}", err)
        raise
    except Exception as err:
        print(f"Unexpected error opening {input} is", repr(err))
        raise
    else:
        with inp, out:
            statements = sqlparse.split(inp.read())
            for statement in statements:
                statement = sqlparse.format(statement, strip_comments=True)
                if statement.lower().startswith('database'):
                    statement = f"USE DATABASE {sfdb};\n"

                if statement.lstrip().lower().startswith("delete from") \
                        and statement.lower().rstrip().endswith("all;"):
                    statement = statement.upper().replace("ALL", "")

                if 'sel ' in statement.lstrip().lower():
                    if statement.lstrip().lower().startswith('sel cast(count(*)'):
                        statement = "--" + statement.strip()
                    else:
                        statement = statement.lstrip().upper().replace("SEL", "SELECT")

                if 'del ' in statement.strip().lower():
                    statement = statement.lstrip().upper().replace("DEL", "DELETE")

                if statement.lstrip().lower().startswith('drop'):
                    drop_table_name = get_table_name(statement, 'drop', sfschema)
                    statement = f"\nDROP TABLE {drop_table_name[1]};\n"

                if statement.lstrip().lower().startswith('insert '):
                    insert_table_name = get_table_name(statement, 'insert', sfschema)
                    statement = statement.replace(insert_table_name[0], insert_table_name[1])

                if statement.lstrip().lower().startswith('update'):
                    update_table_name = get_table_name(statement, 'update', sfschema)
                    statement = statement.replace(update_table_name[0], update_table_name[1])

                if statement.lower().startswith('create'):
                    create_table_name = get_table_name(statement, 'create', sfschema)

                    # get DDL
                    line = sqlparse.format(statement, strip_comments=True)
                    parser = DdlParse()
                    parser.ddl = line.upper()

                    #  remove the teradata junk on create
                    parsed_ddl = parser.ddl.split("(", 1)[1:]
                    parsed_ddl1 = {
                        x.replace('CHARACTER SET LATIN NOT CASESPECIFIC', '')
                        .replace("FORMAT 'YYYY-MM-DD'", '')
                        for x in parsed_ddl
                    }
                    parsed_ddl_str = " ".join(str(x) for x in parsed_ddl1)
                    statement = f"\nCREATE TEMPORARY TABLE {create_table_name[1]} \n(" + parsed_ddl_str

                    if 'unique primary' in statement.strip().lower():
                        statement = re.sub(r'unique primary index.*;', ';', statement.strip().lower(), flags=re.DOTALL)\
                            .upper()\
                            .replace('\n;', ';')
                    if 'primary' in statement.strip().lower():
                        statement = re.sub(r'primary.*;', ';', statement.strip().lower(), flags=re.DOTALL)\
                            .upper()\
                            .replace('\n;', ';')
                        # statement = statement.upper().replace("PRIMARY INDEX", ";\n/*PRIMARY INDEX")
                    if 'index' in statement.strip().lower():
                        statement = re.sub(r'index.*;', ';', statement.strip().lower(), flags=re.DOTALL)\
                            .upper()\
                            .replace('\n;', ';')
                        # statement = statement.upper().replace("INDEX", ";\n/*INDEX")

                    # removing compress junk from the DDL
                    stmt = []
                    for i, line in enumerate(statement.splitlines()):
                        if 'COMPRESS' in line:
                            # print("comp")
                            if i == len(statement.splitlines()) - 1:
                                line = line[:line.index('COMPRESS')] + ');'
                            else:
                                line = line[:line.index('COMPRESS')] + ','
                        elif '\'' in line:
                            line = "".rstrip()
                        else:
                            line = line
                        stmt.append(line.strip())
                    statement = " \n".join(str(x) for x in stmt)
                    print(statement)

                if statement.endswith(';'):
                    statement = "\n" + statement + "\n"
                else:
                    statement = statement
                # finally write it to output file
                out.write(statement)
        # finally remove the temp file if any
        silent_remove(_input)


def build_sql(inpt_file, conf=None):
    sfdb = conf['snowflake']['database'].get()
    sfschema = conf['snowflake']['schema'].get()

    if os.path.isdir(inpt_file):
        print("input path is a directory")
        for root, dirs, files in os.walk(inpt_file):
            for file in files:
                in_filename = root + '/' + file
                print('Working on', in_filename)
                if is_source(in_filename):
                    # out_filename = in_filename + '.sql'
                    out_raw_file = get_outfile_full_name(in_filename, 'raw')
                    out_sql_file = get_outfile_full_name(in_filename, 'sql')

                    print('Generating the output sql...')
                    # process_bteq_scripts(in_filename, out_filename, skip_lines_list)

                    # raw
                    parse_lines(in_filename, out_raw_file, tuple(STMT_START_KW), tuple(STMT_END_KW), STMT_SKIP_KW)

                    # final sql
                    parse_sql(out_raw_file, out_sql_file, sfdb, sfschema)

                    print('conversion completed successfully\n')
    elif os.path.isfile(inpt_file):
        print("input path is a single file")
        out_raw_file = get_outfile_full_name(inpt_file, 'raw')
        out_sql_file = get_outfile_full_name(inpt_file, 'sql')

        # process_bteq_scripts(inpt_file, inpt_file + '.sql', skip_lines_list)
        # outpt_file = get_outfile_full_name(inpt_file)

        # raw
        parse_lines(inpt_file, out_raw_file, tuple(STMT_START_KW), tuple(STMT_END_KW), STMT_SKIP_KW)

        # final sql
        parse_sql(out_raw_file, out_sql_file, sfdb, sfschema)
    else:
        print('Not a file or directory', inpt_file, file=sys.stderr)
        sys.exit(-1)
