import sys
# import gkeepapi

if len(sys.argv) != 5:
    print("Expected 4 args: GOOGLE_USERNAME, GOOGLE_TOKEN, GOOGLE_KEEP_LIST_ID, GOOGLE_APPS_SCRIPT_URL")
    exit(1)

# f = open("/gkeep_config/user.txt", "r")
# g_user = f.read()
# f.close()

# f = open("/gkeep_config/token.txt", "r")
# g_token = f.read()
# f.close()

# keep = gkeepapi.Keep()
# keep.resume(g_user, g_token)

print("Notify stub")