import sys
import gkeepapi
import re
from datetime import datetime
import urllib

def send_due_email(note):
    # link to keep note
    html = "<p><a href='" + note.url + "'>Open in Google Keep</a></p>"
    # table of list with formatting
    now = datetime.now().strftime("%Y-%m-%d")
    html += "<table border=1 style='border-collapse: collapse;'>"
    for item in note.unchecked:
        item_html = "<td>" + item.text + "</td>" #TODO remove due date from the item title
        style = ''
        match = pattern.match(item.text)
        if match:
            due = match.group(1)
            if due != "-":
                item_html += "<td>" + due + "</td>"
                if due == now:
                    # due now
                    style = 'font-weight: bold;'
                elif due < now:
                    # overdue
                    style = 'font-weight: bold; color: red;'
        else:
            # due date not set yet
            style = 'font-style: italic;'
        html += "<tr style='" + style + "'>" + item_html + "</tr>"
    html += "</table>"
    # send the email
    data = {}
    data['title'] = note.title + " items due"
    data['html'] = html
    data['action'] = 'email'
    full_url = backend_url + '?' + urllib.parse.urlencode(data)
    with urllib.request.urlopen(full_url) as response:
        bytes = response.read()
        print(str(bytes, encoding='utf-8'))

# cli args
if len(sys.argv) != 5:
    print("Expected 4 args: GOOGLE_USERNAME, GOOGLE_TOKEN, GOOGLE_KEEP_LIST_ID, GOOGLE_APPS_SCRIPT_URL")
    exit(1)

g_user = sys.argv[1]
g_token = sys.argv[2]
list_id = sys.argv[3]
backend_url = sys.argv[4]

# load note from keep
keep = gkeepapi.Keep()
keep.resume(g_user, g_token)

note = keep.get(list_id)
items = note.unchecked

# check for any items with a due date
pattern = re.compile(r"^\s*\[([^\[\]]+)\]\s*\S+.*$")

existing_due = []
for item in items:
    match = pattern.match(item.text)
    if match:
        due = match.group(1)
        if due != "-":
            # found due date
            print("Found due date " + due + " in " + item.text)
            existing_due.append(due)

# check if any are due today specifically
now = datetime.now().strftime("%Y-%m-%d") #TODO fix timezone (this currently returns yesterday before 11am?)
if now in existing_due:
    # something due today, send email via backend
    print("Sending due email")
    send_due_email(note)