import csv

with open('interface.csv', 'r') as data:

    data_reader = csv.reader(data)
    next(data_reader)

    ip = []
    interface = []
    desc = []
    packData = []
    
    i = 0

    for row in data_reader:
        ip.append(row[0])
        interface.append(row[1])
        desc.append(row[2])
    
    while i < len(ip):
        cnt = ip.count(ip[i])
        ip_desc = {}    
        
        j = 0
        while j < cnt:
            ip_desc[interface[i + j]] = desc[i + j]
            j = j + 1
            
        packData.extend([ip[i], ip_desc])
        i = i + cnt
        
    print(packData)    

    for j in range(0, len(packData), 2):
        print('ssh ' + packData[j])
        for key in packData[j + 1]:
            print("interface " + key)
            print("desc " + packData[j + 1].get(key))
