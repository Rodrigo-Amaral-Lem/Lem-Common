#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Part of LEM. See the accompanying LICENSE for license terms and warranty disclaimer.

# Legacy audit CLI: BASELINE_ZIP --source MATCHING_RECONSTRUCTED_TREE; requires Pygments.
# Read-only comparison for comment/format-only edits, not functional release changes.
# The default source root is Common, which is not the old monorepository; always pass --source here.
# See docs/maintenance.md for scope and limitations.

"""Compare a documented source tree with its original release ZIP.

This is a review aid, not a compiler or proof of runtime equivalence. Python
compares ASTs, C++/Java compare lexical tokens, and QML permits only formatter
semicolon changes and movement of an id within the same brace scope. Run the
real application tests as well. Requires Pygments; no runtime app dependency.
"""

import argparse
import ast
from pathlib import Path
import re
from zipfile import ZipFile

from pygments import lex
from pygments.lexers import CppLexer, JavaLexer, JavascriptLexer
from pygments.token import Comment, Number, Text


def lexical_tokens(source, lexer):
    result = []
    for kind, value in lex(source, lexer):
        if not value or kind in Comment or (kind in Text and value.isspace()):
            continue
        # Pygments can lex x-1 as one signed-number token before formatting,
        # but x - 1 as an operator and a number afterwards. Compare punctuation.
        if kind in Number and len(value) > 1 and value[0] in "+-":
            result.extend((value[0], value[1:]))
        else:
            result.append(value)
    return result


def qml_structure(source):
    # QML's id binding has no evaluation order. qmlformat moves it to the top
    # of the object even without --normalize; retain its exact brace-scope ID.
    tokens = [t for t in lexical_tokens(source, JavascriptLexer()) if t != ";"]
    structure, ids, scopes = [], [], []
    next_scope = 0
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if (
            token == "id"
            and tokens[index + 1 : index + 2] == [":"]
            and index + 2 < len(tokens)
            and re.fullmatch(r"[A-Za-z_$][\w$]*", tokens[index + 2])
        ):
            ids.append((tuple(scopes), tokens[index + 2]))
            index += 3
            continue
        if token == "{":
            next_scope += 1
            scopes.append(next_scope)
        elif token == "}":
            scopes.pop()
        structure.append(token)
        index += 1
    return structure, ids


def equivalent(before, after, suffix):
    if suffix == ".py":
        return ast.dump(ast.parse(before)) == ast.dump(ast.parse(after))
    if suffix == ".qml":
        return qml_structure(before) == qml_structure(after)
    lexer = JavaLexer() if suffix == ".java" else CppLexer()
    return lexical_tokens(before, lexer) == lexical_tokens(after, lexer)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline_zip", type=Path)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    checked = 0
    failures = []
    with ZipFile(args.baseline_zip) as archive:
        for entry in archive.infolist():
            relative = Path(*Path(entry.filename).parts[1:])
            if entry.is_dir() or relative.suffix not in {".py", ".cpp", ".h", ".java", ".qml"}:
                continue
            target = args.source / relative
            if not target.is_file():
                failures.append(str(relative) + " (missing)")
                continue
            before = archive.read(entry).decode("utf-8-sig")
            after = target.read_text(encoding="utf-8-sig")
            if not equivalent(before, after, relative.suffix):
                failures.append(str(relative))
            checked += 1
    if failures:
        raise SystemExit("Executable structure differs: " + ", ".join(failures))
    print(f"PASS: {checked} existing Python/C++/Java/QML files retain their executable structure.")
    print(
        "QML comparison permits formatter semicolons and same-scope id placement; run UI tests too."
    )


if __name__ == "__main__":
    main()
