
function setOptions(chosen) {
var selbox = document.myform.opttwo;
 
selbox.options.length = 0;
if (chosen == " ") {
  selbox.options[selbox.options.length] = new Option('Please select one of the options above first',' ');
 
}
if (chosen == "main") {

  selbox.options[selbox.options.length] = new
Option('Date Added','date_added');
  selbox.options[selbox.options.length] = new
Option('Email MD5','eml_md5');
  selbox.options[selbox.options.length] = new
Option('Review State','Revmatch');
  selbox.options[selbox.options.length] = new
Option('Attatchment Count','attCount');
  selbox.options[selbox.options.length] = new
Option('Comment','Comment');
  selbox.options[selbox.options.length] = new
Option('Event Type','type');
}


if (chosen == "header") {

  selbox.options[selbox.options.length] = new
Option('Sent Date','date');
  selbox.options[selbox.options.length] = new
Option('From Address','from_add');
  selbox.options[selbox.options.length] = new
Option('Sender Domain','domain');
  selbox.options[selbox.options.length] = new
Option('Subject Line','subject');
  selbox.options[selbox.options.length] = new
Option('X-Mailer','x_mailer');
  selbox.options[selbox.options.length] = new
Option('X-Priority','x_priority');
  selbox.options[selbox.options.length] = new
Option('Message ID','message_id');
  selbox.options[selbox.options.length] = new
Option('CC Address','cc_add');
  selbox.options[selbox.options.length] = new
Option('Bcc Address','bcc_add');
  selbox.options[selbox.options.length] = new
Option('To Address','to_add');
}


if (chosen == "attatch") {

  selbox.options[selbox.options.length] = new
Option('FileName','filename');
  selbox.options[selbox.options.length] = new
Option('File Extension','fileExt');
  selbox.options[selbox.options.length] = new
Option('FileSize','date_added');
  selbox.options[selbox.options.length] = new
Option('MD5','md5');
  selbox.options[selbox.options.length] = new
Option('SHA256','sha256');
  selbox.options[selbox.options.length] = new
Option('SSDEEP','ssdeep');
  selbox.options[selbox.options.length] = new
Option('Yara Match','Revmatch');
}


if (chosen == "yara") {
  selbox.options[selbox.options.length] = new
Option('Yara Rule','rule');
  selbox.options[selbox.options.length] = new
Option('Yara Description','description');
}

if (chosen == "flows") {

  selbox.options[selbox.options.length] = new
Option('Source IP','SIP');
  selbox.options[selbox.options.length] = new
Option('Destination IP','DIP');
  selbox.options[selbox.options.length] = new
Option('Source Port','Sport');
  selbox.options[selbox.options.length] = new
Option('Destination Port','Dport');
}

if (chosen == "streams") {

  selbox.options[selbox.options.length] = new
Option('Method','Request');
  selbox.options[selbox.options.length] = new
Option('Requested Path','Path');
  selbox.options[selbox.options.length] = new
Option('Host','host');
  selbox.options[selbox.options.length] = new
Option('Referer','Referer');
  selbox.options[selbox.options.length] = new
Option('Proxy Auth','Proxy');
  selbox.options[selbox.options.length] = new
Option('Response','Response');

}

if (chosen == "hops") {

  selbox.options[selbox.options.length] = new
Option('Hop','hop');

}

}

