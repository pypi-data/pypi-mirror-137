import os
USER_HOME=os.path.expanduser('~')

line0 = "import fire\n"
lineN = "\nfire.Fire()"

def inject_fire(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(line0 + content + lineN)


def remove_fire(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content.startswith(line0)
    assert content.endswith(lineN)
    content = content[len(line0):-len(lineN)]
    with open(path, 'w', encoding='utf-8') as f:
        f.write("".join(content))

