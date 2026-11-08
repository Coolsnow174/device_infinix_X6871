#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
import argparse, json, re, subprocess
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('kernel',type=Path); a=p.parse_args()
all_modules={f.name:f for f in a.kernel.rglob('*.ko')}; missing=[]; deps=[]
for depfile in a.kernel.rglob('modules.dep'):
    for line in depfile.read_text().splitlines():
        for token in line.replace(':',' ').split():
            if Path(token).name not in all_modules: missing.append([str(depfile),token])
internal_names=set()
for f in all_modules.values():
    internal_names.add(subprocess.run(['modinfo','-F','name',str(f)],capture_output=True,text=True).stdout.strip().replace('-','_'))
for f in all_modules.values():
    result=subprocess.run(['modinfo','-F','depends',str(f)],capture_output=True,text=True)
    for name in result.stdout.strip().split(','):
        if name and name.replace('-','_') not in internal_names: deps.append([str(f),name])
report={'unique_module_basenames':len(all_modules),'missing_modules_dep_paths':missing,'module_dependencies_not_in_prebuilts':deps,'abi_note':'Vendor/ODM modules have a different build suffix than GKI. modversions CRC compatibility requires full kernel symbol/CRC validation or device testing; vermagic alone is not proof.'}
(a.kernel/'module-audit.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
