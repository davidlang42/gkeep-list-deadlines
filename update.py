import sys
import gkeepapi

if len(sys.argv) != 4:
    print("Expected 3 args: GOOGLE_USERNAME, GOOGLE_TOKEN, GOOGLE_KEEP_LIST_ID")
    exit(1)

g_user = sys.argv[1]
g_token = sys.argv[2]
list_id = sys.argv[3]

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