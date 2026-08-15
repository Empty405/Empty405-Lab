#!/usr/bin/env python3
import json
from pathlib import Path
HERE=Path(__file__).parent;DATA=json.loads((HERE/'results'/'benchmark.json').read_text())['summaries']
M=('local','central','eventual','signed_token','sketch','oracle');C={'local':'#ef4444','central':'#f59e0b','eventual':'#3b82f6','signed_token':'#22c55e','sketch':'#06b6d4','oracle':'#a78bfa'}
W,H,L,T,PW,PH=940,590,80,60,800,410
def x(v):return L+(v.bit_length()-1)/5*PW
def y(v):return T+(1-v)*PH
def main():
 lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="#08131f"/>','<style>text{font-family:system-ui,sans-serif;fill:#dbeafe}.g{stroke:#294052}</style>','<text x="80" y="30" font-size="20" font-weight="700">B5: cross-server exposure under delayed synchronization</text>','<text x="80" y="50" font-size="12">disjoint outputs · budget 0.25 · fixed 96 requests · 450 trials</text>']
 for t in (0,.25,.5,.75,1):lines += [f'<line class="g" x1="{L}" y1="{y(t)}" x2="{L+PW}" y2="{y(t)}"/>',f'<text x="{L-10}" y="{y(t)+4}" text-anchor="end" font-size="11">{t:.2f}</text>']
 for n in (1,2,4,8,16,32):lines += [f'<line class="g" x1="{x(n)}" y1="{T}" x2="{x(n)}" y2="{T+PH}"/>',f'<text x="{x(n)}" y="{T+PH+22}" text-anchor="middle" font-size="11">{n}</text>']
 lines.append(f'<line x1="{L}" y1="{y(.25)}" x2="{L+PW}" y2="{y(.25)}" stroke="#fff" stroke-dasharray="6 5"/>')
 for i,m in enumerate(M):
  rows=[r for r in DATA if r['accounting_model']==m and r['output_overlap']=='disjoint' and r['sync_condition']=='delayed' and r['budget']==.25];rows.sort(key=lambda r:r['server_count']);c=C[m]
  pts=' '.join(f'{x(r["server_count"]):.1f},{y(r["aggregate_exposure"]):.1f}' for r in rows);lines.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="3"/>')
  for r in rows:lines.append(f'<circle cx="{x(r["server_count"]):.1f}" cy="{y(r["aggregate_exposure"]):.1f}" r="3.5" fill="{c}"/>')
  lx=80+(i//2)*280;ly=510+(i%2)*25;lines += [f'<line x1="{lx}" y1="{ly}" x2="{lx+28}" y2="{ly}" stroke="{c}" stroke-width="4"/>',f'<text x="{lx+36}" y="{ly+4}" font-size="12">{m}</text>']
 lines += ['<text x="480" y="580" text-anchor="middle" font-size="12">server count (log2 spacing)</text>','</svg>'];(HERE/'results'/'figure-b5-cross-server.svg').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
