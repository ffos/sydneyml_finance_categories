# sydneyml_finance_categories
For australian bank statements from one of CBA, ANZ or Bendigo banks, detect the uploaded csv as from one the banks, parse and categorize the transactions.

This project uses sklearn to classify text. 

# Main problems:
The big main problem was getting data, and lots of it. It wasn't much of an issue for implementing the classifier to detect the bank from statement, but was a real bottleneck to implement the classifier to group transactions into various categories. 


# Detecting bank from csv
Bank statements look like:

CBA:

| Date | Amount | Desc |
|27/08/2017 | -6.50 | DELISSE SYDNEY NS AUS Card xx7113 Value Date: 25/09/2017 |
|20/07/2017 | -4.00 | SOUTHGATE GROUP AUSTRA SYDNEY  AUS Card xx7113 Value Date: 26/09/2017 |
|21/06/2017 | -10.00 | Direct Debit 142619 TPG Internet DH9M1IFK4EH-03GJKN	|


Bendigo:

| Date | Amount | Desc |
|10/11/2017 | -14 | RETAIL PURCHASE PUB LIFE KITCHEN, ULTIMO 0810 AUD000000001400 |		
|08/09/2017 | 1000 | E-BANKING TRANSFER 0132269686 0034046540V501		|
|18/07/2017 | 250 | E-BANKING TRANSFER 0132269657 0024701161V501		|
|02/01/2017 | -37 | RETAIL PURCHASE BROWN JERSEY BIKES, ULTIMO 0710 AUD000000003700		|
|28/12/2016 | -135 | RETAIL PURCHASE CLEAN EXPRESS LAUNDE, ULTIMO 0610 AUD000000013500		|
|08/10/2016 | -10.5 | RETAIL PURCHASE COLES EXPRESS 1698, ULTIMO 0710 AUD000000001050		|
|07/08/2016 | -8.47 | INTERNATIONAL TRANSACTION FEE		|


ANZ:

| Date | Amount | Desc |
| 03-09-2017 | -15.14 | 7-ELEVEN 2180 ASHFIELD |
| 20-04-2017 | -200 | BUNNINGS 572000 PENRITH |
| 15-10-2016 | -15.08 | COLES EXPRESS 1557 MINTO |

The idea is to look at the description and tell which bank it came from. While one could argue that we could write regex patterns to detect the banks, the emphasis here is to learn from examples and have the classifier detect it

This was accomplished with GaussianNB classifier from sklearn


# Categorizing transactions
The goal was to categorize the transactions into buckets like `groceries`, `gas_station`, `internet/phone` .. etc
This was a very hard problem. The statements say nothing about the nature of the business, and I used google places api to get training classification for as much data as possible. But since our data was limited, the classification suffered severely, with accuracy of 53% using SVC classifier from sklearn
