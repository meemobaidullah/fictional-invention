<?php
declare(strict_types=1);
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: meeting.html'); exit; }
if (!empty($_POST['website'] ?? '')) { header('Location: thank-you.html'); exit; }
function clean(string $key): string { return trim(strip_tags((string)($_POST[$key] ?? ''))); }
$name=clean('name'); $email=filter_var(clean('email'), FILTER_VALIDATE_EMAIL); $phone=clean('phone');
$business=clean('business'); $service=clean('service'); $timezone=clean('timezone'); $times=clean('times'); $message=clean('message');
if (!$name || !$email || !$service || !$timezone || !$times || !$message || clean('consent') !== 'yes') { http_response_code(422); exit('Please complete every required field.'); }
$to='ecommeem@gmail.com'; $subject='eCommeem meeting request: '.$service;
$body="New meeting request\n\nName: $name\nEmail: $email\nPhone: $phone\nBusiness: $business\nService: $service\nTime zone: $timezone\nPreferred times: $times\n\nGoals and situation:\n$message\n";
$headers=['From: eCommeem Website <noreply@ecommeem.com>','Reply-To: '.$email,'Content-Type: text/plain; charset=UTF-8'];
if (!mail($to,$subject,$body,implode("\r\n",$headers))) { http_response_code(500); exit('The email could not be sent. Please email ecommeem@gmail.com directly.'); }
header('Location: thank-you.html'); exit;
?>