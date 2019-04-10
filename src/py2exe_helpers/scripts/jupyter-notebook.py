from __future__ import absolute_import, print_function, unicode_literals
import sys
import path_helpers as ph

sys.path.insert(0, ph.path(sys.argv[0]).parent)

# Required packages for `pkg_resources`
import pkg_resources

import path_helpers

import cycler
import matplotlib as mpl
import matplotlib.backends
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot
import numpy as np
import pandas as pd
import FileDialog
import IPython
import IPython.terminal.embed
import IPython.core.magic
import IPython.core.oinspect
import pandas._libs
import pandas._libs.tslibs.timedeltas

import zmq
import zmq.auth.base
import zmq.auth.certs
import zmq.auth.ioloop
import zmq.auth.thread
import zmq.backend.select
import zmq.backend.cython

import jinja2.ext

import notebook.auth.login
import notebook.auth.logout
import notebook.auth.security
import notebook.base.handlers
import notebook.base.zmqhandlers
import notebook.bundler.bundlerextensions
import notebook.bundler.handlers
import notebook.bundler.tarball_bundler
import notebook.bundler.tools
import notebook.bundler.zip_bundler
import notebook.edit.handlers
import notebook.files.handlers
import notebook.kernelspecs.handlers
import notebook.nbconvert.handlers
import notebook.notebook.handlers
import notebook.services.shutdown
import notebook.services.api.handlers
import notebook.services.config.handlers
import notebook.services.config.manager
import notebook.services.contents.checkpoints
import notebook.services.contents.filecheckpoints
import notebook.services.contents.fileio
import notebook.services.contents.handlers
import notebook.services.kernels.handlers
import notebook.services.kernels.kernelmanager
import notebook.services.kernelspecs.handlers
import notebook.services.nbconvert.handlers
import notebook.services.security.handlers
import notebook.services.sessions.handlers
import notebook.services.sessions.sessionmanager
import notebook.tree.handlers
import notebook.view.handlers

