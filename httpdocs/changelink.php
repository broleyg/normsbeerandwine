<html>
<body>

<form action="changelink.php" method="post">
New Link: <input type="text" name="link"><br>
Password: <input type="text" name="password"><br>
<input type="submit"><br>

<?php
	if($_POST["password"] == "merlotBeer3") {
		$file = fopen("newsletter_link.txt", "w") or die("Unable to open file");
		fwrite($file, $_POST["link"]);
		fclose($file);
		echo 'Wrote new link: ' . $_POST["link"];
	}
?>

</body>
</html>