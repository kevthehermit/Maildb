//Copyright (C) 2012-2013 Kevin Breen.
// This file is part of the Maildb web application
// See the 'LICENSE' File for copying permission.

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






