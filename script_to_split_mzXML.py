#Importing necessary libraries for xml parsing
import lxml.etree as le
import sys
from os.path import basename
from sys import argv

def split_mzXML(src,scan_start,scan_end):
    #parsing xml tree 
    tree = le.parse(src)
    root = tree.getroot()
    
    #Variable for namespace tag in xml root
    ns =   root.tag[1:].split("}")[0]
    
    # Scan start and end numbers
    scan_start = int(scan_start)
    scan_end = int(scan_end)

    for node in tree.findall("{%s}msRun" %(ns)):
        for snode in node.getchildren():
            num = (snode.attrib.get('num'))
            if isinstance(num,str):
                num = int(num)
                if num not in range(scan_start,scan_end):
                    node.remove(snode)

    for node in tree.findall("{%s}index" %(ns)):
        for snode in node.getchildren():
            if snode.tag == "{%s}offset" %(ns):
                id = snode.attrib.get('id')
                if isinstance(id,str):
                    id = int(id)
                    if id not in range(scan_start,scan_end):
                        node.remove(snode)

    root = tree.getroot()

    output_filename = 'split_'+basename(src)
    f = open(output_filename, 'w')
    f.write(le.tostring(root, pretty_print=True,encoding="unicode"))
    f.close()

# arguments from user
src = argv[1]
scan_start = argv[2]
scan_end = argv[3]

#function call with arguments
split_mzXML(src,scan_start,scan_end)