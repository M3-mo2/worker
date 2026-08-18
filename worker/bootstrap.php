<?php
// Runs before every bot script. Ensures the process working directory is the
// bot's own script directory, so relative file writes (e.g. mkdir('data'),
// file_put_contents('cache.json')) stay inside the user's folder.
// Confinement is still enforced by open_basedir (set per-request by Caddy).
if (isset($_SERVER['SCRIPT_FILENAME']) && is_string($_SERVER['SCRIPT_FILENAME'])) {
    $dir = dirname($_SERVER['SCRIPT_FILENAME']);
    if (is_dir($dir)) {
        @chdir($dir);
    }
}
