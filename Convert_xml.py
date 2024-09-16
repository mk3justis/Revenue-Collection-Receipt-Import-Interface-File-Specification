'''
Script for the City of Winter Haven's Information Technology Department.
Converts an input .xml to an output .xml with different tag and attribute formatting.
Developed by Justis Nazirbage.
'''

import xml.etree.ElementTree as ET
from datetime import datetime as dt
import re

class Convert_xml :
    # Class constructor
    def __init__(self, r_file, w_file) :
        self.r_file = r_file
        self.w_file = w_file

    # Read the input xml and set the values for the new xml attributes.
    def __read_ximl(self) :
        tree = ET.parse(self.r_file)
        root = tree.getroot()
        # List of dictionaries to hold all attributes of all customers' tags.
        rows = []
        
        for row in root.findall('./ttReportRow') :
            info = {}
            
            for child in row :
                if child.tag == 'sagldistribution_glcode' :
                    info[''] = child.text
                elif child.tag == 'saglcode_accountnumber' :
                    info['GLAccountNumber'] = child.text
                elif child.tag == 'sagldistribution_costcenter' :
                    info[''] = child.text
                elif child.tag == 'sagldistribution_receiptnumber' :
                    info['ReceiptNumber'] = child.text
                elif child.tag == 'sagldistribution_module' :
                    info[''] = child.text
                elif child.tag == 'sagldistribution_paycode' :
                    if child.text == 'Debit Card' :
                        info['DistributionType'] = '1'
                        info['ReceiptPaymentType'] = '3'
                    elif child.text == 'Credit Card' :
                        info['DistributionType'] = '2'
                        info['ReceiptPaymentType'] = '3'
                    elif child.text == 'Cash' :
                        info['DistributionType'] = '0'
                        info['ReceiptPaymentType'] = '0'
                    elif child.text == 'Check' :
                        info['DistributionType'] = '0'
                        info['ReceiptPaymentType'] = '1'
                    elif child.text == 'Charge' :
                        info['DistributionType'] = '0'
                        info['ReceiptPaymentType'] = '2'
                    elif child.text == 'Wire Transfer' :
                        info['DistributionType'] = '0'
                        info['ReceiptPaymentType'] = '4'
                    else :
                        info['ReceiptPaymentType'] = '3'
                elif child.tag == 'sagldistribution_transactionreference1' :
                    info[''] = child.text
                elif child.tag == 'sagldistribution_username' :
                    info[''] = child.text
                elif child.tag == 'sagldistribution_dramount' :
                    info['sagldistribution_dramount'] = child.text
                elif child.tag == 'sagldistribution_cramount' :
                    info['ReceiptTransactionAmount'] = child.text
                elif child.tag == 'sagldistribution_postingdate-weekdaymonthdayyear' :
                    info[''] = child.text
                elif child.tag == 'sagldistribution_netamount' :
                    info['DistributionAmount'] = child.text
                elif child.tag == 'sagldistribution_postingdate_sort' :
                    date = dt.strptime(child.text, '%Y-%m-%d')
                    info['PaymentRecordedDate'] = date.strftime('%m/%d/%Y')
                elif child.tag == 'sagldistribution_glcode_sort' :
                    info[''] = child.text
                elif child.tag == 'sagldistribution_costcenter_sort' :
                    info[''] = child.text
                elif child.tag == 'sagldistribution_receiptnumber_sort' :
                    info[''] = child.text
                elif child.tag == 'DT_RowId' :
                    info[''] = child.text
                elif child.tag == 'DT_AllowChange' :
                    info[''] = child.text
                elif child.tag == 'DT_Record' :
                    info[''] = child.text
                
            rows.append(info)
        
        return rows

    # Write the converted data into output xml file.
    def write_xml(self) :
        rows = self.__read_xml()
        # Set up tree structure
        root = ET.Element('ROOT')

        for row in rows :
            ReceiptHeaderLevel = ET.SubElement(root, 'ReceiptHeaderLever')
            ReceiptTransactionLevel = ET.SubElement(ReceiptHeaderLevel, 'ReceiptTransactionLevel')
            ReceiptTransactionGLDistributionLevel = ET.SubElement(ReceiptTransactionLevel, 'ReceiptTransactionGLDistributionLevel')
            ReceiptPaymentLevel = ET.SubElement(ReceiptHeaderLevel, 'ReceiptPaymentLevel')
            
            ReceiptHeaderLevel.set('ReceiptNumber', row['ReceiptNumber'])
            ReceiptHeaderLevel.set('VoidedFlag', '0')
            ReceiptHeaderLevel.set('PaymentEnteredDate', row['PaymentRecordedDate'])
            ReceiptHeaderLevel.set('PaymentRecordedDate', row['PaymentRecordedDate'])
            ReceiptHeaderLevel.set('PaymentGLDate', row['PaymentRecordedDate'])
            ReceiptHeaderLevel.set('ReceivedFromName', 'Unknown')
            ReceiptHeaderLevel.set('ReceiptDescription', 'Unknown')
            ReceiptHeaderLevel.set('ReceiptCashier', 'Unknown')
            
            ReceiptTransactionLevel.set('ReceiptTransactionType', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionAmount', row['ReceiptTransactionAmount'])
            ReceiptTransactionLevel.set('ReceiptTransactionDescription', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionARCustomerNumber', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionARBillType', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionARBillNumber', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionLicenseeNumber', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionLicenseType', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionLicenseNumber', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionLicenseNumberID', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionLicenseRenewalNumber', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionLicenseRenewalNumberID', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionProjectCode1', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionProjectCode2', 'Unknown')
            ReceiptTransactionLevel.set('ReceiptTransactionProjectCode3', 'Unknown')
            
            ReceiptTransactionGLDistributionLevel.set('GLAccountNumber', row['GLAccountNumber'])
            ReceiptTransactionGLDistributionLevel.set('DueToDueFromFund', 'Unknown')
            ReceiptTransactionGLDistributionLevel.set('ProjectCode1', 'Unknown')
            ReceiptTransactionGLDistributionLevel.set('ProjectCode2', 'Unknown')
            ReceiptTransactionGLDistributionLevel.set('ProjectCode3', 'Unknown')
            ReceiptTransactionGLDistributionLevel.set('DistributionAmount', row['DistributionAmount'])
            ReceiptTransactionGLDistributionLevel.set('DistributionType', row['DistributionType'])
            
            ReceiptPaymentLevel.set('ReceiptPaymentType', row['ReceiptPaymentType'])
            ReceiptPaymentLevel.set('ReceiptPaymentAmount', row['DistributionAmount'])
            ReceiptPaymentLevel.set('ReceiptPaymentCheckNumber', 'Unknown')
            ReceiptPaymentLevel.set('ReceiptPaymentCreditCardNumber', 'Unknown')
            ReceiptPaymentLevel.set('ReceiptPaymentCreditCardType', 'Unknown')
            ReceiptPaymentLevel.set('ReceiptPaymentCreditCardExperationDate', 'Unknown')
            ReceiptPaymentLevel.set('ReceiptPaymentCreditCardValidationNumber', 'Unknown')
            ReceiptPaymentLevel.set('ReceiptPaymentCreditCardOtherType', 'Unknown')
        
        # Can't use this implementation if we want attributes on separate lines.
        tree = ET.ElementTree(root)
        ET.indent(tree, '   ')
        tree.write(self.w_file, encoding='utf-8', xml_declaration=True)
    
# Main
def main() :
    # Specify files
    read_file = 'WH__Total_Summary_By_User_101917_AM_9448.xml'
    write_file = 'write.xml'
    # Create object to convert xml
    xml_convert = Convert_xml(read_file, write_file)
    xml_convert.write_xml()
    
main()