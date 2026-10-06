#!/usr/bin/env python3
import os
import re
import glob

FONT_TAGS = """    <!-- Google Fonts Preconnect & Ubuntu Font Loading -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap" rel="stylesheet">
"""

TAILWIND_WINDOW_CONFIG = """    <!-- Tailwind CSS -->
    <script>
        window.tailwind = {
            config: {
                darkMode: 'class',
                theme: {
                    extend: {
                        fontFamily: {
                            sans: ['Ubuntu', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
                        }
                    }
                }
            }
        };
    </script>
    <script src="https://cdn.tailwindcss.com"></script>"""

TAILWIND_CONFIG_BLOCK = """    <!-- Tailwind CSS & Styles (Configured to ignore OS dark mode) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Ubuntu', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
                    }
                }
            }
        };
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
    </script>"""

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip files that shouldn't be processed
    if 'cdn.tailwindcss.com' not in content:
        return False, "No tailwind"

    modified = False

    # 1. Update pattern with window.tailwind
    # Pattern 1:
    # <script>\s*window\.tailwind = { config: { darkMode: 'class' } };\s*</script>\s*<script src="https://cdn\.tailwindcss\.com"></script>
    p1 = re.compile(
        r'(\s*<!--\s*Tailwind CSS\s*-->\s*)?<script>\s*window\.tailwind\s*=\s*\{\s*config:\s*\{\s*darkMode:\s*[\'"]class[\'"]\s*\}\s*\};\s*</script>\s*<script src=[\'"]https://cdn\.tailwindcss\.com[\'"]></script>',
        re.DOTALL
    )

    if p1.search(content):
        # Insert font tags right before tailwind if not already present
        replacement = ""
        if "fonts.googleapis.com" not in content:
            replacement += "\n" + FONT_TAGS + "\n"
        replacement += TAILWIND_WINDOW_CONFIG
        content = p1.sub(replacement, content, count=1)
        modified = True

    # Pattern 2: locations pattern with tailwind.config
    p2 = re.compile(
        r'(\s*<!--\s*Tailwind CSS & Styles[^\>]*-->\s*)?<script src=[\'"]https://cdn\.tailwindcss\.com[\'"]></script>\s*<script>\s*tailwind\.config\s*=\s*\{\s*darkMode:\s*[\'"]class[\'"]\s*\};\s*document\.documentElement\.classList\.remove\([\'"]dark[\'"]\);\s*document\.documentElement\.classList\.add\([\'"]light[\'"]\);\s*</script>',
        re.DOTALL
    )

    if p2.search(content):
        replacement = ""
        if "fonts.googleapis.com" not in content:
            replacement += "\n" + FONT_TAGS + "\n"
        replacement += TAILWIND_CONFIG_BLOCK
        content = p2.sub(replacement, content, count=1)
        modified = True

    # Pattern 3: best-web-design-companies-in-kenya (window.tailwind inside strict light script)
    if not modified and 'window.tailwind = { config: { darkMode: \'class\' } };' in content:
        # replace just the window.tailwind assignment
        new_tw = """window.tailwind = {
            config: {
                darkMode: 'class',
                theme: {
                    extend: {
                        fontFamily: {
                            sans: ['Ubuntu', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
                        }
                    }
                }
            }
        };"""
        content = content.replace("window.tailwind = { config: { darkMode: 'class' } };", new_tw)
        if "fonts.googleapis.com" not in content:
            # Insert before <script src="https://cdn.tailwindcss.com"></script>
            content = content.replace(
                '<script src="https://cdn.tailwindcss.com"></script>',
                FONT_TAGS + '    <script src="https://cdn.tailwindcss.com"></script>'
            )
        modified = True

    # Ensure font tags are present if somehow missed
    if "fonts.googleapis.com" not in content and "</head>" in content:
        content = content.replace(
            '<link rel="stylesheet" href="css/styles.css',
            FONT_TAGS + '    <link rel="stylesheet" href="css/styles.css'
        ).replace(
            '<link rel="stylesheet" href="../css/styles.css',
            FONT_TAGS + '    <link rel="stylesheet" href="../css/styles.css'
        )
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, "Updated"
    return False, "No match"

def main():
    html_files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('node_modules/')]
    updated_count = 0
    for f in html_files:
        success, reason = process_html_file(f)
        if success:
            updated_count += 1
            print(f"Updated: {f}")
        else:
            print(f"Skipped: {f} ({reason})")
    print(f"\nDone! Updated {updated_count}/{len(html_files)} files.")

if __name__ == '__main__':
    main()
