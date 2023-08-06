import re

# RegExes for SQL-Server dialect that Snowflake doesn't support

# NULL (explicit NULL constraint) -- ignore
null_constraint_re = re.compile('(.*)((?<!NOT)\s+NULL(?!::))(.*)', re.IGNORECASE)
is_null_condition_re = re.compile('.*IS NULL.*', re.IGNORECASE)

# NVARCHAR => VARCHAR
nvarchar_re = re.compile('(.*)\ (NVARCHAR)(.*)', re.IGNORECASE)

# NVARCHAR => VARCHAR
nchar_re = re.compile('(.*)\ (NCHAR)(.*)', re.IGNORECASE)

# ON PRIMARY => ignore
on_primary_re = re.compile('(.*)\ (ON PRIMARY)(.*)', re.IGNORECASE)

# DATETIME => TIMESTAMP
datetime_re = re.compile('(.*)\ (DATETIME)(.*)', re.IGNORECASE)

# BIT => BOOLEAN
bit_re = re.compile('(.*)\ (BIT)(.*)', re.IGNORECASE)


def parse_mssql(in_sql, out_sql, no_comments):
    # processing mode
    comment_lines = None
    term_re = None

    for line in in_sql:
        # state variables
        pre = None
        clause = None
        post = None
        comment = None

        sql = line.rstrip()
        sql = sql.replace('[', '').replace(']', '')

        # print >> sys.stdout, 'input: ' + sql

        if comment_lines:
            result = term_re.match(sql)
            if result:
                comment_lines = None
                term_re = None
            sql = '-- {0}'.format(sql)

        # NVARCHAR => VARCHAR
        result = nvarchar_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} VARCHAR {1}\t\t-- {2}'.format(pre, post, clause)

        # NCHAR => CHAR
        result = nchar_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} CHAR {1}\t\t-- {2}'.format(pre, post, clause)

        # DATETIME => TIMESTAMP
        result = datetime_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} TIMESTAMP {1}\t\t-- {2}'.format(pre, post, clause)

        # BIT => BOOLEAN
        result = bit_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} BOOLEAN {1}\t\t-- {2}'.format(pre, post, clause)

        # NULL (without NOT) => implicit nullable
        result = null_constraint_re.match(sql)
        if result and is_null_condition_re.match(sql):
            # we are in sql_query or DML, so not looking at a constraint
            result = None
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}{1}\t\t-- {2}'.format(pre, post, clause)

        # ON PRIMARY => ignore
        result = on_primary_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}{1}\t\t-- {2}'.format(pre, post, clause)

        # write out possibly modified line
        out_sql.write(sql)
        if comment:
            out_sql.write('\t\t-- {0}'.format(comment))
        out_sql.write('\n')
        continue


def append_comment(old_comment, new_comment, no_comments):
    if no_comments:
        return None
    if old_comment and new_comment:
        return '{0} // {1}'.format(old_comment, new_comment)
    if not old_comment:
        return new_comment
    return old_comment


# if __name__ == "__main__":
#     parse_mssql(inputfile, outfile, no_comments)
#     inputfile.close()
#     outfile.close()
#     print("done parsing " + inputfile.name)
