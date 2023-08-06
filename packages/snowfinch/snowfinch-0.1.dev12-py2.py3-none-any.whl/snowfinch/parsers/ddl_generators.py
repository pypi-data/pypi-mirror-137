from snowfinch.logger import log

logger = log.get_logger()


def get_ddl(engine, db, schema, table):
    ddl = None
    logger.info(f"Fetching DDL from {engine}")
    if engine.lower() == 'mssql':
        ddl = get_ddl_mssql(db, schema, table)
    elif engine.lower() == 'teradata':
        ddl = get_ddl_tera(db, schema, table)
    else:
        print("DB engine not  supported yet")
    return ddl


def get_sproc_def(engine, db, schema, sp_name):
    sp_source_text = None
    logger.info(f"Fetching DDL from {engine}")
    if engine.lower() == 'mssql':
        sp_source_text = get_sproc_def_mssql(db, schema, sp_name)
    elif engine.lower() == 'teradata':
        sp_source_text = get_sproc_def_tera(db, sp_name)
    else:
        print("DB engine not  supported yet")
    return sp_source_text


def get_ddl_tera(db, schema, table):
    print(db)
    ddl_stmt = f"""
with snowfinch_ddl as(
select 
C.databasename,
C.tablename,
columntype,
case columntype 
when 'CF' then 'CHAR'
when 'CV' then 'VARCHAR'
when 'DA' then 'DATE'
when 'I8' then 'BIGINT'
when 'TS' then 'TIMESTAMP'
when 'D' then 'DECIMAL'
when 'I' then 'INTEGER'
when 'I2' then 'SMALLINT' 
when 'I1' then 'BYTEINT'
when 'N' then 'NUMBER' 
when 'F' then 'FLOAT' 
end as dtype,
case 
when columntype in ('CF','CV') then '('||trim(cast(columnlength as integer))||')'
when columntype in ('D','N') then '('||trim(cast(decimaltotaldigits as integer))||','||trim(cast(decimalfractionaldigits as integer))||')'
when columntype in ('TS') then '('||trim(cast(decimalfractionaldigits as integer))||')'
else ''
end dlen,
 case nullable when 'N' then 'NOT NULL' else '' end as nulltype,
 case 
 when columntype in ('CF','CV','I8','I','I2','D','N','F','I1') and defaultvalue is not null then 'DEFAULT '||trim(defaultvalue) 
 when columntype in ('DA') and defaultvalue not like all('%date','null') then 'DEFAULT '''||trim(defaultvalue)||trim('''::DATE') 
 when columntype in ('DA') and defaultvalue like ('%date') then 'DEFAULT '||trim('CURRENT_DATE')||trim('::DATE') 
 else '' 
 end as deftype,
 max(columnid) over (partition by C.databasename,C.tablename order by columnid) as maxid,
 min(columnid) over (partition by C.databasename,C.tablename order by columnid) as minid,
 case when maxid=columnid then trim(coalesce(I.keycolumns,''))||' );' else ',' end as commadelim,
 case when minid=columnid and T.commitopt='N' and C.databasename not like all('%temp%','%data%') then 'CREATE TABLE IF NOT EXISTS {schema}.'||upper(C.tablename)||' ( '
 when minid=columnid and T.commitopt='N' and C.databasename like any('%temp%','%data%') then 'CREATE TABLE IF NOT EXISTS {schema}.'||upper(C.tablename)||' ( '
 when minid=columnid and T.commitopt in ('P','D') then 'CREATE TABLE IF NOT EXISTS {schema}.'||upper(C.tablename)||' ( 'else '' end as createtbl,
 case 
 when idcoltype in ('GD','GA') then 'AUTOINCREMENT' else '' 
 end as autoinc,
 columnid,
 dense_rank() over (order by C.tablename) TBL_COUNT,
 case when T.commitopt in ('P','D') then 'Temporary' else 'Permanent' end as tbltype,
 createtbl||columnname||' '||trim(dtype)||trim(dlen)||' '||trim(nulltype)||' '||trim(deftype)||' '||trim(autoinc)||' '||trim(commadelim) as ddl
from dbc.columnsv C
join dbc.tablesv T
on C.databasename=T.databasename
and C.tablename=T.tablename
and T.tablekind IN('T','O')
left outer join 
(select databasename,tablename,COALESCE(', CONSTRAINT PK_'||trim(tablename)||' PRIMARY KEY ('||TRIM(TRAILING ',' FROM XMLAGG(columnName || ',' ORDER BY columnPosition)(varchar(4000)))||' )','') AS KeyColumns
from dbc.indicesv
group by 1,2
where indextype='K' or uniqueflag='Y'
) I
on I.databasename=T.databasename
and I.tablename=T.tablename
where 
--upper(c.databasename) in ('PI','RDM','ETL_TEMP_PI','ETL_DATA_PI','EDW_V20','QADATA_PI')
upper(c.databasename) in ('{db}')
and upper(c.tablename)='{table}'
)

sel DDL
from snowfinch_ddl
order by tbltype,databasename,tablename,columnid;
 """
    # print(ddl_stmt)
    return ddl_stmt


