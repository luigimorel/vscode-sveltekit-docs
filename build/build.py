import re
import json
from os.path import abspath, join, dirname
import urllib.request

# Create a request with a valid User-Agent
req = urllib.request.Request(
    'https://kit.svelte.dev/docs',
    data= None,
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) ' +
        'AppleWebKit/537.36 (KHTML, like Gecko) ' +
        'Chrome/112.0.0.0 Safari/537.36'
    }
)

# Find all the /docs links
docs = urllib.request.urlopen(req)
links = re.findall('href="(/docs/.*?)"', docs.read().decode('utf-8'))
print(links)

found = []
pages = []

# Compile all page info
for url in sorted(set(links)):
    topic = url.split('/')[2].title().replace('-', ' ').split('#')[0]
    slug = url.split('/')[2].split('#')[0]

    if (topic not in found):
        found.append(topic)
        pages.append({
            "topic": topic,
            "slug": slug,
            "command": "svelteKitDocs" + slug.replace('-', ' ').title().replace(' ', '')
        })

# Generate command definitions in package.json
with open(join(abspath(dirname(__file__)), '../package.json'), 'r') as f:
    data = json.load(f)
    data['contributes']['commands'] = []
    data['activationEvents'] = []

    for page in pages:
        data['activationEvents'].append(
            "onCommand:extension." + page['command'])
        data['contributes']['commands'].append({
            "command": "extension.{}".format(page['command']),
            "category": "SvelteKit Docs",
            "title": page['topic'],
        })

with open(join(abspath(dirname(__file__)), '../package.json'), 'w') as f:
    json.dump(data, f, indent=4)

# Generate the extension.ts file
with open(join(abspath(dirname(__file__)), '../src/extension.ts'), 'w+') as f:
    f.write("'use strict';\n")
    f.write("import * as vscode from 'vscode';\n\n")
    f.write("export function activate(context: vscode.ExtensionContext) {\n\n")

    for page in pages:
        f.write(
            '    let ' + page['command'] + ' = ' +
            'vscode.commands.registerCommand('
            + "'extension." + page['command'] + "', () => {\n"
            + "        vscode.commands.executeCommand('vscode.open', "
            + "vscode.Uri.parse('https://kit.svelte.dev/docs/s" + page['slug']
            + "'));\n"
            + "    });\n"
            + "    context.subscriptions.push(" + page['command'] + ");\n"
        )

    f.write("\n}")

print('Extension files have been built.')
