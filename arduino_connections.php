
<?php 

$hostname = "localhost"; 
$username = "root"; 
$password = "S/g041408";
$database = "truckers"; 

$conn = mysqli_connect($hostname, $username, $password, $database);

$license_plates = [
	"ABC1234",
	"XYZ5678",
	"LMN9101",
	"QRS2345",
	"TUV6789"
];

if (!$conn) 
{ 
	die("Connection failed: " . mysqli_connect_error()); 
} 

else {
echo "Database connection is OK<br>"; }

// check what values are being requested from Arduino
if(!empty($_GET('value'))) {
	$value = $_GET['value'];
	if($value == "active_jobs") {
		$sql = "USE truckers";
		if ($conn->query($sql) === TRUE) {
			$sql = "SELECT * FROM truckmanagement_job WHERE job_status = 'InProgress'";
			$result = $conn->query($sql);
			if ($result->num_rows > 0) {
				echo json_encode($result->fetch_all(MYSQLI_ASSOC));
			}
		}
	}
	else if($value == "plate_initial") {
		/*$sql = "USE truckers";
		if ($conn->query($sql) === TRUE) {
			$sql = "SELECT * FROM truckmanagement_licenseplate";
			$result = $conn->query($sql);
			if ($result->num_rows > 0) {
				echo $result;
			}
		}*/
		// just for testing purposes, this will return initial license plate from OCR
		echo json_encode(["plate" => $license_plates[0]]);
	}
	else if($value=="status") {
		$sql = "USE truckers";
		$job_id = $_GET['job_id'];
		if ($conn->query($sql) === TRUE) {
			$sql = "SELECT * FROM truckmanagement_job WHERE job_id = '$job_id'";
			$result = $conn->query($sql);
			$status = $result->fetch_assoc()['status'];
			if ($result->num_rows > 0) {
				echo $status;
			} else {
				echo "error on getting status";
			}
		}
	}
	else if($value=="temp_finger") {
		$sql = "USE truckers";
		$job_id = $_GET['job_id'];
		if ($conn->query($sql) === TRUE) {
			$sql = "SELECT * FROM truckmanagement_job WHERE job_id = '$job_id'";
			$result = $conn->query($sql);
			$status = $result->fetch_assoc()['temp_finger'];
			if ($result->num_rows > 0) {
				echo $status;
			} else {
				echo "error on getting status";
			}
		}
	}
	else if($value == "plate_final") {
		echo json_encode(["plate" => $license_plates[1]]);
	}
	else {
		echo "Invalid value requested.";
	}
}

if(!empty($_POST['job_id'])) {
	$job_id = $_POST['job_id'];
	$column = $_POST['column'];
	$message = $_POST['message'];
	$sql = "UPDATE truckmanagement_job SET $column = '$message' WHERE job_id = '$job_id'";
	if ($conn->query($sql) === TRUE) {
		echo "Column $column updated successfully with value $message in job #$job_id.";
	} else {
		echo "Error updating column: " . $conn->error;
	}
}


// Close MySQL connection
$conn->close();

?>
