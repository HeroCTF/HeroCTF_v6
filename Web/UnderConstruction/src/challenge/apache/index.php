<?php
$nonce = bin2hex(random_bytes(16));
header("Content-Security-Policy: default-src 'none'; script-src 'nonce-$nonce' 'strict-dynamic'; style-src 'self'; img-src 'self'; object-src 'none'; base-uri 'none'; connect-src 'self'; frame-src 'self'");
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Under Construction</title>
    <link rel="icon" type="image/x-icon" href="/c/static/favicon.jpg">
    <link rel="stylesheet" type="text/css" href="/c/static/styles.css">
    <script id="userInfo">
        <?= json_encode(array_merge([
            "ip" => $_SERVER["HTTP_X_REAL_IP"],
            "date" => date("Y-m-d H:i:s"),
            "user-agent" => $_SERVER["HTTP_USER_AGENT"]
        ], $_GET)) ?>
    </script>
</head>
<body>
    <header>
        <div class="construction-container">
            <div class="icon">🚧</div>
            <h1>We're Under Construction</h1>
            <p>Our website is currently being updated. Check back soon!</p>
        </div>
    </header>

    <main></main>

    <footer>
        <script>console.log(navigator.serviceWorker.register)</script>
        <script nonce="<?= $nonce ?>" src="/c/static/bundle.js"></script>
    </footer>
</body>
</html>