<?php
// Executed by the worker's /health endpoint through the internal Caddy +
// PHP-FPM path (see the `handle /__php_health` route in the Caddyfile).
// Outputs a fixed token so /health can confirm PHP actually ran end-to-end
// (not merely that Caddy is listening). No compat prepend is applied for this
// route, so it must not depend on any framework globals.
http_response_code(200);
echo "php-health-ok";
