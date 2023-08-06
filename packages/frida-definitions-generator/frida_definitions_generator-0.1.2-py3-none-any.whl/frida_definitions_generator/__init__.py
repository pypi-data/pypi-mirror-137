import contextlib
import os
import re
import tempfile
import zipfile

import lief

__version__ = "0.1.2"

METHODS_BLACKLIST = ("<init>", "<clinit>")
LEGAL_NAME_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z\d_$]*$")
ILLEGAL_NAME_CHARACTERS_REGEX = re.compile(r"[^a-zA-Z\d_$]")
LEGAL_FIRST_CHAR_REGEX = re.compile(r"^[a-zA-Z_]$")
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


class APKDexFiles:
    def __init__(self, apk_path: str):
        self._tmpdir = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(apk_path, "r") as apk_file:
            files = apk_file.namelist()
            for file_name in files:
                if file_name.endswith(".dex"):
                    apk_file.extract(file_name, self._tmpdir.name)
        self.files = [os.path.join(self._tmpdir.name, file) for file in os.listdir(self._tmpdir.name)]

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        self._index += 1
        if self._index > len(self.files):
            raise StopIteration
        return self.files[self._index - 1]


def get_legal_name(name: str):
    if LEGAL_NAME_REGEX.match(name) and name not in JAVASCRIPT_KEYWORDS:
        return name

    stripped_name = ILLEGAL_NAME_CHARACTERS_REGEX.sub("", name)
    if len(stripped_name) and LEGAL_FIRST_CHAR_REGEX.match(stripped_name[0]):
        return stripped_name

    return "_" + stripped_name


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
        legal_name = get_legal_pretty_name(type.value.pretty_name)
        return f"Java.Wrapper<{legal_name}>"


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
                    print(f"{indent}interface {legal_name} extends Java.Wrapper {{")
                    method_names = set(map(lambda m: m.name, v.methods))
                    for method_name in method_names:
                        # TODO: what does Frida do here?
                        if get_legal_name(method_name) != method_name:
                            continue
                        holder_legal_name = get_legal_pretty_name(v.pretty_name)
                        print(f"{indent}\t{method_name}: Java.MethodDispatcher<{holder_legal_name}>;")
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

    return APKDexFiles(path)


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