def get_ddl_mssql(db, schema, table):
    print(db)

    ddl_stmt = f"""
DECLARE @table_name SYSNAME
        SELECT @table_name = 'dbo.{table}'
        DECLARE 
              @object_name SYSNAME
            , @object_id INT
        SELECT 
              @object_name = '' + s.name + '.' + o.name + ''
            , @object_id = o.[object_id]
        FROM sys.objects o WITH (NOWAIT)
        JOIN sys.schemas s WITH (NOWAIT) ON o.[schema_id] = s.[schema_id]
        WHERE s.name + '.' + o.name = @table_name
            AND o.[type] = 'U'
            AND o.is_ms_shipped = 0

        DECLARE @SQL NVARCHAR(MAX) = ''

        ;WITH index_column AS 
        (
            SELECT 
                  ic.[object_id]
                , ic.index_id
                , ic.is_descending_key
                , ic.is_included_column
                , c.name
            FROM sys.index_columns ic WITH (NOWAIT)
            JOIN sys.columns c WITH (NOWAIT) ON ic.[object_id] = c.[object_id] AND ic.column_id = c.column_id
            WHERE ic.[object_id] = @object_id
        ),
        fk_columns AS 
        (
             SELECT 
                  k.constraint_object_id
                , cname = c.name
                , rcname = rc.name
            FROM sys.foreign_key_columns k WITH (NOWAIT)
            JOIN sys.columns rc WITH (NOWAIT) ON rc.[object_id] = k.referenced_object_id AND rc.column_id = k.referenced_column_id 
            JOIN sys.columns c WITH (NOWAIT) ON c.[object_id] = k.parent_object_id AND c.column_id = k.parent_column_id
            WHERE k.parent_object_id = @object_id
        )
        SELECT @SQL = 'CREATE TABLE IF NOT EXISTS {schema}.' + substring(@object_name,5,len(@object_name)) + CHAR(13) + '(' + CHAR(13) + STUFF((
            SELECT CHAR(9) + ', ' + c.name + ' ' + 
                CASE WHEN c.is_computed = 1
                    THEN 'AS ' + cc.[definition] 
                    ELSE case when tp.name = 'datetime' then 'timestamp_ntz(9)'  else tp.name end + 
                        CASE WHEN tp.name IN ('varchar', 'char', 'varbinary', 'binary')
                               THEN '(' + CASE WHEN c.max_length = -1 THEN '16777216' ELSE CAST(c.max_length AS VARCHAR(5)) END + ')'
                             WHEN tp.name IN ('nvarchar', 'nchar')
                               THEN '(' + CASE WHEN c.max_length = -1 THEN '16777216' ELSE CAST(c.max_length / 2 AS VARCHAR(5)) END + ')'
                             WHEN tp.name IN ('datetime2', 'time2', 'datetimeoffset') 
                               THEN '(' + CAST(c.scale AS VARCHAR(5)) + ')'
                             WHEN tp.name IN ('decimal','numeric') 
                               THEN '(' + CAST(c.[precision] AS VARCHAR(5)) + ',' + CAST(c.scale AS VARCHAR(5)) + ')'
                            ELSE ''
                        END +  
                        CASE WHEN ic.is_identity = 1 THEN ' IDENTITY(' + CAST(ISNULL(ic.seed_value, '0') AS CHAR(1)) + ',' + CAST(ISNULL(ic.increment_value, '1') AS CHAR(1)) + ')' ELSE '' END + 
                        CASE WHEN c.is_nullable = 1 THEN ' NULL' ELSE ' NOT NULL' END +
                        CASE WHEN dc.[definition] IS NOT NULL THEN ' DEFAULT' + dc.[definition] ELSE '' END                
                END + CHAR(13)
            FROM sys.columns c WITH (NOWAIT)
            JOIN sys.types tp WITH (NOWAIT) ON c.user_type_id = tp.user_type_id
            LEFT JOIN sys.computed_columns cc WITH (NOWAIT) ON c.[object_id] = cc.[object_id] AND c.column_id = cc.column_id
            LEFT JOIN sys.default_constraints dc WITH (NOWAIT) ON c.default_object_id != 0 AND c.[object_id] = dc.parent_object_id AND c.column_id = dc.parent_column_id
            LEFT JOIN sys.identity_columns ic WITH (NOWAIT) ON c.is_identity = 1 AND c.[object_id] = ic.[object_id] AND c.column_id = ic.column_id
            WHERE c.[object_id] = @object_id
            ORDER BY c.column_id
            FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, CHAR(9) + ' ')
            + ISNULL((SELECT CHAR(9) + ', CONSTRAINT ' + k.name + ' PRIMARY KEY  (' + 
                            (SELECT STUFF((
                                 SELECT ', ' + c.name + ' ' + CASE WHEN ic.is_descending_key = 1 THEN 'DESC' ELSE '' END
                                 FROM sys.index_columns ic WITH (NOWAIT)
                                 JOIN sys.columns c WITH (NOWAIT) ON c.[object_id] = ic.[object_id] AND c.column_id = ic.column_id
                                 WHERE ic.is_included_column = 0
                                     AND ic.[object_id] = k.parent_object_id 
                                     AND ic.index_id = k.unique_index_id     
                                 FOR XML PATH(N''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, ''))
                    + ')' + CHAR(13)
                    FROM sys.key_constraints k WITH (NOWAIT)
                    WHERE k.parent_object_id = @object_id 
                        AND k.[type] = 'PK'), '') + ')'  + CHAR(13)

SELECT @SQL AS DDL;
"""

    # print(ddl_stmt)
    return ddl_stmt


