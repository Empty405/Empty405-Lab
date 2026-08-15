#!/usr/bin/env python3
import json
from pathlib import Path

HERE=Path(__file__).parent
DATA=json.loads((HERE/'results'/'benchmark.json').read_text())['summaries']
SCOPES=('per_identity','attributed_cluster','global','proof_cost','oracle')
COLORS={'per_identity':'#ef4444','attributed_cluster':'#3b82f6','global':'#f59e0b','proof_cost':'#22c55e','oracle':'#a78bfa'}
W,H,L,T,PW,PH=920,570,80,60,780,400
def x(v): return L + (v.bit_length()-1)/6*PW
def y(v): return T+(1-v)*PH

def main():
 lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="#08131f"/>','<style>text{font-family:system-ui,sans-serif;fill:#dbeafe}.g{stroke:#294052}.a{stroke:#94a3b8;stroke-width:1.5}</style>','<text x="80" y="30" font-size="20" font-weight="700">B2: Sybil pool size vs aggregate exposure</text>','<text x="80" y="50" font-size="12">partition coordination · budget 0.25 · missing signals · 500 trials</text>']
 for t in (0,.25,.5,.75,1):
  lines += [f'<line class="g" x1="{L}" y1="{y(t)}" x2="{L+PW}" y2="{y(t)}"/>',f'<text x="{L-10}" y="{y(t)+4}" text-anchor="end" font-size="11">{t:.2f}</text>']
 for p in (1,2,4,8,16,32,64):
  lines += [f'<line class="g" x1="{x(p)}" y1="{T}" x2="{x(p)}" y2="{T+PH}"/>',f'<text x="{x(p)}" y="{T+PH+22}" text-anchor="middle" font-size="11">{p}</text>']
 lines += [f'<line class="a" x1="{L}" y1="{T+PH}" x2="{L+PW}" y2="{T+PH}"/>',f'<line x1="{L}" y1="{y(.25)}" x2="{L+PW}" y2="{y(.25)}" stroke="#fff" stroke-dasharray="6 5"/>']
 for i,scope in enumerate(SCOPES):
  rows=[r for r in DATA if r['ledger_scope']==scope and r['coordination']=='partition' and r['budget']==.25 and r['signal_quality']=='missing']; rows.sort(key=lambda r:r['pool_size'])
  pts=' '.join(f'{x(r["pool_size"]):.1f},{y(r["exposure"]):.1f}' for r in rows); c=COLORS[scope]
  lines.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="3"/>')
  for r in rows: lines.append(f'<circle cx="{x(r["pool_size"]):.1f}" cy="{y(r["exposure"]):.1f}" r="3.5" fill="{c}"/>')
  lx=80+(i//2)*280; ly=500+(i%2)*25
  lines += [f'<line x1="{lx}" y1="{ly}" x2="{lx+28}" y2="{ly}" stroke="{c}" stroke-width="4"/>',f'<text x="{lx+36}" y="{ly+4}" font-size="12">{scope}</text>']
 lines += ['<text x="470" y="560" text-anchor="middle" font-size="12">concurrent identities (log2 spacing)</text>','<text x="18" y="260" text-anchor="middle" font-size="12" transform="rotate(-90 18 260)">aggregate exposure</text>','</svg>']
 (HERE/'results'/'figure-b2-sybil-exposure.svg').write_text('\n'.join(lines)+'\n')
if __name__=='__main__': main()
