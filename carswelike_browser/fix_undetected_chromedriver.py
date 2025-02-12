#!/usr/bin/env python3
import os
import sysconfig

_already_fixed = False

def fix_undetected_chromedriver():
    """
    Patches undetected_chromedriver's patcher.py to replace distutils with packaging
    so it works on Python 3.12+ (where distutils may be missing).
    """

    global _already_fixed
    if _already_fixed:
        return

    # 1. Find the path to site-packages in the current environment
    site_packages_dir = sysconfig.get_paths().get("purelib")
    if not site_packages_dir or not os.path.isdir(site_packages_dir):
        print("[fix_undetected_chromedriver] Could not find site-packages directory. Exiting.")
        return

    # 2. Build full path to undetected_chromedriver/patcher.py
    patcher_file = os.path.join(site_packages_dir, "undetected_chromedriver", "patcher.py")
    if not os.path.isfile(patcher_file):
        print(f"[fix_undetected_chromedriver] patcher.py not found at {patcher_file}")
        return

    print(f"[fix_undetected_chromedriver] Located patcher.py at: {patcher_file}")

    # 3. Read its content
    with open(patcher_file, "r", encoding="utf-8") as f:
        original_content = f.read()

    content = original_content

    # Replace distutils references with packaging.version
    content = content.replace(
        "from distutils.version import LooseVersion",
        "from packaging.version import Version as LooseVersion"
    )
    # Convert .version[...] -> .release[...]
    content = content.replace(".version[", ".release[")
    # Convert .vstring -> .public
    content = content.replace(".vstring", ".public")

    if content != original_content:
        # 4. Backup the original file, then write the patched content
        backup_path = patcher_file + ".bak"
        print(f"[fix_undetected_chromedriver] Backing up original to {backup_path}")
        with open(backup_path, "w", encoding="utf-8") as bf:
            bf.write(original_content)

        print("[fix_undetected_chromedriver] Applying replacements...")
        with open(patcher_file, "w", encoding="utf-8") as pf:
            pf.write(content)

        print("[fix_undetected_chromedriver] Done patching.")
    else:
        print("[fix_undetected_chromedriver] No changes needed (already patched?).")

    _already_fixed = True

if __name__ == "__main__":
    # 5. Run the patch
    fix_undetected_chromedriver()

    # 6. Optionally, try importing undetected_chromedriver after patching
    try:
        import undetected_chromedriver as uc
        print("[fix_undetected_chromedriver] Successfully imported undetected_chromedriver after patch.")
    except ModuleNotFoundError as e:
        print("[fix_undetected_chromedriver] Failed to import undetected_chromedriver:", e)
    except Exception as e:
        print("[fix_undetected_chromedriver] Some other error occurred:", e)
