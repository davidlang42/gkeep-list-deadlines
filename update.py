import sys
import gkeepapi
import re
import urllib.request
import urllib.parse
from datetime import datetime

def send_due_email(note):
    # link to keep note
    html = "<p><a href='" + note.url + "'>Open in Google Keep</a></p>"
    # table of list with formatting
    now = datetime.now().strftime("%Y-%m-%d")
    html += "<table border=1 style='border-collapse: collapse;'>"
    for item in note.unchecked:
        style = ''
        match = pattern.match(item.text)
        if match:
            item_html = "<td>" + match.group(2) + "</td>"
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
            item_html = "<td>" + item.text + "</td>"
            style = 'font-style: italic;'
        html += "<tr style='" + style + "'>" + item_html + "</tr>"
    html += "</table>"
    # send the email
    data = {}
    data['title'] = note.title + " DUE"
    data['html'] = html
    data['action'] = 'email'
    full_url = backend_url + '?' + urllib.parse.urlencode(data)
    with urllib.request.urlopen(full_url) as response:
        bytes = response.read()
        print(str(bytes, encoding='utf-8'))

def due_then_name(item):
    match = pattern.match(item.text)
    if match:
        due = match.group(1)
        if due != "-":
            return "a " + due.lower() + " " + match.group(2).lower()
        else:
            return "b " + match.group(2).lower()
    else:
        return "c " + item.text.lower()

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

# check for any items without a due date
pattern = re.compile(r"^\s*\[([^\[\]]+)\]\s*(\S+.*)$")

new_due = []
for item in items:
    match = pattern.match(item.text)
    if not match:
        # request due date for this item from backend
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
                # received due date
                item.text = '[' + due + '] ' + item.text
                print("Set due date: " + due)
                if due != "-":
                    new_due.append(due)
            else:
                # due date not known yet
                print("Due date unknown")

# save changes to keep note
note.sort_items(key=due_then_name)
keep.sync()

# check if any new due dates are already due
now = datetime.now().strftime("%Y-%m-%d")
if any(due <= now for due in new_due):
    # something we just set is due already, we should notify immediately
    print("Sending due email")
    send_due_email(note)