import code
import sys


def _exec_function(ast, globals_map):
    locals_map = globals_map
    exec(ast, globals_map, locals_map)
    return locals_map


def execute_content(name, content):
    try:
        ast = compile(content, name, "exec", flags=0, dont_inherit=1)
    except SyntaxError:
        raise RuntimeError(
            "Unable to parse {}. Is it a Python script? Syntax correct?".format(name)
        )

    old_name, old_file = globals().get("__name__"), globals().get("__file__")

    try:
        globals()["__name__"] = "__main__"
        globals()["__file__"] = name
        _exec_function(ast, globals())
    finally:
        if old_name:
            globals()["__name__"] = old_name
        else:
            globals().pop("__name__")
        if old_file:
            globals()["__file__"] = old_file
        else:
            globals().pop("__file__")


def execute_interpreter():
    if sys.argv[1:]:
        try:
            with open(sys.argv[1]) as fp:
                name, content = sys.argv[1], fp.read()
        except (FileNotFoundError, IsADirectoryError, PermissionError) as e:
            raise RuntimeError(
                "Could not open {} in the environment [{}]: {}".format(
                    sys.argv[1], sys.argv[0], e
                )
            )

        sys.argv = sys.argv[1:]
        execute_content(name, content)
    else:
        code.interact()
