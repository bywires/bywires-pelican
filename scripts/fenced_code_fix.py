import re, sys, glob

def fix(match):
    return "```{lang}\n{code}\n```\n\n".format(
        lang=match.group('lang'),
        code=re.sub('(?<=\n)( {4}|\t)', '', match.group('code'))
    )

def replace(text):
    return re.sub(
        "<div class=\"code (?P<lang>\w+)\" markdown=\"1\">\s*?\n\s*(?:<\?(?:php)?)?\s*(?P<code>.*?)\s*<\/div>\s*", 
        fix, 
        text, 
        flags=re.MULTILINE | re.DOTALL
    )

def replace_file(path):
    with open(path, 'rb') as f:
        data = replace(f.read())

    with open(path, 'wb') as f:
        f.write(data)

for path in glob.glob(sys.argv[1]):
    print path
    replace_file(path)
