Maildb
======

        <p>Welcome to the Mail DataBase although it has expanded slightly now. Here is a list of all the things it does at the moment</p>
		<h3>Submit email from PCAP, Text stream, IMAP or POP servers</h3>
		<li>The email parser will read the headers extracting the main fields
		<li>Links, Img tags and Iframes sources extracted and listed
		<li>Any attatchments are extracted, Hashed stored and scanned with Yara, optionally you can include options to scan with Clam AV and submit to Virus Total
		<li>All the information extracted above is stored in to a SQLite Database as a Task.
		<li>All files are stored for further analysis
		<li>Options to submit file attatchments to Sandboxs, Cuckoo or FireEyes, MAS
		<h3>Http PCAP files</h3>
		<li>Extract all the streams
		<li>Parse the HTTP Headers
		<li>Extract all the HTTP Objects and files
		<li>Replicate the Server Path structure
		<li> Write the Header data to the SQLite Database as a Task
		<h3>Management System</h3>
		<li>Micro management system allows you to track Tasks in the Database
		<li>Add Comments to Tasks
		<li>Set tasks as Reviewed, Events or Unchecked
		<li>Generate, Weekly, Montly, Yearly reports on all Submitted tasks
		<li>Trend analysis on all artefacts in the database


Requires:
=========

		- Python 2.7
		- Mako
		- Bottle
		- Yara
		- BeautifulSoup (Included)


Reccomended:
============

		- SSDEEP 
		
INSTALL:
=========

		- See the INSTALL File for Installation details

Tested On
=========

		- Ubuntu 12.04
		- Windows 7 x64


To Do
=========
		- Implement Cuckoo API
		- Finish the VT Function
		- Timer for the IMAP / POP Feeds
		- More reports / trends.



