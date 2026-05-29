# bot/utils/bot_detector.py
# Comprehensive Telegram bot detection for PHP files.
# Supports multi-file OOP projects with recursive include/require chain tracing.

import os
import re
from typing import Dict, List, Optional, Set

# ─── Patterns for reading POST input ──────────────────────────
INPUT_PATTERNS = [
    re.compile(r"""file_get_contents\s*\(\s*['"]php://input['"]\s*\)"""),
    re.compile(r"""file_get_contents\s*\(\s*\$\w+\s*\)"""),          # via variable
    re.compile(r"""fopen\s*\(\s*['"]php://input['"]\s*,"""),
    re.compile(r"""php://stdin"""),
    re.compile(r"""\$HTTP_RAW_POST_DATA"""),
    re.compile(r"""GLOBALS\s*\[\s*['"]HTTP_RAW_POST_DATA"""),
]

# ─── Patterns for include/require statements ──────────────────
INCLUDE_PATTERNS = [
    # include 'file.php' / require_once "file.php" / etc.
    re.compile(
        r"""(?:include|include_once|require|require_once)\s*[\(]?\s*['"]([^'"]+)['"]\s*[\)]?\s*;""",
        re.IGNORECASE
    ),
    # include __DIR__ . '/file.php'
    re.compile(
        r"""(?:include|include_once|require|require_once)\s*[\(]?\s*__DIR__\s*\.\s*['"]([^'"]+)['"]\s*[\)]?\s*;""",
        re.IGNORECASE
    ),
    # include dirname(__FILE__) . '/file.php'
    re.compile(
        r"""(?:include|include_once|require|require_once)\s*[\(]?\s*dirname\s*\(\s*__FILE__\s*\)\s*\.\s*['"]([^'"]+)['"]\s*[\)]?\s*;""",
        re.IGNORECASE
    ),
]

# ─── Token pattern ────────────────────────────────────────────
TOKEN_PATTERN = re.compile(r'\d{6,14}:[a-zA-Z0-9_\-]{35,75}')

# ─── Max include depth to prevent infinite loops ──────────────
MAX_INCLUDE_DEPTH = 10


