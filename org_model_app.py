File "/mount/src/restructure/org_model_app.py", line 57, in <module>
    dot.attr(graph={"fontsize": "24"})
File "/home/adminuser/venv/lib/python3.12/site-packages/graphviz/_tools.py", line 171, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/graphviz/dot.py", line 274, in attr
    a_list = self._a_list(None, kwargs=attrs, attributes=_attributes)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/graphviz/_tools.py", line 171, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/graphviz/quoting.py", line 125, in a_list
    result += [f'{quote(k)}={quote(v)}'
                             ^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/graphviz/_tools.py", line 171, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/graphviz/quoting.py", line 82, in quote
    if is_html_string(identifier) and not isinstance(identifier, NoHtml):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^