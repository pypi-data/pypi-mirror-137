"""This module provides the SQL request to extract the metadata of a
PostgreSQL database.
"""

import inspect

REQUEST = """
SELECT
    a.attrelid AS tableid,
    array_agg( distinct i.inhseqno::TEXT || ':' || i.inhparent::TEXT ) AS inherits,
    c.relkind AS tablekind,
    n.nspname AS schemaname,
    c.relname AS relationname,
    tdesc.description AS tabledescription,
    a.attname AS fieldname,
    a.attnum AS fieldnum,
    adesc.description AS fielddescription,
    a.attndims AS fielddim,
    pt.typname AS fieldtype,
    a.attnum AS fieldnum,
    NOT( a.attislocal ) AS inherited,
    cn_uniq.contype AS uniq,
    a.attnotnull OR NULL AS notnull,
    cn_pk.contype AS pkey,
    cn_fk.contype AS fkey,
    cn_fk.conname AS fkeyname,
    cn_fk.conkey AS keynum,
    cn_fk.confrelid AS fkeytableid,
    cn_fk.confkey AS fkeynum,
    cn_fk.confupdtype as fkey_confupdtype,
    cn_fk.confdeltype as fkey_confdeltype
FROM
    pg_class c -- table
    LEFT JOIN pg_description tdesc ON
    tdesc.objoid = c.oid AND
    tdesc.objsubid = 0
    LEFT JOIN pg_namespace n ON
    n.oid = c.relnamespace
    LEFT JOIN pg_inherits i ON
    i.inhrelid = c.oid
    LEFT JOIN pg_attribute a ON
    a.attrelid = c.oid
    LEFT JOIN pg_description adesc ON
    adesc.objoid = c.oid AND
    adesc.objsubid = a.attnum
    JOIN pg_type pt ON
    a.atttypid = pt.oid
    LEFT JOIN pg_constraint cn_uniq ON
    cn_uniq.contype = 'u' AND
    cn_uniq.conrelid = a.attrelid AND
    a.attnum = ANY( cn_uniq.conkey )
    LEFT JOIN pg_constraint cn_pk ON
    cn_pk.contype = 'p' AND
    cn_pk.conrelid = a.attrelid AND
    a.attnum = ANY( cn_pk.conkey )
    LEFT JOIN pg_constraint cn_fk ON
    cn_fk.contype = 'f' AND
    cn_fk.conrelid = a.attrelid AND
    a.attnum = ANY( cn_fk.conkey )
WHERE
    n.nspname <> 'pg_catalog'::name AND
    n.nspname <> 'information_schema'::name AND
    ( c.relkind = 'r'::"char" -- table
      OR c.relkind = 'v'::"char" -- view
      OR c.relkind = 'm' -- materialized view
      OR c.relkind = 'f' -- foreign table/view/mat. view
      OR c.relkind = 'p' -- patitioned table
    ) AND
    a.attnum > 0 -- AND
GROUP BY
    a.attrelid,
    n.nspname,
    c.relname,
    tdesc.description,
    c.relkind,
    a.attnum,
    a.attname,
    a.attnum,
    adesc.description,
    a.attndims,
    a.attislocal,
    pt.typname,
    cn_uniq.contype,
    a.attnotnull,
    cn_pk.contype,
    cn_fk.contype,
    cn_fk.conname,
    cn_fk.conkey,
    cn_fk.confrelid,
    cn_fk.confkey,
    cn_fk.confupdtype,
    cn_fk.confdeltype
ORDER BY
    n.nspname, c.relname, a.attnum
"""

def __get_fqn(db, schema, relation=None, field=None):
    fqn = f'{db}:"{schema}"'
    if relation:
        fqn = f'{fqn}.{relation}'
    if field and not relation:
        raise Exception("Can't have a field without a relation")
    if field:
        fqn = f'{fqn}.{field}'
    return fqn

def __inherits(data, d_rel, d_db):
    d_rel['inherits'] = []
    for elt in data:
        inherited = __get_fqn(*elt)
        d_rel['inherits'].append(inherited)
        d_db['inheritance'].append((d_rel['fqn'], inherited))

def __assoc(data, d_rel, d_db):
    for remote in data.values():
        d_db['association'].append((d_rel['fqn'], __get_fqn(*remote[0])))

def __get_fields(data, d_rel, _):
    order = [None for elt in range(len(data))]
    ret = {}
    for name, props in data.items():
        order[props['fieldnum'] -1] = name
        if props['inherited'] == False:
            ret[name] = props['fieldtype']
    d_rel['order'] = order
    return ret

def __return(data, d_rel, *args):
    d_rel['description'] = data

def schema(metadata):
    """Returns a (dict) representation of the model
    """
    switch = {
        'fields': __get_fields,
        'fkeys': __assoc,
        'inherits': __inherits,
        'description': __return,
    }
    d_model = {}
    entry = metadata['byname']
    for key in entry:
        db_name, sch, relation = key
        if sch.find('half_orm_meta') != -1:
            continue
        if not db_name in d_model:
            d_model[db_name] = {}
            d_db = d_model[db_name]
            d_db['association'] = []
            d_db['inheritance'] = []
        if not sch in d_db:
            d_db[sch] = {}
            d_db[sch]['fqn'] = __get_fqn(db_name, sch)
            d_db[sch]['relations'] = {}
        d_sch = d_db[sch]['relations']
        d_rel = d_sch[relation] = {}
        d_rel['fqn'] = __get_fqn(db_name, sch, relation)
        for elt in entry[key]:
            val = entry[key][elt]
            if elt in switch:
                d_rel[elt] = {}
                ret = switch[elt](val, d_rel, d_db)
                if ret:
                    d_rel[elt].update(ret)
    return d_model

if __name__ == '__main__':
    import json
    import sys
    from pprint import PrettyPrinter
    from half_orm.model import Model
    from half_orm.model_errors import MissingConfigFile

    pp = PrettyPrinter().pprint
    try:
        pp(Model(sys.argv[1]).schema)
    except IndexError:
        sys.stderr.write(f"USAGE: {sys.argv[0]} <db>\n")
        sys.exit(1)
    except MissingConfigFile:
        sys.stderr.write(f"ERROR: {sys.argv[1]} config file not found.\n")
        sys.exit(1)