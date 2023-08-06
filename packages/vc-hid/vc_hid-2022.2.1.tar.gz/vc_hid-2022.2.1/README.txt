#Copyright (c) 2021 lorry_rui  
#//////////usage://///////////////  
#for HID use  
#/////////////////////////////////////////  
#VC_tde USE only  @ logitech , Lorry RUi  
https://pypi.org/project/vc-hid  
https://github.com/Lorrytoolcenter/VC-HID.git  

Sample code:  
from vc_hid import vc_hid as hid  
vid="046D" ## this Logi vid
pid="89a"  ## this is logi Rally bar PID  
pid1="867"  ## this is Logi meetup PID  
mousepid="c332"
setID="28"
readID="29"
LED=""
mousebutton="a"
controlID=20
readnumber=20

test = hid.HID_class()




if(__name__)=="__main__":
    anotherCMD=[0,0,0,0]
    
    passflag,data=test.hidset(pid1,setID,controlID,readnumber,anotherCMD)
    print(passflag,data)

    
    passflag,data=test.readhid(pid1,readID,controlID,readnumber)  
    print(passflag,data)

    passflag,data=test.hidset_vpid(vid,pid,setID,controlID,readnumber,anotherCMD)
    print(passflag,data)

    
    passflag,data=test.readhid_vpid(vid,pid,readID,controlID,readnumber)  
    print(passflag,data)

    passflag,data=test.readhid_vpid_all(vid,pid,readID,readnumber)  
    print(passflag,data)
