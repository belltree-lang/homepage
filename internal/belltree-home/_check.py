# -*- coding: utf-8 -*-
# 公開前チェック: リンク切れ・外部参照逃げ・仮置き#・canonical/GA4/FAB の網羅検査
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
errors, warns = [], []
pages = 0

attr_re = re.compile(r'(?:href|src)="([^"]+)"')

for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for f in files:
        if not f.endswith(".html"):
            continue
        pages += 1
        path = os.path.join(root, f)
        rel = os.path.relpath(path, BASE)
        with open(path, "r", encoding="utf-8") as fh:
            s = fh.read()
        # 仮置き
        n_stub = len(re.findall(r'href="#(?:final)?"', s))
        if n_stub:
            errors.append(f"{rel}: 仮置きリンク href=\"#\" が {n_stub} 件")
        # 参照解決
        for url in attr_re.findall(s):
            if url.startswith(("http://", "https://", "tel:", "mailto:", "data:", "javascript:", "#")):
                continue
            target = url.split("#")[0].split("?")[0]
            if not target:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                errors.append(f"{rel}: リンク切れ -> {url}")
            else:
                try:
                    outside = os.path.relpath(resolved, BASE).startswith("..")
                except ValueError:
                    outside = True
                if outside:
                    errors.append(f"{rel}: 公開フォルダ外を参照 -> {url}")
        # 必須要素
        if "thanks" not in rel:
            if 'rel="canonical" href="https://belltree1102.com' not in s:
                warns.append(f"{rel}: canonical なし/不正")
            if "G-RQRJ45S3V3" not in s:
                warns.append(f"{rel}: GA4 なし")
            if "fab-call" not in s:
                warns.append(f"{rel}: 追従電話ボタンなし")

print(f"checked pages: {pages}")
print(f"errors: {len(errors)}")
for e in errors: print("  ERR", e)
print(f"warns: {len(warns)}")
for w in warns: print("  WARN", w)
if not errors and not warns:
    print("ALL CLEAN")
