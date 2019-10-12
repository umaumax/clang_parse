#!/usr/bin/env python3

import sys
import re
import argparse

from clang.cindex import Index
from clang.cindex import Config

from vprint import vprint


def get_func_name(displayname):
    # NOTE: you can use node.spelling instead of this function
    name = str(displayname).split('(')[0]
    return name


class ClangFuncRangeParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.index = Index.create()
        # NOTE: for avoid search extra include files
        # NOTE: Maybe, system-header-prefix is not needed?
        # NOTE: If you want to see the help of clang index parser, add '--help' options to below list
        # args = ['-nobuiltininc', '-nostdinc++', '--system-header-prefix=".*"']
        args = ['-nobuiltininc']
        self.tu = self.index.parse("", [filepath, *args])
        if not self.tu:
            parser.error("unable to load input")

    def print_all(self):
        def _lambda(node, parent):
            if (str(node.extent.start.file) == self.filepath):
                # print("file : %s" % node.extent.start.file)
                # print("kind : %s" % node.kind.name)
                # print("function : %s" % node.displayname)
                # print(" from line:%s column:%s" % (node.extent.start.line, node.extent.start.column))
                # print(" to   line:%s column:%s" % (node.extent.end.line, node.extent.end.column))

                # NOTE: end without underscore
                re_snake = re.compile(r'[a-z0-9_]*[a-z0-9]')
                re_snake_end_with_underscore = re.compile(r'[a-z_0-9]+_')
                re_camel = re.compile(r'[a-z0-9]+([A-Z0-9][a-z0-9]*)*')
                re_upper_camel = re.compile(r'([A-Z0-9][a-z0-9]*)+')

                google_coding_rule_name_def = {
                    'STRUCT_DECL': re_upper_camel,
                    'CLASS_DECL': re_upper_camel,
                    'FUNCTION_DECL': re_upper_camel,
                    'FUNCTION_TEMPLATE': re_upper_camel,
                    'CXX_METHOD': re_upper_camel,
                    'FIELD_DECL': None,
                    'FIELD_DECL.CLASS_DECL': re_snake_end_with_underscore,
                    'FIELD_DECL.CLASS_TEMPLATE': re_snake_end_with_underscore,
                    'MEMBER_REF': re_snake_end_with_underscore,
                    'FIELD_DECL.STRUCT_DECL': re_snake,
                    'FIELD_DECL.UNION_DECL': re_snake,
                    'VAR_DECL': re_snake,
                    'PARM_DECL': re_snake,
                    'DECL_REF_EXPR': re_snake,
                    'NAMESPACE': re_snake,
                    'TYPE_REF': None,
                    'CALL_EXPR': None,
                    'TRANSLATION_UNIT': None,  # TODO: add filename check
                    'TEMPLATE_TYPE_PARAMETER': None,
                    'CONSTRUCTOR': None,
                    'DESTRUCTOR': None,
                    'UNEXPOSED_EXPR': None,
                    'MEMBER_REF_EXPR': None,
                }

                name = node.displayname
                if name != "":
                    if node.kind.name in google_coding_rule_name_def:
                        name_re = google_coding_rule_name_def[node.kind.name]
                        if name_re is not None:
                            if node.kind.name == "FIELD_DECL":
                                if parent is not None:
                                    key = node.kind.name + '.' + parent.kind.name
                                    if key in google_coding_rule_name_def:
                                        name_re = google_coding_rule_name_def[key]
                                    else:
                                        print("not supported pattern {}({})".format(name, key))
                            if node.kind.name in ["CXX_METHOD", "FUNCTION_DECL", "FUNCTION_TEMPLATE"]:
                                name = node.spelling
                                # NOTE: for debug
                                # vprint(node)
                            if not name_re.fullmatch(name):
                                print("{} wrong name : {}".format(node.kind.name, name))
                    else:
                        if node.displayname:
                            print("other display name: {}".format(node.kind.name))
                            print("other display name: {}".format(node.displayname))
            return True
        self.traverse(_lambda)

    def traverse(self, f):
        self.traverse_body(self.tu.cursor, None, f)

    def traverse_body(self, node, parent, f):
        ret = f(node, parent)
        if not ret:
            return
        parent = node
        for child in node.get_children():
            ret = self.traverse_body(child, parent, f)
            if not ret:
                break
        return ret


def main():
    Config.set_compatibility_check(False)
    # NOTE: for darwin
    Config.set_library_path("/usr/local/opt/llvm/lib")

    parser = argparse.ArgumentParser()
    parser.add_argument('--style', type=str, help='coding rule (only google is supported)')
    parser.add_argument('filepath')

    args, extra_args = parser.parse_known_args()

    clang_func_range_parser = ClangFuncRangeParser(args.filepath)
    clang_func_range_parser.print_all()


if __name__ == '__main__':
    main()
