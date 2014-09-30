__author__ = 'Andrew'
import requests
import xml.etree.ElementTree as ET


def get_info(account, password, pic):
    transaction = ET.Element('TransactionsListingRequest')
    accountid = ET.SubElement(transaction, 'AccountID')
    accountid.text = account
    passphrase = ET.SubElement(transaction, 'PassPhrase')
    test = ET.SubElement(transaction, "Test")
    test.text = "Y"
    passphrase.text = password
    tracking = ET.SubElement(transaction, 'TrackingList')
    PICNumber = ET.SubElement(tracking, 'PICNumber')
    PICNumber.text = pic
    return '<?xml version="1.0" encoding="utf-8"?>' + ET.tostring(transaction, encoding="us-ascii", method="xml")


def check_refund(info, link):
    data = info.encode('utf-8')
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    request = {'XMLInput': data}
    r = requests.post(link,
                      data=request, headers=headers)
    return r.content

# https://www.endicia.com/ELS/ELSServices.cfc?wsdl&method=GetTransactionsListing


def return_refund(x):

    returned_data_et = ET.fromstring(x)
    # print returned_data_et
    return returned_data_et.find('TransactionResults').find('Transaction').find('RefundCode').text
    # print returned_data_et.find('Transaction Results').find('Transaction').find('Weight').text


def main(account, password, pic, link):
    info = get_info(account, password, pic)
    x = check_refund(info, link)
    return_refund(x)


main('blaa','foo','bar','https://www.endicia.com/ELS/ELSServices.cfc?wsdl&method=GetTransactionsListing')

xml_example = '<?xml version="1.0" encoding="UTF-8"?> <TransactionsListingResponse>  <AccountID></AccountID>  <ErrorMsg></ErrorMsg>  <Test></Test>  <TransactionResults>   <Transaction>    <RefundCode>N</RefundCode>     <RefundStatus></RefundStatus>   </Transaction>  </TransactionResults> </TransactionsListingResponse>'.strip()
print return_refund(xml_example)

