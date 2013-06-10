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
<!doctype html>
<html>
<head>


<script src="/static/js/jquery.min.js" type="text/javascript"></script>
<script src="/static/js/popup.js" type="text/javascript"></script>
<title>DataBase ${self.title()}</title>
${self.head_tags()}
<link rel="stylesheet" type="text/css" href="/static/css/mae.css">
<link rel="stylesheet" type="text/css" href="/static/css/menu.css">
</head>
<body>

<div class=container>
<div id='cssmenu'>
<ul>
	
   <li><a href='/'><span>Home</span></a></li>
   <li><a href='/browse'><span>Browse</span></a></li>
   <li><a href='/stats'><span>Stats</span></a></li>
      <li class='has-sub last'><a href='#'><span>Search</span></a>
      <ul>
         <li><a href='/search'><span>Record Search</span></a></li>
         <li class='last'><a href='/logSearch'><span>Log Search</span></a></li>
      </ul>
   </li>
   <li class='has-sub last'><a href='#'><span>Tools</span></a>
      <ul>
         <li><a href='/help'><span>Help</span></a></li>
         <li><a href='/decode'><span>Decode Tools</span></a></li>
         <li><a href='/useradmin'><span>User Accounts</span></a></li>
         <li class='last'><a href='/admin'><span>Admin Tools</span></a></li>
      </ul>
   </li>
   <li><a href='/login'><span>Login</span></a></li>
   <li><a href='/logout'><span>Logout</span></a></li>
</ul>
</div>
</div>

    
<div class="container">
${self.body()}
</div>
<p align="center">Copyright Kevin Breen 2012-2013 Version 0.3.3</p>
</body>
</html>
