import sys
import gkeepapi
import re
import urllib.request
import urllib.parse

if len(sys.argv) != 5:
    print("Expected 4 args: GOOGLE_USERNAME, GOOGLE_TOKEN, GOOGLE_KEEP_LIST_ID, GOOGLE_APPS_SCRIPT_URL")
    exit(1)

g_user = sys.argv[1]
g_token = sys.argv[2]
list_id = sys.argv[3]
backend_url = sys.argv[4]

keep = gkeepapi.Keep()
keep.resume(g_user, g_token)

note = keep.get(list_id)

items = note.unchecked

pattern = re.compile(r"^\s*\[([^\[\]]+)\]\s*\S+.*$")

for item in items:
    match = pattern.match(item.text)
    if not match:
        print("Requesting due date for: " + item.text)
        data = {}
        data['item'] = item.text
        data['action'] = 'lookup'
        data['list_title'] = note.title
        full_url = backend_url + '?' + urllib.parse.urlencode(data)
        with urllib.request.urlopen(full_url) as response:
            bytes = response.read()
            due = str(bytes, encoding='utf-8')
            if due:
                item.text = '[' + due + '] ' + item.text
                print("Set due date: " + due)
            else:
                print("Due date unknown")

note.sort_items() #TODO make sort actually work

keep.sync()