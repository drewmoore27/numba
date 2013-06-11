# -*- coding: utf-8 -*-

"""
Pretty printing of numba IRs.
"""

from __future__ import print_function, division, absolute_import

import os
import sys

from numba.viz import cfgviz, astviz
from numba.annotate.annotate import (Source, Program, render_text,
                                     render_webpage, build_linemap)

# ______________________________________________________________________

def dumppass(option):
    def decorator(f):
        def wrapper(ast, env):
            if env.cmdopts.get(option):
                f(ast, env, env.cmdopts.get("fancy"))
            return ast
        return wrapper
    return decorator

# ______________________________________________________________________

@dumppass("dump-ast")
def dump_ast(ast, env, fancy):
    if fancy:
        astviz.render_ast(ast, os.path.expanduser("~/ast.dot"))
    else:
        import ast as ast_module
        print(ast_module.dump(ast))

@dumppass("dump-cfg")
def dump_cfg(ast, env, fancy):
    cfg = env.crnt.flow
    if fancy:
        cfgviz.render_cfg(cfg, os.path.expanduser("~/cfg.dot"))
    else:
        for block in cfg.blocks:
            print(block)
            print("    ", block.parents)
            print("    ", block.children)

@dumppass("annotate")
def dump_annotations(ast, env, fancy):
    p = Program(Source(build_linemap(env.crnt.func), env.crnt.annotations),
                env.crnt.intermediates)
    render = render_webpage if fancy else render_text
    render(p, emit=sys.stdout.write, intermediate_names=["llvm"])

@dumppass("dump-llvm")
def dump_llvm(ast, env, fancy):
    print(env.crnt.lfunc)

@dumppass("dump-optimized")
def dump_optimized(ast, env, fancy):
    print(env.crnt.lfunc)