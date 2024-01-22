
import xml.etree.ElementTree as ET
import argparse
import os

parser = argparse.ArgumentParser(description="Remove ordernumber from invoice",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--files", help="input .xml file, example, -f C:\python\APReporting_SED5_20231222113508.xml", required=True, default=[], nargs='+')
parser.add_argument("-o", "--ordernumbers", help="list of ordernumbers to remove, example -o 000000110450 000000110451", required=True, default=[], nargs='+')
args = parser.parse_args()
config = vars(args)
paths = args.files
ordernumbers = args.ordernumbers

for path in paths:
    file = os.path.splitext(os.path.basename(path))[0]
    folder = os.path.dirname(path)

    filename = os.path.join(folder, f'{file}.modified.xml')
    filteredFilename = os.path.join(folder, f'{file}.filtered_out.xml')

    tree = ET.parse(path)

    root = tree.getroot()
    dataarea = root.findall("dataarea")

    invoices = dataarea[0].findall("invoice")

    newInvoices = []
    filteredInvoices = []
    for i in invoices:
         ordernumber = i.find("ordernumber")
         if (ordernumber is not None and ordernumber.text in ordernumbers):
            i.remove(ordernumber)
            newInvoices.append(i)
         else:
            filteredInvoices.append(i)

    dataarea[0].clear()

    for i in newInvoices:
        dataarea[0].append(i)
    with open(filename, 'wb') as f:
        tree.write(f, encoding='utf-8')
    
    dataarea[0].clear()
    
    for i in filteredInvoices:
        dataarea[0].append(i)
    with open(filteredFilename, 'wb') as f:
        tree.write(f, encoding='utf-8')


