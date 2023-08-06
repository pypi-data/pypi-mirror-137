import ast
import json
import os
import sys
import time
from io import StringIO
from pathlib import Path
from typing import Any

from samon.environment import Environment
from samon.parser import DefaultParser
from . import python_minifier


class Visitor(ast.NodeVisitor):
    """Used to list all the modules imported by a script."""

    def __init__(self, lib_path, package):
        self.imports = set()
        self.lib_path = lib_path
        self.package = package

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(self, node):
        if node.level > 0:
            package = self.package[:]
            level = node.level - 1
            while level:
                package.pop()
                level -= 1
            module = ".".join(package)
            if node.module:
                module += "." + node.module
        else:
            module = node.module
        self.imports.add(module)
        for alias in node.names:
            if alias.name == "*":
                continue
            else:
                # Only keep "from X import Y" if X.Y is a module, not if Y
                # is a variable defined in X
                path = os.path.join(self.lib_path, *module.split("."),
                    alias.name + ".py")
                if os.path.exists(path):
                    self.imports.add(module + "." + alias.name)


class BrythonTransformer(ast.NodeTransformer):
    def __init__(self, source_path):
        self.path = source_path
        self.require_function = None

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if node.module == 'django_brython.assets':
            for nname in node.names:
                if nname.name == 'require':
                    self.require_function = nname.asname or nname.name
                    return None

        return node

    def visit_Import(self, node: ast.Import) -> Any:
        for nname in node.names:
            if nname.name == 'django_brython.assets.require':
                self.require_function = nname.asname or nname.name
                return None

        return node

    def generic_visit(self, node: ast.AST) -> ast.AST:
        if isinstance(node, ast.Import):
            return self.visit_Import(node)
        elif isinstance(node, ast.ImportFrom):
            return self.visit_ImportFrom(node)
        elif isinstance(node, ast.Call):
            if hasattr(node.func, 'id') and node.func.id == self.require_function:
                template_path = Path(node.args[0].value)
                if not template_path.is_absolute():
                    template_path = (self.path.parent / node.args[0].value).resolve()
                with template_path.open('r', encoding='utf-8') as f:
                    parser = DefaultParser(environment=Environment(loader=None))
                    template = parser.parse(source=f.read(), template_name=template_path.name)
                    return template.serialize(output='psx')

        return super().generic_visit(node)


def make(package_name, package_path, exclude_dirs=None, output: StringIO=None, exclude_modules=[]):
    if not package_name:
        raise ValueError("package name is not specified")
    # print("Generating package {}".format(package_name))
    VFS = {"$timestamp": int(1000 * time.time())}
    has_init = os.path.exists(os.path.join(package_path, "__init__.py"))
    nb = 0
    if exclude_dirs is None:
        exclude_dirs = []

    if hasattr(ast, 'unparse'):
        ast_unparse_working = True
    else:
        ast_unparse_working = False
        print("ast module hasn't 'unparse' method, bundling assets is not working (require python >= 3.9)", file=sys.stderr)

    for dirpath, dirnames, filenames in os.walk(package_path):
        flag = False
        root_elts = dirpath.split(os.sep)
        for exclude in exclude_dirs:
            if exclude in root_elts:
               continue
        if '__pycache__' in dirnames:
            dirnames.remove("__pycache__")

        if dirpath == package_path:
            package = []
        else:
            package = dirpath[len(package_path) + 1:].split(os.sep)
        if has_init:
            package.insert(0, package_name)

        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if ext != '.py':
                continue
            is_package = name.endswith('__init__')
            if is_package:
                mod_name = '.'.join(package)
            else:
                mod_name = '.'.join(package + [name])

            nb += 1
            absname = os.path.join(dirpath, filename)
            with open(absname, encoding='utf-8') as f:
                src = f.read()

            tree = ast.parse(src)

            if ast_unparse_working:
                src = ast.unparse(BrythonTransformer(source_path=Path(absname)).visit(tree).body)

            data = python_minifier.minify(src, preserve_lines=True)
            path_elts = package[:]
            if os.path.basename(filename) != "__init__.py":
                path_elts.append(os.path.basename(filename)[:-3])

            visitor = Visitor(package_path, package)
            visitor.visit(tree)  # todo: ez nem a transzformált fa
            imports = sorted(list(visitor.imports))

            for exc_mod_name in exclude_modules:
                if mod_name.startswith(exc_mod_name):
                    break
            else:
                if is_package:
                   VFS[mod_name] = [ext, data, imports, 1]
                else:
                    VFS[mod_name] = [ext, data, imports]

            # print("adding {} package {}".format(mod_name, is_package))

    if nb == 0:
        print("No Python file found in current directory")
    else:
        # print('{} files'.format(nb))

        output = output or StringIO()
        # output_path = output_path or os.path.join(package_path, package_name + ".brython.js")
        #with open(output_path, "w", encoding="utf-8") as out:
        output.write('__BRYTHON__.use_VFS = true;\n')
        output.write('var scripts = {}\n'.format(json.dumps(VFS)))
        output.write('__BRYTHON__.update_VFS(scripts)\n')
        output.seek(0)

        return output


if __name__ == "__main__":
    import sys
    package_name = sys.argv[1] if len(sys.argv) > 1 else ""
    src_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()

    make(package_name, src_dir)
