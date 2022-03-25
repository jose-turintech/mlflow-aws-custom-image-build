"""
This module contains useful methods for the representation of different data structures
"""


def get_start_end(title, print_char="-", size=150, nl_str=True, nl_end=True):
    """
    :return:
        start: ------------------------------- <title> -------------------------------
          end: -----------------------------------------------------------------------
    """
    title_len = len(title)
    print_char_group = print_char * int((size - title_len - 2) / 2)
    start = " ".join([print_char_group, title, print_char_group])
    end = print_char * len(start)
    if nl_str:
        start = f"\n{start}"
    if nl_end:
        end = f"{end}\n"
    return start, end


def get_list_formatter(
        data: list, indent=1, title: str = None, print_char="-", size=150, nl_str=True, nl_end=True
) -> str:
    """
    :return:
            - <value1>
            - <value2>
            ...
            - <valueN>
    """
    start, end = (
        get_start_end(title=title, print_char=print_char, size=size, nl_str=nl_str, nl_end=nl_end) if title else
        ("", "")
    )
    union = '\n' + '    ' * indent + '- '
    data_str = start + union
    data_str = data_str + union.join([str(value) for value in data])
    return data_str + ("\n" + end if nl_end else end)


def get_dict_formatter(
        data: dict, title: str = None, print_char="-", size=150, nl_str=True, nl_end=True, indent=1
) -> str:
    """
    :return:
        ------------------------------- <title> -------------------------------
            - <key1>                  : <value1>
            - <key3>                  : <value2>
            ...
            - <keyN>                  : <valueN>
        -----------------------------------------------------------------------
    """
    start, end = (
        get_start_end(title=title, print_char=print_char, size=size, nl_str=nl_str, nl_end=nl_end) if title else
        ("", "")
    )

    union = '\n' + '    ' * indent + '- '
    keys_str = [str(key) for key in data.keys()]
    key_size = len(max(keys_str, key=len)) + 1

    data_str = start + union
    data_str = data_str + union.join([f"{key:<{key_size}}: {value}" for key, value in data.items()])
    return data_str + "\n" + end


def get_data_formatter(
        data: dict or list, title: str = None, print_char: str = "-", levels: int = 2, size=150, nl_str=True,
        nl_end=True, indent=1
) -> str:
    """
    :return:
        ------------------------------- <title> -------------------------------
            - <value1>
                - <key1> : <value1>
                - <key2> : <value2>
            - <value2>
                - <key3> :
                    - <value3>
        -----------------------------------------------------------------------
    """
    args = dict(print_char=print_char, size=size, nl_str=nl_str, nl_end=nl_end)
    start, end = get_start_end(title=title, **args) if title else ("", "")
    args['nl_str'] = args['nl_end'] = False
    union = '\n' + '    ' * indent + '- '
    data_str = start
    if indent > levels or not isinstance(data, (dict, list)):
        return str(data)
    if isinstance(data, dict):
        key_size = len(max(data.keys(), key=len)) + 1 if data.keys() else 0
        for key, value in data.items():
            _value = get_data_formatter(data=value, levels=levels, indent=indent + 1, **args)
            data_str += union + f"{key:<{key_size}}: {_value}"
    else:
        for value in data:
            if not isinstance(value, (dict, list)):
                data_str += union
            data_str += get_data_formatter(data=value, levels=levels, indent=indent, **args)
    return data_str + ("\n" if nl_end else "") + end
