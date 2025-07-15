
<?php 

$hostname = "localhost"; 
$username = "root"; 
$password = "S/g041408";
$database = "truckers"; 

$conn = mysqli_connect($hostname, $username, $password, $database);

if (!$conn) 
{ 
	die("Connection failed: " . mysqli_connect_error()); 
} 

else {
echo "Database connection is OK<br>"; }

// check what values are being requested from Arduino
if(!empty($_GET('value'))) {
	$value = $_GET['value'];
	if($value == "truckers") {
		$sql = "USE truckers";
		if ($conn->query($sql) === TRUE) {
			$sql = "SELECT * FROM truckmanagement_job WHERE job_status = 'InProgress'";
			$result = $conn->query($sql);
			if ($result->num_rows > 0) {
				echo $result;
			}
		}
	}
	else if($value == "licenseplates") {
		$sql = "USE truckers";
		if ($conn->query($sql) === TRUE) {
			$sql = "SELECT * FROM truckmanagement_licenseplate";
			$result = $conn->query($sql);
			if ($result->num_rows > 0) {
				echo $result;
			}
		}
	}
}

if(!empty($_POST['sendval']) && !empty($_POST['sendval2']) )
{
	$temprature = $_POST['sendval'];
	$humidity  = $_POST['sendval2'];


// Update your tablename here
	$sql = "UPDATE sensor_data SET temprature = ".$temprature.", humidity = ".$humidity." WHERE id = 1"; 

	if ($conn->query($sql) === TRUE) {
		echo "Values updated in MySQL database table.";
	} else {
		echo "Error: " . $sql . "<br>" . $conn->error;
	}
}


// Close MySQL connection
$conn->close();

?>
