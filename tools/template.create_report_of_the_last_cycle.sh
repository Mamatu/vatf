#/bin/bash
find ${WORKSPACE_PATH} -name status -type f | sed "s|\(test_.*\)\/session.*|\1|g" | uniq -c | awk '{print "(" $2 ", number of sessions: " $1 ")";system("cat " $2"/$(ls " $2 "| tail -n +" $1 ")/status/status")}'
