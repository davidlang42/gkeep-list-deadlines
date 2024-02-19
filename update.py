import sys
import gkeepapi

if len(sys.argv) != 5:
    print("Expected 4 args: GOOGLE_USERNAME, GOOGLE_TOKEN, GOOGLE_KEEP_LIST_ID, GOOGLE_APPS_SCRIPT_URL")
    exit(1)

g_user = sys.argv[1]
g_token = sys.argv[2]
list_id = sys.argv[3]
backend_url = sys.arv[4]

keep = gkeepapi.Keep()
keep.resume(g_user, g_token)

note = keep.get(list_id)

print(note.title)
print("^^^^^^^^^^^^^^")
print(note.text)

# note = keep.createNote('Todo', 'Eat breakfast')
# note.pinned = True
# note.color = gkeepapi.node.ColorValue.Red

# keep.sync()