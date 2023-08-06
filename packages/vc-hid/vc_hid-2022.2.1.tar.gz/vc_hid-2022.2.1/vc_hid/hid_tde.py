

#from vc_hid import vc_hid as hid
import vc_hid  
vid="046D"
pid="89a"
pid1="867"
setID="28"
readID="29"
controlID=1
readnumber=20


if(__name__)=="__main__":
    anotherCMD=[0,0,0,0]
    test = vc_hid.HID_class()

    passflag,data=test.hidset(pid,setID,controlID,readnumber,anotherCMD)
    print(passflag,data)

    
    passflag,data=test.readhid(pid,readID,controlID,readnumber)  
    print(passflag,data)
   

    passflag,data=test.hidset_vpid(vid,pid,setID,controlID,readnumber,anotherCMD)
    print(passflag,data)

    
    passflag,data=test.readhid_vpid(vid,pid,readID,controlID,readnumber)  
    print(passflag,data)


    passflag,data=test.readhid_vpid_all(vid,pid,readID,readnumber)  
    print(passflag,data)



