#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).parent;p=json.loads((root/'results'/'benchmark.json').read_text());counts=p['frontier_counts']
items=sorted(counts.items(),key=lambda x:(-x[1],x[0]));w,h=1100,650;left,top,ch=85,60,430
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">','<rect width="100%" height="100%" fill="#0f172a"/>','<text x="40" y="35" fill="#e2e8f0" font-family="sans-serif" font-size="22" font-weight="bold">A4 frontier inclusion across 24 workload/deadline contexts</text>']
for n in (0,6,12,18,24):
 y=top+ch-ch*n/24;parts += [f'<line x1="{left}" y1="{y}" x2="1070" y2="{y}" stroke="#334155"/>',f'<text x="45" y="{y+5}" fill="#94a3b8" font-family="sans-serif" font-size="12">{n}</text>']
bw=48;gap=17
for i,(name,val) in enumerate(items):
 x=left+15+i*(bw+gap);bh=ch*val/24;color='#10b981' if val==24 else('#eab308' if val else '#ef4444')
 parts.append(f'<rect x="{x}" y="{top+ch-bh}" width="{bw}" height="{bh}" fill="{color}" rx="3"/>')
 parts.append(f'<text transform="translate({x+24},520) rotate(55)" fill="#cbd5e1" font-family="sans-serif" font-size="10">{name}</text>')
parts.append('</svg>');(root/'results'/'figure-a4-frontier-counts.svg').write_text('\n'.join(parts)+'\n')
