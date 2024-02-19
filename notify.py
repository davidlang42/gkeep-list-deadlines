import sys
import gkeepapi
import re

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
    if match:
        print(item.text + ": " + match.group(1))
        #TODO check if any are due, if so trigger due email with list and google keep link