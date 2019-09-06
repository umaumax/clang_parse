class pycolor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'


def vprint(obj, level=0, **kwargs):
    indent = '\t' * level
    print('{}"{}" {}'.format(indent, obj, type(obj)))

    function_list = []
    method_list = []
    for attr in dir(obj):
        try:
            attr_type = getattr(obj, attr)
            if 'all' in kwargs and kwargs['all']:
                if attr.startswith('__'):
                    # NOTE: skip print
                    # print('{}"{}" {} {}'.format(indent, attr, type(attr_type), attr_type))
                    pass
                else:
                    pass
            else:
                pass
            if not attr.startswith('__'):
                if isinstance(attr, tuple) or \
                        isinstance(attr, list) or \
                        isinstance(attr, dict):
                    print('{}"{}" {}'.format(indent, attr, type(attr)))
                    vprint(getattr(obj, attr), (level + 1), **kwargs)
                else:
                    attr_type_str = str(type(attr_type))
                    if attr_type_str == "<class 'method'>":
                        method_list.append(attr)
                    elif attr_type_str == "<class 'function'>":
                        function_list.append(attr)
                    else:
                        print('{}"{}"={}({})'.format(indent, pycolor.YELLOW + attr + pycolor.END, pycolor.BLUE + str(attr_type) + pycolor.END, type(attr_type)))
            else:
                pass
                # print('{}"{}" {}'.format(indent, attr, type(attr)))
        except Exception as e:
            print(pycolor.RED + '# Exception at {}:{}({}) obj:{}({})'.format(attr, e, type(e), obj, type(obj)) + pycolor.END)
    print('{}{}:{}'.format(indent, pycolor.GREEN + "functions" + pycolor.END, function_list))
    print('{}{}:{}'.format(indent, pycolor.PURPLE + "methods" + pycolor.END, method_list))
