#!/usr/bin/env python3
"""
Patch undetected_chromedriver so it does not rely on distutils.

Usage:
    from .fix_undetected_chromedriver import fix_undetected_chromedriver
    fix_undetected_chromedriver()
    import undetected_chromedriver
"""

import os
import sysconfig

_already_fixed = False

def fix_undetected_chromedriver():
    """
    Locate patcher.py inside undetected_chromedriver and replace distutils.version
    usage with packaging.version. This avoids the 'No module named distutils' error
    on Python 3.12.
    """
    global _already_fixed
    if _already_fixed:
        return

    # 1. Find the site-packages path
    site_packages_dir = sysconfig.get_paths().get("purelib")
    if not site_packages_dir or not os.path.isdir(site_packages_dir):
        print("[fix_undetected_chromedriver] Could not find site-packages directory. Aborting patch.")
        return

    # 2. Build the full path to undetected_chromedriver/patcher.py
    patcher_file = os.path.join(site_packages_dir, "undetected_chromedriver", "patcher.py")
    if not os.path.isfile(patcher_file):
        print(f"[fix_undetected_chromedriver] patcher.py not found at {patcher_file}")
        return

    print(f"[fix_undetected_chromedriver] Located patcher.py at: {patcher_file}")

    # 3. Read existing content
    with open(patcher_file, "r", encoding="utf-8") as f:
        original_content = f.read()
    content = original_content

    # 4. Replace distutils-related code with packaging
    content = content.replace(
        "from distutils.version import LooseVersion",
        "from packaging.version import Version as LooseVersion"
    )
    # For references to .version[...] -> .release[...]
    content = content.replace(".version[", ".release[")
    # For references to .vstring -> .public
    content = content.replace(".vstring", ".public")

    # 5. If any changes were made, backup and overwrite
    if content != original_content:
        backup_path = patcher_file + ".bak"
        print(f"[fix_undetected_chromedriver] Backing up original file to {backup_path}")
        with open(backup_path, "w", encoding="utf-8") as bf:
            bf.write(original_content)

        print("[fix_undetected_chromedriver] Writing patched content...")
        with open(patcher_file, "w", encoding="utf-8") as pf:
            pf.write(content)

        print("[fix_undetected_chromedriver] Patching complete.")
    else:
        print("[fix_undetected_chromedriver] No changes needed (already patched?).")

    _already_fixed = True

if __name__ == "__main__":
    fix_undetected_chromedriver()
    # Optional: test importing after patch
    try:
        import undetected_chromedriver
        print("[fix_undetected_chromedriver] Successfully imported undetected_chromedriver after patch.")
    except Exception as e:
        print("[fix_undetected_chromedriver] Failed to import undetected_chromedriver:", e)
