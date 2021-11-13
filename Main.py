import Data_Manager
import Lock
import Query_Parser
import Site
import Transaction
import Transaction_Manager
import Variable


def main(input_file_path):

    # print("Hello World!")
    trans_mgr=Transaction_Manager()
    cmmd_waitlist=[]
    input_path=input_file_path
    exe_result, in_waitlist=False,False
    waitlist_idx=0
    

    try:
        file_read= open(input_path,"r")
        while True:

            fetched=None
            in_waitlist=False

            if (len(cmmd_waitlist)>0 and waitlist_idx< len(cmmd_waitlist)):
                print("waitlist_idx %d",waitlist_idx)
                fetched=cmmd_waitlist[waitlist_idx]
                in_waitlist=True
            else:
                qry=file_read.readline()
                if qry!=None:
                    fetched=Query_Parser.parse_query(fetched)
                else:
                    break
            
            if (fetched[0]=='begin'):
                pass
            elif (fetched[0]==''):
                pass
            elif (fetched[0]==''):
                pass
            elif (fetched[0]==''):
                pass
            elif (fetched[0]==''):
                pass
            elif (fetched[0]==''):
                pass
            elif (fetched[0]==''):
                pass
            elif (fetched[0]==''):
                pass
    except:
        print("Something went wrong")
    finally:
        print("The 'try except' is finished")


    



if __name__ == "__main__":
    main()

