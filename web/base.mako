# -*- coding: utf-8 -*-
<!--
    Maildb Application To Parse Emails and other Traffic from Pcap Files or streams.
    Copyright (C) 2012-2013  Kevin Breen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->
<html>
<head>



<title>Mail DataBase ${self.title()}</title>
${self.head_tags()}
<link rel="stylesheet" type="text/css" href="/static/mae.css" />

</head>
<body>
<script language="javascript">
var popupWindow = null;
function centeredPopup(url,winName,w,h,scroll){
LeftPosition = (screen.width) ? (screen.width-w)/2 : 0;
TopPosition = (screen.height) ? (screen.height-h)/2 : 0;
settings =
'height='+h+',width='+w+',top='+TopPosition+',left='+LeftPosition+',scrollbars='+scroll+',resizable'
popupWindow = window.open(url,winName,settings)
}
</script>
<ul id="nav">
    <img src="/static/Maildb.png" align="left"/>
    <li id="nav-1"><a href="/">Home</a></li>
    <li id="nav-2"><a href="/browse">Browse</a></li>
    <li id="nav-3"><a href="/stats">Stats</a></li>
    <li id="nav-4"><a href="/search">Search</a></li>
    <li id="nav-5"><a href="/help">Help</a></li>
    <li id="nav-6"><a href="/decode">Decode Tools</a></li>
    <li id="nav-7"><a href="/admin">Admin</a></li>
</ul>
<br>
<br>
    

${self.body()}
<br />
<p align="center">Copyright Kevin Breen 2012-2013 Version xxxx</p>
</body>
</html>
