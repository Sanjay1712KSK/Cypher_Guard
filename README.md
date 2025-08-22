
# Drop your 7 Python files here

- Put your existing `.py` modules into this folder.
- They will be auto-discovered by the Toolbox page.
- Public functions (not starting with `_`) will be listed for execution.
- Function parameters will be shown as simple text fields; values are parsed with `ast.literal_eval` when possible.

## Tips
- Add type hints and sensible defaults to function signatures for better UI.
- Keep side effects obvious (print/log) so outputs are visible.
