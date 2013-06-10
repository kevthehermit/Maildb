function validateForm()
{
var x=document.forms["submission"]["data"].value;
if (x==null || x=="")
	{
	alert("A File Must be selected");
	return false;
	}
var y=document.forms["submission"]["comment"].value;
if (y==null || y=="")
	{
	alert("A Comment is required");
	return false;
	}
		

	
}
function validateComment()
{
var x=document.forms["Comments"]["title"].value;
if (x==null || x=="")
	{
	alert("Title is a required Field");
	return false;
	}
var y=document.forms["Comments"]["freetext"].value;
if (y==null || y=="")
	{
	alert("You must enter a Comment");
	return false;
	}	

	
}