def _read_file_safe(file_path: str) -> Optional[str]:
    """Read a PHP file safely, return None on failure."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return None


def _has_input_pattern(content: str) -> bool:
    """Check if content contains any PHP input reading pattern."""
    for pattern in INPUT_PATTERNS:
        if pattern.search(content):
            return True
    return False


def _has_token(content: str) -> bool:
    """Check if content contains a Telegram bot token."""
    return bool(TOKEN_PATTERN.search(content))


def _extract_includes(content: str, base_dir: str) -> List[str]:
    """
    Extract all include/require paths from PHP content,
    resolved to absolute paths relative to base_dir.
    
    Also handles:
    - PHP autoloaders (spl_autoload_register) + use statements
    - PSR-4 style namespace-to-directory mapping
    """
    includes = []
    
    # --- Standard include/require ---
    for pattern in INCLUDE_PATTERNS:
        for match in pattern.finditer(content):
            raw_path = match.group(1)
            raw_path = raw_path.lstrip('/')
            raw_path = raw_path.lstrip('./')
            resolved = os.path.normpath(os.path.join(base_dir, raw_path))
            if os.path.isfile(resolved):
                includes.append(resolved)
    
    # --- Autoloader + use statement resolution ---
    # Detect spl_autoload_register and extract namespace → directory mapping
    # Common patterns:
    #   $prefix = 'Src\\';  $base_dir = __DIR__ . '/src/';
    #   $base_dir = __DIR__ . '/app/';
    #   str_replace('\\', '/', $relative_class)
    
    autoloader_mappings = _detect_autoloader(content, base_dir)
    
    if autoloader_mappings:
        # Extract all 'use' statements from this file
        use_pattern = re.compile(r'^\s*use\s+([A-Za-z0-9_\\\\]+)\s*;', re.MULTILINE)
        for match in use_pattern.finditer(content):
            fqcn = match.group(1)  # e.g. Src\Telegram\Request
            
            for prefix, mapped_dir in autoloader_mappings:
                if fqcn.startswith(prefix):
                    relative = fqcn[len(prefix):]
                    # Convert namespace separators to path separators
                    relative_path = relative.replace('\\', '/') + '.php'
                    resolved = os.path.normpath(os.path.join(mapped_dir, relative_path))
                    if os.path.isfile(resolved):
                        includes.append(resolved)
                    break
    else:
        # Fallback: even without detected autoloader, try resolving 'use' statements
        # against common directory structures (src/, app/, lib/, classes/)
        use_pattern = re.compile(r'^\s*use\s+([A-Za-z0-9_\\\\]+)\s*;', re.MULTILINE)
        common_dirs = ['src', 'app', 'lib', 'classes', 'vendor', '']
        
        for match in use_pattern.finditer(content):
            fqcn = match.group(1)
            # Try each common directory
            for cdir in common_dirs:
                # Try with first namespace segment stripped (e.g. Src\Telegram\Bot → Telegram/Bot.php)
                parts = fqcn.split('\\')
                if len(parts) >= 2:
                    # Without first segment
                    relative_path = '/'.join(parts[1:]) + '.php'
                    if cdir:
                        resolved = os.path.normpath(os.path.join(base_dir, cdir, relative_path))
                    else:
                        resolved = os.path.normpath(os.path.join(base_dir, relative_path))
                    if os.path.isfile(resolved):
                        includes.append(resolved)
                        break
                
                # With all segments as path
                relative_path = '/'.join(parts) + '.php'
                if cdir:
                    resolved = os.path.normpath(os.path.join(base_dir, cdir, relative_path))
                else:
                    resolved = os.path.normpath(os.path.join(base_dir, relative_path))
                if os.path.isfile(resolved):
                    includes.append(resolved)
                    break
    
    return includes


def _detect_autoloader(content: str, base_dir: str) -> List[tuple]:
    """
    Detect PHP autoloader registration and extract namespace-to-directory mappings.
    
    Returns list of (namespace_prefix, absolute_directory) tuples.
    """
    mappings = []
    
    if 'spl_autoload_register' not in content:
        return mappings
    
    # Pattern 1: $prefix = 'Namespace\\'; $base_dir = __DIR__ . '/dir/';
    prefix_match = re.search(
        r"""\$\w*prefix\w*\s*=\s*['"]([^'"]+)['"]""",
        content
    )
    base_match = re.search(
        r"""\$\w*(?:base_dir|baseDir|base|dir)\w*\s*=\s*__DIR__\s*\.\s*['"]([^'"]+)['"]""",
        content
    )
    
    if prefix_match and base_match:
        prefix = prefix_match.group(1).rstrip('\\') + '\\'
        rel_dir = base_match.group(1).strip('/')
        abs_dir = os.path.normpath(os.path.join(base_dir, rel_dir))
        if os.path.isdir(abs_dir):
            mappings.append((prefix, abs_dir))
    
    # Pattern 2: Just a base_dir without explicit prefix — assume root namespace
    if not mappings and base_match:
        rel_dir = base_match.group(1).strip('/')
        abs_dir = os.path.normpath(os.path.join(base_dir, rel_dir))
        if os.path.isdir(abs_dir):
            mappings.append(('', abs_dir))
    
    # Pattern 3: Common convention — if autoloader exists but no clear prefix,
    # try standard directories
    if not mappings:
        for common_dir in ['src', 'app', 'lib', 'classes']:
            candidate = os.path.join(base_dir, common_dir)
            if os.path.isdir(candidate):
                # Use directory name as prefix (capitalized)
                prefix = common_dir.capitalize() + '\\'
                mappings.append((prefix, candidate))
                break
    
    return mappings


def _trace_includes(
    file_path: str,
    visited: Set[str],
    depth: int = 0
) -> Dict:
    """
    Recursively trace include/require chain from a PHP file.
    
    Returns dict with:
        - has_input: bool
        - has_token: bool
        - input_source: str or None (path where php://input was found)
        - token_source: str or None (path where token was found)
        - chain: list of traced file paths
    """
    result = {
        'has_input': False,
        'has_token': False,
        'input_source': None,
        'token_source': None,
        'chain': [],
    }
    
    # Safety checks
    if depth > MAX_INCLUDE_DEPTH:
        return result
    
    abs_path = os.path.abspath(file_path)
    if abs_path in visited:
        return result  # Already visited — prevent infinite loops
    
    visited.add(abs_path)
    result['chain'].append(abs_path)
    
    content = _read_file_safe(abs_path)
    if content is None:
        return result
    
    # Check this file for input patterns
    if _has_input_pattern(content):
        result['has_input'] = True
        result['input_source'] = abs_path
    
    # Check this file for token
    if _has_token(content):
        result['has_token'] = True
        result['token_source'] = abs_path
    
    # If we already found both, no need to dig deeper
    if result['has_input'] and result['has_token']:
        return result
    
    # Extract includes and trace them recursively
    base_dir = os.path.dirname(abs_path)
    includes = _extract_includes(content, base_dir)
    
    for included_path in includes:
        sub_result = _trace_includes(included_path, visited, depth + 1)
        result['chain'].extend(sub_result['chain'])
        
        if sub_result['has_input'] and not result['has_input']:
            result['has_input'] = True
            result['input_source'] = sub_result['input_source']
        
        if sub_result['has_token'] and not result['has_token']:
            result['has_token'] = True
            result['token_source'] = sub_result['token_source']
        
        # Early exit if both found
        if result['has_input'] and result['has_token']:
            return result
    
    return result


def detect_telegram_bot(file_path: str) -> Dict:
    """
    Comprehensive check: is this PHP file a Telegram bot entry point?
    
    Uses 3 layers:
      1. Direct php://input detection (multiple patterns)
      2. Recursive include/require chain tracing
      3. Token detection in file and its include chain
    
    Returns:
        {
            "is_bot": bool,           # Can this file be run as a bot?
            "has_input": bool,        # php://input found (direct or via includes)
            "has_token": bool,        # Bot token found (direct or via includes)
            "input_source": str,      # Path where php://input was found
            "token_source": str,      # Path where token was found
            "include_chain": list,    # All files traced
        }
    """
    if not os.path.isfile(file_path):
        return {
            'is_bot': False,
            'has_input': False,
            'has_token': False,
            'input_source': None,
            'token_source': None,
            'include_chain': [],
        }
    
    visited: Set[str] = set()
    trace = _trace_includes(file_path, visited)
    
    return {
        'is_bot': trace['has_input'],  # Main criterion: can receive webhook updates
        'has_input': trace['has_input'],
        'has_token': trace['has_token'],
        'input_source': trace['input_source'],
        'token_source': trace['token_source'],
        'include_chain': trace['chain'],
    }


# ═══════════════════════════════════════════════════════════════
# Project-level Analysis (for ZIP uploads)
# ═══════════════════════════════════════════════════════════════

def _find_all_php_files(directory: str) -> List[str]:
    """Find all .php files recursively in a directory."""
    php_files = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower().endswith('.php'):
                php_files.append(os.path.join(root, f))
    return php_files


def _build_dependency_map(php_files: List[str]) -> Dict:
    """
    Build a dependency map: for each file, who does it include and who includes it.
    
    Returns:
        {
            '/path/file.php': {
                'includes': ['/path/other.php', ...],   # files this file includes
                'included_by': ['/path/parent.php', ...], # files that include this file
                'has_input': bool,
                'has_token': bool,
                'token': str or None,
                'content_preview': str,  # first meaningful line
            }
        }
    """
    dep_map = {}
    
    # First pass: read all files and extract their includes + properties
    for fp in php_files:
        content = _read_file_safe(fp)
        if content is None:
            continue
        
        base_dir = os.path.dirname(fp)
        includes = _extract_includes(content, base_dir)
        
        token_match = TOKEN_PATTERN.search(content)
        
        dep_map[fp] = {
            'includes': includes,
            'included_by': [],
            'has_input': _has_input_pattern(content),
            'has_token': bool(token_match),
            'token': token_match.group(0) if token_match else None,
        }
    
    # Second pass: build reverse references (included_by)
    for fp, info in dep_map.items():
        for included_file in info['includes']:
            if included_file in dep_map:
                dep_map[included_file]['included_by'].append(fp)
    
    return dep_map


def _find_entry_points(dep_map: Dict, project_dir: str) -> List[Dict]:
    """
    Find entry points: files that are NOT included by any other file,
    AND have php://input somewhere in their include chain.
    
    Returns list of entry point dicts sorted by relevance.
    """
    entry_points = []
    
    for fp, info in dep_map.items():
        # Entry point = not included by anyone else
        if len(info['included_by']) > 0:
            continue
        
        # Check if this file or its chain has php://input
        visited: Set[str] = set()
        trace = _trace_includes(fp, visited)
        
        if not trace['has_input']:
            continue
        
        # Count how many files this entry point manages
        chain_size = len(trace['chain'])
        
        # Score: prefer files that include more things (project managers)
        score = chain_size * 10
        if info['has_input']:
            score += 5  # Bonus if it directly has input
        if info['has_token']:
            score += 3  # Bonus if it has the token
        
        rel_path = os.path.relpath(fp, project_dir)
        
        entry_points.append({
            'path': fp,
            'rel_path': rel_path,
            'has_input_direct': info['has_input'],
            'has_token_direct': info['has_token'],
            'token': trace.get('token_source'),
            'chain': trace['chain'],
            'chain_size': chain_size,
            'score': score,
            'input_source': trace['input_source'],
            'token_source': trace['token_source'],
        })
    
    # Also check standalone files (has input + not included by anyone)
    # They might not include anything either — single-file bots
    
    # Sort by score descending (best entry point first)
    entry_points.sort(key=lambda x: x['score'], reverse=True)
    return entry_points


def _extract_token_from_chain(chain: List[str]) -> Optional[str]:
    """Extract the first token found in a chain of files."""
    for fp in chain:
        content = _read_file_safe(fp)
        if content:
            match = TOKEN_PATTERN.search(content)
            if match:
                return match.group(0)
    return None


def _group_bots(entry_points: List[Dict]) -> List[Dict]:
    """
    Group entry points into separate bots based on tokens.
    Each bot has a token and one or more entry points.
    """
    bots = {}  # token -> bot info
    no_token_entries = []
    
    for ep in entry_points:
        token = _extract_token_from_chain(ep['chain'])
        
        if not token:
            no_token_entries.append(ep)
            continue
        
        if token not in bots:
            bots[token] = {
                'token': token,
                'masked_token': f"{token[:8]}...{token[-4:]}",
                'entry_points': [],
            }
        
        ep['token_value'] = token
        bots[token]['entry_points'].append(ep)
    
    # Set the suggested entry for each bot (highest score)
    result = []
    for token, bot in bots.items():
        bot['suggested_entry'] = bot['entry_points'][0]  # Already sorted by score
        result.append(bot)
    
    # Add orphan entries (no token) as a separate group if they exist
    if no_token_entries:
        result.append({
            'token': None,
            'masked_token': None,
            'entry_points': no_token_entries,
            'suggested_entry': no_token_entries[0] if no_token_entries else None,
        })
    
    return result


def generate_execution_flow_html(entry_point: Dict, dep_map: Dict, project_dir: str) -> str:
    """
    Generate a beautiful HTML execution flow visualization for Telegram.
    Shows how files call each other with icons for input/token.
    
    Output format: HTML suitable for Telegram's blockquote expandable.
    """
    
    def _build_tree(fp: str, visited: Set[str], prefix: str = "", is_last: bool = True, depth: int = 0) -> str:
        if depth > MAX_INCLUDE_DEPTH or fp in visited:
            return ""
        
        visited.add(fp)
        rel = os.path.relpath(fp, project_dir)
        info = dep_map.get(fp, {})
        
        # Icons
        icons = []
        if info.get('has_input'):
            icons.append("📡")  # webhook receiver
        if info.get('has_token'):
            icons.append("🔑")  # has token
        
        icon_str = " ".join(icons)
        if icon_str:
            icon_str = f" {icon_str}"
        
        # Tree connector
        if depth == 0:
            connector = "⚡"
            line = f"{connector} <b>{rel}</b>{icon_str}\n"
        else:
            branch = "└── " if is_last else "├── "
            line = f"{prefix}{branch}{rel}{icon_str}\n"
        
        # Recurse into includes
        includes = [inc for inc in info.get('includes', []) if inc in dep_map]
        child_prefix = prefix + ("    " if is_last else "│   ")
        
        for i, inc_path in enumerate(includes):
            is_child_last = (i == len(includes) - 1)
            line += _build_tree(inc_path, visited, child_prefix, is_child_last, depth + 1)
        
        return line
    
    visited: Set[str] = set()
    tree = _build_tree(entry_point['path'], visited)
    
    # Legend
    legend = "📡 = يستقبل التحديثات  🔑 = يحتوي التوكن"
    
    html = (
        f"<b>⚙️ هيكل التشغيل:</b>\n"
        f"<blockquote expandable>"
        f"<code>{tree}</code>\n"
        f"{legend}"
        f"</blockquote>"
    )
    
    return html


def analyze_project(directory: str) -> Dict:
    """
    Analyze an entire PHP project directory to discover bots and entry points.
    
    Returns:
        {
            "bots": [
                {
                    "token": str,
                    "masked_token": str,
                    "entry_points": [...],
                    "suggested_entry": {...},
                }
            ],
            "total_php_files": int,
            "total_entry_points": int,
            "dep_map": {...},
            "execution_flow_html": str,  # HTML visualization
        }
    """
    php_files = _find_all_php_files(directory)
    
    if not php_files:
        return {
            'bots': [],
            'total_php_files': 0,
            'total_entry_points': 0,
            'dep_map': {},
            'execution_flow_html': '',
        }
    
    # Build dependency map
    dep_map = _build_dependency_map(php_files)
    
    # Find entry points
    entry_points = _find_entry_points(dep_map, directory)
    
    # Group into bots
    bots = _group_bots(entry_points)
    
    # Generate execution flow HTML for each bot
    flow_htmls = []
    for bot in bots:
        if bot.get('suggested_entry'):
            html = generate_execution_flow_html(
                bot['suggested_entry'], dep_map, directory
            )
            bot['execution_flow_html'] = html
            flow_htmls.append(html)
    
    # Combined flow HTML
    combined_html = "\n\n".join(flow_htmls) if flow_htmls else ""
    
    return {
        'bots': bots,
        'total_php_files': len(php_files),
        'total_entry_points': len(entry_points),
        'dep_map': dep_map,
        'execution_flow_html': combined_html,
    }


print("✅ Bot Detector module initialized.")

