#!/usr/bin/env python3
"""
Patch undetected_chromedriver so it does not rely on distutils (missing in Python 3.12).
"""

import os
import sysconfig

_already_fixed = False

def fix_undetected_chromedriver():
    """
    Locate undetected_chromedriver/patcher.py and replace 'distutils.version'
    references with 'packaging.version'.
    """
    global _already_fixed
    if _already_fixed:
        return  # Only do this once

    site_packages_dir = sysconfig.get_paths().get("purelib")
    if not (site_packages_dir and os.path.isdir(site_packages_dir)):
        print("[fix_undetected_chromedriver] Could not find site-packages directory.")
        return

    patcher_file = os.path.join(site_packages_dir, "undetected_chromedriver", "patcher.py")
    if not os.path.isfile(patcher_file):
        print(f"[fix_undetected_chromedriver] patcher.py not found at {patcher_file}")
        return

    # Read original content
    with open(patcher_file, "r", encoding="utf-8") as f:
        original_content = f.read()
    content = original_content

    # Replace references to distutils.version.LooseVersion with packaging.version.Version
    content = content.replace(
        "from distutils.version import LooseVersion",
        "from packaging.version import Version as LooseVersion"
    )
    # If the code uses .version[...] -> .release[...]
    content = content.replace(".version[", ".release[")
    # If the code uses .vstring -> .public
    content = content.replace(".vstring", ".public")

    # If changes were made, write them out
    if content != original_content:
        backup_path = patcher_file + ".bak"
        print(f"[fix_undetected_chromedriver] Backing up original to {backup_path}")
        with open(backup_path, "w", encoding="utf-8") as bf:
            bf.write(original_content)

        print("[fix_undetected_chromedriver] Patching patcher.py...")
        with open(patcher_file, "w", encoding="utf-8") as pf:
            pf.write(content)

        print("[fix_undetected_chromedriver] Done.")
    else:
        print("[fix_undetected_chromedriver] No changes needed (already patched?).")

    _already_fixed = True

if __name__ == "__main__":
    fix_undetected_chromedriver()
    try:
        import undetected_chromedriver
        print("[fix_undetected_chromedriver] Import successful after patch.")
    except Exception as e:
        print("[fix_undetected_chromedriver] Still cannot import:", e)
