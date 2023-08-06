import argparse
import contextlib
import os
import re
import tempfile
import zipfile

import lief

METHODS_BLACKLIST = ("<init>", "<clinit>")
LEGAL_NAME_REGEX = re.compile("^[a-zA-Z]\w*$")
JAVASCRIPT_KEYWORDS = (
    "break",
    "case",
    "catch",
    "class",
    "const",
    "continue",
    "debugger",
    "default",
    "delete",
    "do",
    "else",
    "export",
    "extends",
    "finally",
    "for",
    "function",
    "if",
    "import",
    "in",
    "instanceof",
    "new",
    "return",
    "super",
    "switch",
    "this",
    "throw",
    "try",
    "typeof",
    "var",
    "void",
    "while",
    "with",
    "yield",
)
TYPESCRIPT_KEYWORDS = (
    "null",
    "package",
    "type",
    "static",
    "default",
    "number",
    "import",
    "with",
    "implements",
    "delete",
    "debugger",
    "enum",
    "private",
    "class",
    "public",
    "get",
    "as",
    "true",
    "let",
    "false",
    "any",
    "string",
    "interface",
    "module",
)


def get_legal_name(name: str):
    if LEGAL_NAME_REGEX.match(name) and name not in JAVASCRIPT_KEYWORDS:
        return name
    else:
        # TODO: handle illegal characters
        return "_" + name


def get_legal_pretty_name(name: str):
    names = name.split(".")
    return ".".join(map(get_legal_name, names))


@contextlib.contextmanager
def declare_namespace(name):
    indent = ""
    if name is not None:
        escaped_prefix = get_legal_pretty_name(name)
        print(f"declare namespace {escaped_prefix} {{")
        indent = "\t"

    yield indent

    if name is not None:
        print("}\n")


def java_type_to_typescript(type):
    if type.type == lief.DEX.Type.TYPES.PRIMITIVE:
        if type.value in (
            lief.DEX.Type.PRIMITIVES.FLOAT,
            lief.DEX.Type.PRIMITIVES.DOUBLE,
            lief.DEX.Type.PRIMITIVES.SHORT,
            lief.DEX.Type.PRIMITIVES.INT,
            lief.DEX.Type.PRIMITIVES.LONG,
            lief.DEX.Type.PRIMITIVES.BYTE,
        ):
            return "number"
        elif type.value == lief.DEX.Type.PRIMITIVES.BOOLEAN:
            return "boolean"
        elif type.value == lief.DEX.Type.PRIMITIVES.CHAR:
            return "string"
    elif type.type == lief.DEX.Type.TYPES.CLASS:
        return f"Java.Wrapper<{type.value.pretty_name}>"


def generate_choose_definitions(classes):
    print("declare namespace Java {")
    for cls in classes:
        escaped_pretty_name = get_legal_pretty_name(cls.pretty_name)
        print(
            f'\tfunction choose(className: "{cls.pretty_name}", callbacks: ChooseCallbacks<{escaped_pretty_name}>): void;'
        )
        print(f'\tfunction use(className: "{cls.pretty_name}"): Java.Wrapper<{escaped_pretty_name}>;')
    print("}")


def generate_type_definitions(d, prefix=None):
    indent = ""
    contains_classes = any(isinstance(i, lief.DEX.Class) for i in d.values())
    if contains_classes:
        with declare_namespace(prefix) as indent:
            for k, v in d.items():
                if isinstance(v, lief.DEX.Class):
                    name = v.pretty_name.split(".")[-1]
                    legal_name = get_legal_name(name)
                    print(f"{indent}interface {legal_name} {{")
                    method_names = set(map(lambda m: m.name, v.methods))
                    for method_name in method_names:
                        # TODO: what does Frida do here?
                        if get_legal_name(method_name) != method_name:
                            continue
                        print(f"{indent}\t{method_name}: Java.MethodDispatcher<{v.pretty_name}>;")
                    for field in v.fields:
                        field_name = field.name
                        # TODO: what does Frida do here?
                        if get_legal_name(field_name) != field_name:
                            continue
                        if field.name in method_names:
                            field_name = "_" + field_name
                        typescript_type = java_type_to_typescript(field.type)
                        if typescript_type is not None:
                            print(f"{indent}\t{field_name}: Java.Field<{typescript_type}>;")
                        else:
                            print(f"{indent}\t{field_name}: Java.Field;")
                    print(f"{indent}}}\n")

    for k, v in d.items():
        if isinstance(v, dict):
            if prefix is None:
                generate_type_definitions(v, prefix=k)
            else:
                generate_type_definitions(v, prefix=prefix + "." + k)


def insert_class_to_dict(classes, path, cls):
    curr = classes
    for key in path[:-1]:
        if key not in curr:
            curr[key] = {}
        curr = curr[key]

    curr[path[-1]] = cls


def get_dex_files(path: str):
    if os.path.isdir(path):
        files = os.listdir(path)
        return [os.path.join(path, file) for file in files if file.endswith(".dex")]

    tmpdir = tempfile.TemporaryDirectory()
    with zipfile.ZipFile(path, "r") as apk_file:
        files = apk_file.namelist()
        for file_name in files:
            if file_name.endswith(".dex"):
                apk_file.extract(file_name, tmpdir.name)
    return [os.path.join(tmpdir.name, file) for file in os.listdir(tmpdir.name)]


def generate(args):
    # lief is a bit broken so we need to keep a reference to the Dex instance
    # otherwise our classes will be freed before we are done with them
    dexes_list = list()

    classes_list = list()
    for path in args.paths:
        for file in get_dex_files(path):
            dex = lief.DEX.parse(file)
            dexes_list.append(dex)
            classes_list.extend(dex.classes)

    classes_dict = dict()
    for cls in classes_list:
        path = cls.pretty_name.split(".")
        insert_class_to_dict(classes_dict, path, cls)

    generate_type_definitions(classes_dict)
    generate_choose_definitions(classes_list)


def get_arguments_parser():
    parser = argparse.ArgumentParser(description="Generate TypeScript definition files for use with Frida")
    parser.add_argument(
        "--type", choices=["Java"], default="Java", help="The type of package to expect in the given paths"
    )
    parser.add_argument(
        "paths", metavar="FILE", nargs="+", help="a file or directory containing the program to generate from"
    )
    return parser


def main():
    args = get_arguments_parser().parse_args()
    generate(args)


if __name__ == "__main__":
    main()
