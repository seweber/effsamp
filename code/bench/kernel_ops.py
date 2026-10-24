"""Static work of a svpass kernel per amplitude: floating-point instructions and shared-memory accesses.

Counts what the generated stages (`svpass.cuda.codegen._stages`) ask of a thread per amplitude of a
pass, without a GPU. Each statement ``r[i] = make_float2(re, im);`` contributes the instructions of
its two expressions: a sum of t terms of which k are products costs ``(t - 1) + k - min(k, t - 1)``
instructions (products fuse into FMAs with the additions), and a factored common magnitude
``(...) * c`` one multiplication more. Negations and copies are free (the compiler folds them into
the operands). The global load scales every amplitude (2 multiplications) and the store sums its
squared norm (2 FMAs), as `apply.cu` does.

The counts are a model of the arithmetic the compiler cannot avoid, not of the SASS it emits.
"""

from __future__ import annotations

import re

from svpass.cuda import codegen

_ASSIGN = re.compile(r"^r\[\d+\] = make_(?:float2|double2)\((.*)\);$")


def _split_top(expr: str, seps: tuple[str, ...] = (" + ", " - ")) -> list[str]:
    """Split ``expr`` at top-level separators (outside parentheses)."""
    parts, depth, start, i = [], 0, 0, 0
    while i < len(expr):
        ch = expr[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif depth == 0:
            for sep in seps:
                if expr.startswith(sep, i):
                    parts.append(expr[start:i])
                    start = i + len(sep)
                    i += len(sep) - 1
                    break
        i += 1
    parts.append(expr[start:])
    return parts


def _expr_ops(expr: str) -> int:
    """Return the instructions of one real expression, see the module docstring."""
    expr = expr.strip()
    extra = 0
    # A factored common magnitude: "(sum) * literal".
    m = re.match(r"^\((.*)\) \* [-+0-9.eE]+f?$", expr)
    if m and _balanced(m.group(1)):
        expr, extra = m.group(1), 1
    terms = _split_top(expr)
    t = len(terms)
    k = sum(1 for term in terms if "*" in _strip_parens(term))
    return (t - 1) + k - min(k, t - 1) + extra


def _strip_parens(term: str) -> str:
    term = term.strip()
    while term.startswith("(") and term.endswith(")") and _balanced(term[1:-1]):
        term = term[1:-1].strip()
    return term


def _balanced(s: str) -> bool:
    depth = 0
    for ch in s:
        depth += ch == "("
        depth -= ch == ")"
        if depth < 0:
            return False
    return depth == 0


def statement_ops(line: str) -> int:
    """Return the instructions of the register assignments ``r[i] = make_float2(re, im)`` in one generated line."""
    total = 0
    for m in re.finditer(r"r\[\d+\] = make_(?:float2|double2)\(", line):
        start = m.end()
        depth, i = 1, start
        while depth:
            depth += {"(": 1, ")": -1}.get(line[i], 0)
            i += 1
        re_part, im_part = _split_top(line[start : i - 1], (", ",))[:2]
        total += _expr_ops(re_part) + _expr_ops(im_part)
    return total


def stage_ops(lines: list[str]) -> int:
    """Return the instructions of a stage's statements (one switch case counted, the first)."""
    total, in_switch, case_seen = 0, False, False
    for line in lines:
        s = line.strip()
        if s.startswith("switch"):
            in_switch, case_seen = True, False
            continue
        if in_switch and s.startswith("case "):
            if case_seen:
                in_switch = "skip"
            case_seen = True
            continue
        if in_switch == "skip":
            if s == "}" and not line.startswith(" "):
                in_switch = False
            continue
        total += statement_ops(line)
    return total


def block_work(block, config) -> dict:
    """Return the instructions and shared accesses per amplitude of the block's kernel, and its stages."""
    stages = codegen._stages(block, config)
    r = codegen.stage_width(config, len(block.tile(config)))
    ops = sum(stage_ops(stage.statements) for stage in stages) / (1 << r)
    shared = codegen.shared_accesses(block, config)
    return {
        "fp_ops": ops + 4,  # + scaling on load and the norm on store
        "shared": shared,
        "stages": len(stages),
        "operations": block.n_operations,
    }
