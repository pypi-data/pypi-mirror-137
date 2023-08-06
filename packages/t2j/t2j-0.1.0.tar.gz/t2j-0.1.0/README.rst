===
t2j
===

t2j converts TOML input to JSON output and vice versa.

Usage
=====

Feed the TOML contents via standard input::

    cat pyproject.toml | t2j | jq -r '.project.dependencies[]'

Specifying the filename has the same effect::

    t2j pyproject.toml | jq -r '.project.dependencies[]'

Reverse Direction (JSON-to-TOML)
--------------------------------

Invoke as ``j2t`` option for reverse (JSON-to-TOML) conversion::

    t2j pyproject.toml | j2t

Note:

1. The JSON input must be a mapping (JSON object).
2. Round-trip formatting is not preserved, e.g. keys and tables may be
   reordered, comments are dropped, etc.

Conversion direction may also be given as ``-J``/``--json-to-toml`` or
``-T``/``--toml-to-json``.  These options override the direction implied by the
command name, e.g. ``t2j -J`` is the same as ``j2t``.