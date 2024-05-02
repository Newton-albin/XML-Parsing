import xml.etree.ElementTree as et
import pandas as pd

#pip install pycopy-xml.etree.ElementTree
roots =''
def fetch_roots():
    global roots
    #declaring input file name
    #'D:/crst/DB Profiler/trace_file.txt'
    ip_file = input('Enter file path to parse : ')

    #defining output file
    
    op_file = ip_file.rsplit('.',1)[0].strip()+'_Parse_Result'+'.xlsx'
    #print(op_file)
    print()
    try:
        #parsing input file
        parser=et.XMLParser(encoding="UTF-8")
        tree=et.parse(ip_file,parser=parser)

        #getting root tag from xml file
        roots= tree.getroot()
        print("------------------- Root Fetched ----------------------")
        print()
    except et.ParseError as e:
        print("XML Syntax Error:",e)
        print()
        print("------------ ERROR WHILE OPENING FIILE; TRY AGAIN ---------------")

    #printing root tags
    for root in roots:
        print(root)
    print()
    return 0

def fetch_values(op_file):
    global roots

    Event_cnt=0
    Parse=[]
    spid_count=0

    #find all the Event tag
    root_tag=input('Paste the Root namespace : ')
    SPID_flag = int(input('Enter 0 to all or Enter 1 to specific value : '))
    if(SPID_flag==1):
        SPID = input('Enter the SPID to search and count : ')
    else:
        SPID = input('Enter the SPID to count : ')
    
    for event in roots[1].findall(root_tag+'Event'):
        #print('a')
        #print("----Event:------",Event_cnt)
        column_values_texts={} # adding column data to dictionary
        flag=0
    
        for column in event.findall(root_tag+'Column'):
            #print(column.attrib) # printing attributes of column tag
            key = column.get('name') #fetching attribute name 
            value = column.text #fetching attribute text
            column_values_texts[key]=value # appending to dictionary

            #incrementing the spid_count when spid=51 in each iteration
            
            if(key == 'SPID' and value == SPID):
                spid_count+=1
                flag=1
                

        if(SPID_flag==0):
            Parse.append(column_values_texts) #appending all values to final list
        else:
            if(flag==1):
                Parse.append(column_values_texts) #appending the required spid value to the list
        Event_cnt+=1

        #To test with limited numeber of loops
        if(Event_cnt==2):
            break
        else:
            Event_cnt+=1
    print()    
    print('------------ Extracted all the column tags -------------')
    print()
    print('---------------------- Summary -------------------------')
    print('No. of. Event Tag  = ', Event_cnt)
    print('No. of. SPID : {0} = {1}'.format(SPID,spid_count))

    #print(Parse)
    #creating dataframe to get the table strucutre
    dataframe = pd.DataFrame(Parse) 
    #print(dataframe.to_string())

    #loading to excel file
    dataframe.to_excel(op_file, index=False)
    print()
    print('---------------- Loaded to Target File -----------------')
    print('---------------------- SUCCESS--------------------------')

    return 0

op_file=fetch_roots()
fetch_values(op_file)
