<?php  

$url=$_POST["url"];  
$html = file_get_contents($url);  
echo $html;  
?> 

