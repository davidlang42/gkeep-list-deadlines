import sys
# import gkeepapi

if len(sys.argv) != 4:
    print("Expected 3 args: GOOGLE_USERNAME, GOOGLE_TOKEN, GOOGLE_KEEP_LIST_ID")
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