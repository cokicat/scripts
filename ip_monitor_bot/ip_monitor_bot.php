<?php

function get_country_info($ip) {	
	$ch = curl_init("http://ip-api.com/json/$ip?fields=status,country,countryCode,city");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);

    $response = curl_exec($ch);
    curl_close($ch);

    if ($response) {
        $data = json_decode($response, true);

        if ($data["status"] === "success") {
			return [
				"country" => $data["country"],
				"country_code" => $data["countryCode"],
				"city" => $data["city"]
			];
        }
	}

	return [];
}


function get_flag($countryCode) {
    $unicode_offset = 0x1F1E6; // Unicode flag

    if (strlen($countryCode) !== 2) return "🌍"; // Default flag

    $emoji1 = "&#" . ($unicode_offset + ord($countryCode[0]) - 65) . ";";
    $emoji2 = "&#" . ($unicode_offset + ord($countryCode[1]) - 65) . ";";

    return mb_convert_encoding($emoji1 . $emoji2, 'UTF-8', 'HTML-ENTITIES');
}


function send_message($token, $data) {
    $ch = curl_init("https://api.telegram.org/bot$token/sendMessage");
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);
    curl_close($ch);
}


if (!isset($_COOKIE["visited"])) {	
	$token = "<telegram_bot_token>"; // change this
	$chat_id = "<telegram_chat_id>"; // change this

	$ip = $_SERVER['REMOTE_ADDR'];

	$country_info = get_country_info($ip);
    $country = $country_info["country"] ?? "Unknown Country";
	$country_code = $country_info["country_code"] ?? "Unknown Country Code";
	$city = $country_info["city"] ?? "Unknown City";
	$country_flag = get_flag($country_code);

    $timestamp = $_SERVER['REQUEST_TIME'];
	$date = date("d/m/Y H:i:s", $timestamp);

    $port = $_SERVER['REMOTE_PORT'];
    $request_method = $_SERVER['REQUEST_METHOD'];
    $ua = $_SERVER['HTTP_USER_AGENT'];
    $language = $_SERVER['HTTP_ACCEPT_LANGUAGE'];

    $message = <<<EOF
<b><u>Report for: $date</u></b>

<b>IP:</b> <code>$ip</code>
<b>Country:</b> $country_flag $country, $city
<b>Port:</b> <code>$port</code>
<b>Request Method:</b> <code>$request_method</code>
<b>User Agent:</b> <code>$ua</code>
<b>Language:</b> <code>$language</code>
<a href="https://ip-api.com/#$ip">More info...</a>
EOF;

	$data = [
		"chat_id" => $chat_id,
		"text" => $message,
		"parse_mode" => "HTML"
	];

	send_message($token, $data);
    setcookie("visited", "1", time() + 3600); // 1 hour cookie
}

?>

