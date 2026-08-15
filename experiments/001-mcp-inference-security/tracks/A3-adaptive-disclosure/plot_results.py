#!/usr/bin/env python3
import json
from pathlib import Path

root=Path(__file__).parent; data=json.loads((root/'results'/'benchmark.json').read_text())
front=data['matched_frontier']; w,h=900,470
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">','<rect width="100%" height="100%" fill="#0f172a"/>',
       '<text x="40" y="35" fill="#e2e8f0" font-family="sans-serif" font-size="22" font-weight="bold">A3 matched-risk macro utility</text>']
for pct in (0,.2,.4,.6,.8,1):
 y=390-320*pct; parts += [f'<line x1="70" y1="{y}" x2="860" y2="{y}" stroke="#334155"/>',f'<text x="32" y="{y+5}" fill="#94a3b8" font-family="sans-serif" font-size="12">{pct:.1f}</text>']
for i,row in enumerate(front):
 x=120+i*250
 for off,key,color in ((0,'adaptive_utility','#10b981'),(70,'hard_utility','#8b5cf6')):
  val=row[key]; bh=320*val
  parts.append(f'<rect x="{x+off}" y="{390-bh}" width="55" height="{bh}" fill="{color}" rx="4"/>')
  parts.append(f'<text x="{x+off+27}" y="{380-bh}" text-anchor="middle" fill="#f8fafc" font-family="sans-serif" font-size="13">{val:.3f}</text>')
 parts.append(f'<text x="{x+62}" y="420" text-anchor="middle" fill="#cbd5e1" font-family="sans-serif" font-size="12">{row["adaptive"].replace("adaptive_","")}</text>')
parts += ['<rect x="590" y="445" width="15" height="15" fill="#10b981"/><text x="615" y="457" fill="#cbd5e1" font-family="sans-serif" font-size="12">adaptive</text>',
          '<rect x="700" y="445" width="15" height="15" fill="#8b5cf6"/><text x="725" y="457" fill="#cbd5e1" font-family="sans-serif" font-size="12">matched hard block</text></svg>']
(root/'results'/'figure-a3-matched-risk.svg').write_text('\n'.join(parts)+'\n')
