import Query_Parser

from Transaction_Manager import Transaction_Manager


def main(input_file_path):
    # print("Hello World!")
    trans_mgr = Transaction_Manager()
    cmmd_waitlist = []
    input_path = input_file_path
    exe_result, in_waitlist = False, False
    waitlist_idx = 0

    # try:
    file_read = open(input_path, "r")
    print("file loaded")
    while True:

        fetched = None
        in_waitlist = False

        if len(cmmd_waitlist) > 0 and waitlist_idx < len(cmmd_waitlist):
            print("waitlist_idx %d", waitlist_idx)
            fetched = cmmd_waitlist[waitlist_idx]
            in_waitlist = True
        else:

            qry = file_read.readline()
            if len(qry)==0:
                break
            if '//' in qry:
                qry = qry[:qry.index('//')]
            if qry is not None and qry != '\n' and qry.strip() != "":

                fetched = Query_Parser.parse_query(qry)
            else:
                # break
                continue

        if fetched[0] == 'begin':
            exe_result = trans_mgr.begin(int(fetched[1]))
        elif fetched[0] == 'beginRO':
            exe_result = trans_mgr.begin_read_only(int(fetched[1]))
        elif fetched[0] == 'R':
            exe_result = trans_mgr.read(int(fetched[1]), int(fetched[2]))
        elif fetched[0] == 'W':
            exe_result = trans_mgr.write(int(fetched[1]), int(fetched[2]), int(fetched[3]))
        elif fetched[0] == 'recover':
            exe_result = trans_mgr.recover(int(fetched[1]))
        elif fetched[0] == 'fail':
            exe_result = trans_mgr.fail(int(fetched[1]))
        elif fetched[0] == 'dump':
            exe_result = trans_mgr.dump()
        elif fetched[0] == 'end':
            exe_result = trans_mgr.end(int(fetched[1]))

        if exe_result == True:
            if in_waitlist == True:
                cmmd_waitlist.remove(waitlist_idx)
            waitlist_idx = 0
        else:
            if in_waitlist == False:
                cmmd_waitlist.append(fetched)
                waitlist_idx = 0
            else:
                waitlist_idx += 1
        trans_mgr.time_stamp += 1
        trans_mgr.dead_lock_detect()



    # except:
    #     print("Something went wrong")
    # finally:
    #     print("The 'try except' is finished")


if __name__ == "__main__":
    main("testcases.txt")
    # t=Transaction_Manager()
    # print(t(1,2,102))