import pygments.formatters.bbcode
import pygments.formatters.html
import pygments.formatters.img
import pygments.formatters.irc
import pygments.formatters.latex
import pygments.formatters.other
import pygments.formatters.rtf
import pygments.formatters.svg
import pygments.formatters.terminal
import pygments.formatters.terminal256
import pygments.formatters._mapping
import pygments.lexers.actionscript
import pygments.lexers.agile
import pygments.lexers.algebra
import pygments.lexers.ambient
import pygments.lexers.ampl
import pygments.lexers.apl
import pygments.lexers.archetype
import pygments.lexers.asm
import pygments.lexers.automation
import pygments.lexers.basic
import pygments.lexers.bibtex
import pygments.lexers.business
import pygments.lexers.capnproto
import pygments.lexers.chapel
import pygments.lexers.clean
import pygments.lexers.compiled
import pygments.lexers.configs
import pygments.lexers.console
import pygments.lexers.crystal
import pygments.lexers.csound
import pygments.lexers.css
import pygments.lexers.c_cpp
import pygments.lexers.c_like
import pygments.lexers.d
import pygments.lexers.dalvik
import pygments.lexers.data
import pygments.lexers.diff
import pygments.lexers.dotnet
import pygments.lexers.dsls
import pygments.lexers.dylan
import pygments.lexers.ecl
import pygments.lexers.eiffel
import pygments.lexers.elm
import pygments.lexers.erlang
import pygments.lexers.esoteric
import pygments.lexers.ezhil
import pygments.lexers.factor
import pygments.lexers.fantom
import pygments.lexers.felix
import pygments.lexers.forth
import pygments.lexers.fortran
import pygments.lexers.foxpro
import pygments.lexers.functional
import pygments.lexers.go
import pygments.lexers.grammar_notation
import pygments.lexers.graph
import pygments.lexers.graphics
import pygments.lexers.haskell
import pygments.lexers.haxe
import pygments.lexers.hdl
import pygments.lexers.hexdump
import pygments.lexers.html
import pygments.lexers.idl
import pygments.lexers.igor
import pygments.lexers.inferno
import pygments.lexers.installers
import pygments.lexers.int_fiction
import pygments.lexers.iolang
import pygments.lexers.j
import pygments.lexers.javascript
import pygments.lexers.julia
import pygments.lexers.jvm
import pygments.lexers.lisp
import pygments.lexers.make
import pygments.lexers.markup
import pygments.lexers.math
import pygments.lexers.matlab
import pygments.lexers.ml
import pygments.lexers.modeling
import pygments.lexers.modula2
import pygments.lexers.monte
import pygments.lexers.ncl
import pygments.lexers.nimrod
import pygments.lexers.nit
import pygments.lexers.nix
import pygments.lexers.oberon
import pygments.lexers.objective
import pygments.lexers.ooc
import pygments.lexers.other
import pygments.lexers.parasail
import pygments.lexers.parsers
import pygments.lexers.pascal
import pygments.lexers.pawn
import pygments.lexers.perl
import pygments.lexers.php
import pygments.lexers.praat
import pygments.lexers.prolog
import pygments.lexers.python
import pygments.lexers.qvt
import pygments.lexers.r
import pygments.lexers.rdf
import pygments.lexers.rebol
import pygments.lexers.resource
import pygments.lexers.rnc
import pygments.lexers.roboconf
import pygments.lexers.robotframework
import pygments.lexers.ruby
import pygments.lexers.rust
import pygments.lexers.sas
import pygments.lexers.scripting
import pygments.lexers.shell
import pygments.lexers.smalltalk
import pygments.lexers.smv
import pygments.lexers.snobol
import pygments.lexers.special
import pygments.lexers.sql
import pygments.lexers.stata
import pygments.lexers.supercollider
import pygments.lexers.tcl
import pygments.lexers.templates
import pygments.lexers.testing
import pygments.lexers.text
import pygments.lexers.textedit
import pygments.lexers.textfmts
import pygments.lexers.theorem
import pygments.lexers.trafficscript
import pygments.lexers.typoscript
import pygments.lexers.urbi
import pygments.lexers.varnish
import pygments.lexers.verification
import pygments.lexers.web
import pygments.lexers.webmisc
import pygments.lexers.whiley
import pygments.lexers.x10
import pygments.lexers._asy_builtins
import pygments.lexers._cl_builtins
import pygments.lexers._cocoa_builtins
import pygments.lexers._csound_builtins
import pygments.lexers._lasso_builtins
import pygments.lexers._lua_builtins
import pygments.lexers._mapping
import pygments.lexers._mql_builtins
import pygments.lexers._openedge_builtins
import pygments.lexers._php_builtins
import pygments.lexers._postgres_builtins
import pygments.lexers._scilab_builtins
import pygments.lexers._sourcemod_builtins
import pygments.lexers._stan_builtins
import pygments.lexers._stata_builtins
import pygments.lexers._tsql_builtins
import pygments.lexers._vim_builtins
import pygments.styles.abap
import pygments.styles.algol
import pygments.styles.algol_nu
import pygments.styles.arduino
import pygments.styles.autumn
import pygments.styles.borland
import pygments.styles.bw
import pygments.styles.colorful
import pygments.styles.default
import pygments.styles.emacs
import pygments.styles.friendly
import pygments.styles.fruity
import pygments.styles.igor
import pygments.styles.lovelace
import pygments.styles.manni
import pygments.styles.monokai
import pygments.styles.murphy
import pygments.styles.native
import pygments.styles.paraiso_dark
import pygments.styles.paraiso_light
import pygments.styles.pastie
import pygments.styles.perldoc
import pygments.styles.rainbow_dash
import pygments.styles.rrt
import pygments.styles.sas
import pygments.styles.stata
import pygments.styles.tango
import pygments.styles.trac
import pygments.styles.vim
import pygments.styles.vs
import pygments.styles.xcode

import multiprocessing

import sys
import jupyter
import notebook.notebookapp
import nbformat
import ipywidgets

import traitlets.config.application
import traitlets.config.configurable
import traitlets.config.loader
import traitlets.config.manager
import traitlets.utils.bunch
import traitlets.utils.getargspec
import traitlets.utils.importstring
import traitlets.utils.sentinel

from ipykernel import kernelapp
import ipykernel.datapub

import notebook
for i, v in enumerate(notebook.DEFAULT_TEMPLATE_PATH_LIST):
    notebook.DEFAULT_TEMPLATE_PATH_LIST[i] = v.replace('library.zip\\', '')
print(notebook.DEFAULT_TEMPLATE_PATH_LIST)
notebook.DEFAULT_STATIC_FILES_PATH = notebook.DEFAULT_STATIC_FILES_PATH.replace('library.zip\\', '')
print(notebook.DEFAULT_STATIC_FILES_PATH)

if __name__ == '__main__':
    multiprocessing.freeze_support()

    if 'ipykernel_launcher' in sys.argv:
        # Remove the CWD from sys.path while we load stuff.
        # This is added back by InteractiveShellApp.init_path()
        if sys.path[0] == '':
            del sys.path[0]

        kernelapp.launch_new_instance()
    else:
        sys.exit(notebook.notebookapp
                 .main(extra_static_paths=[notebook.DEFAULT_STATIC_FILES_PATH
                                           .replace('library.zip\\', '')]))
