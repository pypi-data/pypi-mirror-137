NoelOCR is a Python Library for extracting text from scanned PDF and full text PDF
developed by Noel Moses Mwadende. 







How it works ?



processPDF module from NoelOCR takes scanned PDF process it and
output searchabel/plain text.





For whom it was developed ?



It was developed for Machine Learning engineer who deals with PDF.
It might be classification of scanned PDF, text extraction from
scanned PDF or any task which requires feature extraction from
scanned PDF. Not only that, NoelOCR is very flexible as it can
also extract text from full text PDF. That means it works for both,
full text PDF and scanned PDF though it was purposefuly created
for scanned PDF.









How to use it ? 



import NoelOCR as nm

text = nm.processPDF('moses.pdf')

print(text)





It works for Linux operating system. The module for Windows
will be added in Beta version.