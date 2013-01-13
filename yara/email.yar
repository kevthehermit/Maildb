//Copyright (C) 2012-2013 Kevin Breen.
// This file is part of the Maildb web application
// See the 'LICENSE' File for copying permission.



rule known_XMailer
{ meta: description = "Known X-Mailer" strings: $a = "Sample Mailer v1" condition: $a}
rule Subject_Payroll
{ meta: description = "Sample Found In subject Line" strings: $a = "Sample" condition: $a}
rule Known_Sender
{ meta: description = "Known Sender" strings: $a = "mickey@mouse.co.uk" condition: $a}

rule Hidden_iframe
{ meta: description = "Hidden iframe" 
	strings: 
	$iframe = "<iframe" nocase
	$a = "width=0" nocase
	$b = "height=0" nocase
	condition: all of them
}
rule PHP_Mail_Script
{ meta: description = "PHP Mail Script" strings: $a = "X-PHP-Originating-Script" condition: $a}