def get_sproc_def_mssql(_db, _schema, _sp_name):
    sproc_def = f"""
    SELECT SPECIFIC_NAME, ROUTINE_DEFINITION
    FROM {_db}.INFORMATION_SCHEMA.ROUTINES
    WHERE  
    UPPER(SPECIFIC_CATALOG) = '{_db}'
    AND UPPER(SPECIFIC_SCHEMA) = '{_schema}'
    AND UPPER(ROUTINE_TYPE) = 'PROCEDURE'
    AND UPPER(SPECIFIC_NAME) = '{_sp_name}'
    """
    return sproc_def


def get_sproc_args_mssql(_db, _schema, _sp_name):
    args_sql = f"""
    SELECT  
    P.SPECIFIC_NAME,
    UPPER(REPLACE(CONCAT(P.PARAMETER_NAME, ' ',
    CASE 
    WHEN P.DATA_TYPE = 'INT' then P.DATA_TYPE 
    WHEN P.DATA_TYPE = 'datetime' then 'timestamp_ntz(9)'  
    
    WHEN P.DATA_TYPE IN ('varchar', 'char', 'varbinary', 'binary') THEN 
        CASE 
            WHEN P.CHARACTER_MAXIMUM_LENGTH = -1 THEN  P.DATA_TYPE 
            ELSE '(' + CAST( P.CHARACTER_MAXIMUM_LENGTH AS VARCHAR(5)) + ')'
        END
    WHEN P.DATA_TYPE  IN ('nvarchar', 'nchar') THEN 
        CASE
            WHEN P.CHARACTER_MAXIMUM_LENGTH = -1 THEN P.DATA_TYPE 
            ELSE '(' + CAST( P.CHARACTER_MAXIMUM_LENGTH AS VARCHAR(5)) + ')'
        END

    ELSE P.DATA_TYPE
    END),'@','')) AS  PARAM
    FROM {_db}.INFORMATION_SCHEMA.PARAMETERS p
    WHERE 
    UPPER(P.SPECIFIC_SCHEMA) = '{_schema}' 
    AND UPPER(P.SPECIFIC_NAME) = '{_sp_name}';
    """
    return args_sql


def get_sproc_def_tera(_engine, _sp_name):
    sproc_def = f"""
    """
    return sproc_def
