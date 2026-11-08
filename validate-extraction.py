#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit extraction without assuming an Android source checkout is present."""
import argparse, collections, hashlib, json, re, subprocess, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
p=argparse.ArgumentParser(); p.add_argument('dump',type=Path); p.add_argument('vendor',type=Path); p.add_argument('--report',type=Path,required=True); a=p.parse_args()
here=Path(__file__).resolve().parent
paths=[l.lstrip('-').split(';')[0] for l in (here/'proprietary-files.txt').read_text().splitlines() if l and not l.startswith('#')]
missing=[]; changed=[]; elfs={}; providers=collections.defaultdict(list)
for rel in paths:
    src=a.dump/rel; dst=a.vendor/'proprietary'/rel
    if not dst.is_file(): missing.append(rel); continue
    if hashlib.sha256(src.read_bytes()).digest()!=hashlib.sha256(dst.read_bytes()).digest(): changed.append(rel)
    with dst.open('rb') as f: header=f.read(20)
    if header[:4]!=b'\x7fELF': continue
    out=subprocess.run(['readelf','-d',str(dst)],capture_output=True,text=True,check=True).stdout
    deps=re.findall(r'\(NEEDED\).*?\[(.*?)\]',out)
    soname=re.findall(r'\(SONAME\).*?\[(.*?)\]',out)
    arch=header[4]; elfs[rel]=(arch,deps)
    if '/lib/' in rel or '/lib64/' in rel:
        providers[(arch,Path(rel).name)].append(rel)
        for n in soname: providers[(arch,n)].append(rel)
external=collections.defaultdict(list)
for rel,(arch,deps) in elfs.items():
    for dep in deps:
        if (arch,dep) not in providers: external[dep].append(rel)
# Locate external filenames in stock system partitions; this is evidence of
# a stock provider, NOT proof of a corresponding Lineage source module.
stock=collections.defaultdict(list)
for part in ('system','system_ext','product'):
    for f in (a.dump/part).rglob('*'):
        if f.name in external and f.is_file(): stock[f.name].append(str(f.relative_to(a.dump)))
xml=[]; xml_errors=[]; apex=[]
for part in ('vendor','odm'):
    for f in (a.dump/part/'etc/vintf').rglob('*.xml'):
        try:
            root=ET.parse(f).getroot(); xml.append({'path':str(f.relative_to(a.dump)),'attributes':root.attrib,'hals':[e.findtext('name') for e in root.findall('hal')]})
        except ET.ParseError as e: xml_errors.append([str(f),str(e)])
    for f in (a.dump/part/'apex').glob('*.apex'):
        with zipfile.ZipFile(f) as z: apex.append({'path':str(f.relative_to(a.dump)),'members':z.namelist(),'payload_vintf_checked':False})
bp=(a.vendor/'Android.bp').read_text(); names=re.findall(r'^\s*name: "([^"]+)"',bp,re.M)
links=json.loads((here/'stock-symlinks.json').read_text()); unresolved_links=[]
for rel,target in links:
    if target not in paths: unresolved_links.append([rel,target])
report={'files':len(paths),'elf_files':len(elfs),'missing':missing,'changed':changed,'duplicate_bp_modules':[n for n,c in collections.Counter(names).items() if c>1],'generated_modules':len(names),'external_elf_dependencies':{n:{'consumers':sorted(set(v)),'stock_filename_providers':stock[n]} for n,v in sorted(external.items())},'vintf':xml,'xml_errors':xml_errors,'apex':apex,'symlinks_not_backed_by_selected_file':unresolved_links}
a.report.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('external_elf_dependencies','vintf','apex','symlinks_not_backed_by_selected_file')},indent=2)); print('External ELF names:',len(external),'unselected symlink targets:',len(unresolved_links))
assert not missing and not changed and not report['duplicate_bp_modules'] and not xml_errors
