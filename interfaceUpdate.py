# $language = "python"
# $interface = "1.0"
#

# Author: Ethan Park
# Date: 4/6/2020
# This script reads csv file and updates interface name

import csv

def main():

    # Set Synchronous to True so that we don't miss any data
    crt.Screen.Synchronous=True

    IP_Address = []
    interface = []
    description = []
    packData = []
    

    # CSV file open
    #
    with open('interface.csv', 'r') as data:
        data_reader = csv.reader(data)
        next(data_reader)

        for row in data_reader:
            IP_Address.append(row[0])
            interface.append(row[1])
            description.append(row[2])
        
        i = 0
        while i < len(IP_Address):
            cnt = IP_Address.count(IP_Address[i])
            ip_desc = {}

            j = 0
            while j < cnt:
                ip_desc[interface[i + j]] = description[i + j]
                j = j + 1

            packData.extend([IP_Address[i], ip_desc])
            i = i + cnt

        # Your admin account password
        password = crt.Dialog.Prompt("SSH password:", "Password", "", True)

    for j in range(0, len(packData), 2):
        crt.Screen.Send('ssh ' + packData[j] + '\r')
        #crt.Dialog.MessageBox('ssh ' + packData[j])
        result = crt.Screen.WaitForStrings(["(yes/no)?", "refused", "ord:"])

        if result == 1:
            crt.Screen.Send('yes' + '\r')
        elif result == 2:
            crt.Screen.Send('telnet ' + packData[j] + '\r')
            crt.Screen.WaitForString("Username:")
            crt.Screen.Send('hpkadm' + '\r')
            crt.Screen.WaitForString("ord:")
        else:
            pass

        crt.Sleep(500)
        crt.Screen.Send(password + '\r')
        crt.Screen.WaitForString("#")

        #crt.Screen.Send('en' + '\r')
        #crt.Screen.WaitForString("ord:")

        #crt.Screen.Send(password + '\r')
        #crt.Screen.WaitForString("#")

        crt.Screen.Send('conf t' + '\r')
        crt.Screen.WaitForString("#")
        
        for key in packData[j + 1]:    
            crt.Screen.Send('int ' + key + '\r')
            #crt.Dialog.MessageBox("int " + key)
            crt.Screen.WaitForString("#")
            
            crt.Screen.Send('desc ' + 'UPLINK ' + packData[j + 1].get(key) + '\r')
            #crt.Dialog.MessageBox('desc ' + 'UPLINK ' + packData[j + 1].get(key))
            crt.Screen.WaitForString("#")
            
        crt.Screen.Send('end' + '\r')
        crt.Screen.WaitForString("#")

        crt.Screen.Send('wr' + '\r')
        crt.Screen.WaitForString("#")

        crt.Screen.Send('exit' + '\r')
        crt.Screen.WaitForString("$")

main()