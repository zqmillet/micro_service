def value_to_string(value):
    if isinstance(value, str):
        prefix = '"'
        suffix = '"'
    else:
        prefix = ''
        suffix = ''
    return '{prefix}{value}{suffix}'.format(
        prefix = prefix,
        value = value,
        suffix = suffix
    )

def fetch_python_type(mysql_type):
    mysql_type = mysql_type.split('(')[0]
    type_dictionary = {
        int:   ['tinyint', 'smallint', 'mediumint', 'int', 'bigint', 'bit'],
        float: ['float', 'double', 'decimal'],
        str:   ['char', 'varchar', 'tinytext', 'text', 'mediumtext', 'longtext']
    }

    for python_type, mysql_type_string_list in type_dictionary.items():
        if mysql_type in mysql_type_string_list:
            return python_type
    return lambda x: x