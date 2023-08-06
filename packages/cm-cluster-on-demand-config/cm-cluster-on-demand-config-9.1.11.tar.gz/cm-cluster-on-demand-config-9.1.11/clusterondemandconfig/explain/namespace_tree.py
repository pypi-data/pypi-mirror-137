# Copyright 2004-2022 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from collections import defaultdict
from contextlib import contextmanager

from six import StringIO


def generate_namespace_tree(parameters):
    tree = _construct_namespace_tree(parameters)

    buffer = StringIO()
    with capture_stdout(buffer):
        _print_namespace_tree(tree)
    return buffer.getvalue().strip()


def _construct_namespace_tree(parameters):
    tree = defaultdict(set)

    for parameter in parameters:
        parent = f"{parameter.namespaces[0]}:{parameter.name}"
        tree["root"].add(parent)

        for namespace in parameter.namespaces[1:]:
            child = f"{namespace}:{parameter.name}"
            tree[parent].add(child)
            parent = child

        tree[parent] = parameter.command
    return tree


def _print_namespace_tree(tree):
    def __print_subtree(node, prefix, last):
        if prefix and last:
            box_art = "└─"
        elif prefix:
            box_art = "├─"
        else:
            box_art = "─"

        if node in tree and isinstance(tree[node], str):
            print(f"{prefix}{box_art}[{node}]\t(command: {tree[node]})")
            return
        elif node not in tree:
            print(f"{prefix}{box_art}[{node}]")
            return

        print(f"{prefix}{box_art}[{node}]")

        children = sorted(tree[node])
        for node in children[:-1]:
            __print_subtree(node, prefix=prefix + ("   " if last else "│  "), last=False)
        __print_subtree(children[-1], prefix=prefix + ("   " if last else "│  "), last=True)

    for root in sorted(tree["root"]):
        __print_subtree(root, "", True)


@contextmanager
def capture_stdout(buffer):
    sys.stdout, old_stdout = buffer, sys.stdout
    try:
        yield
    finally:
        sys.stdout = old_stdout
