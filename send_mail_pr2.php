<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

// Include PHPMailer files
require 'PHPMailer/PHPMailer.php';
require 'PHPMailer/SMTP.php';
require 'PHPMailer/Exception.php';

// Validate and sanitize inputs
$email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
$prenom = htmlspecialchars($_POST['prenom'] ?? '');
$telephone = htmlspecialchars($_POST['telephone'] ?? '');
$wilaya = htmlspecialchars($_POST['wilaya'] ?? '');
$profession = htmlspecialchars($_POST['profession'] ?? '');
$appartement = htmlspecialchars($_POST['appartement'] ?? '');

// Ensure all required fields are filled
if (!$email || !$prenom || !$telephone || !$wilaya || !$profession || !$appartement) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Tous les champs sont obligatoires.']);
    exit;
}

$mail = new PHPMailer(true);

try {
    // SMTP settings
    $mail->isSMTP();
    $mail->Host = 'smtp.gmail.com'; // Change this if you're using a different SMTP
    $mail->SMTPAuth = true;
    $mail->Username   = 'nasreddinehamou8@gmail.com';         // 🔁 Your Gmail address
    $mail->Password   = 'rqfzuhtmmxqcduvg';         // ✅ Use app-specific password if Gmail
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
    $mail->Port = 587;

    // Sender and recipient
    $mail->setFrom('contact@imaar-eldjazair.com', 'Form Submission');
    $mail->addAddress('nasreddinehamou8@gmail.com');

    // Email content
    $mail->isHTML(true);
    $mail->Subject = 'Nouvelle Demande De La Residence Orion';
    $mail->Body = "
        <h3>Salut,</h3>
        <p><strong>Nom et Prénom:</strong> {$prenom}</p>
        <p><strong>Email:</strong> {$email}</p>
        <p><strong>Téléphone:</strong> {$telephone}</p>
        <p><strong>Wilaya:</strong> {$wilaya}</p>
        <p><strong>Profession:</strong> {$profession}</p>
        <p><strong>Appartement:</strong> {$appartement}</p>
    ";

    $mail->send();

    echo json_encode(['success' => true, 'message' => 'Formulaire envoyé avec succès.']);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Erreur lors de l\'envoi: ' . $mail->ErrorInfo]);
}
?>
