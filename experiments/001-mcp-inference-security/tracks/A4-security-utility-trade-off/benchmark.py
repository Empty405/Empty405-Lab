#!/usr/bin/env python3
"""Unified A4 Pareto benchmark for tested disclosure configurations."""
from __future__ import annotations
import argparse, csv, gzip, json, math, random, statistics
from dataclasses import asdict, dataclass
from pathlib import Path

CELLS=96; WINDOW=60
TASKS=("threshold","category","planning","exact","aggregate")
PROFILES={
 "balanced":dict.fromkeys(TASKS,.2),
 "exact-critical":{"threshold":.125,"category":.125,"planning":.125,"exact":.5,"aggregate":.125},
 "category-first":{"threshold":.2,"category":.5,"planning":.1,"exact":.1,"aggregate":.1},
 "aggregate-planning":{"threshold":.05,"category":.05,"planning":.4,"exact":.1,"aggregate":.4},
 "threshold-first":{"threshold":.5,"category":.2,"planning":.1,"exact":.1,"aggregate":.1},
 "coarse-service":{"threshold":.2,"category":.3,"planning":.1,"exact":0.0,"aggregate":.4},
}
DEADLINES={"patient":math.inf,"long":600,"medium":180,"short":60}
ADAPTIVE={"adaptive_conservative":(.10,.25,.40,.55,.70),"adaptive_balanced":(.20,.40,.60,.75,.90),"adaptive_permissive":(.30,.50,.70,.85,.95)}
CONFIGS=["release_all","deny_all",*[f"rate_{n}" for n in (5,10,20)],
         *[f"quota_{x:.2f}" for x in (.25,.50,.75)],*[f"coverage_{x:.2f}" for x in (.25,.50,.75)],
         "hybrid_10_0.50",*ADAPTIVE]

@dataclass
class Row:
 trial:int; profile:str; deadline:str; policy:str; risk:float; exact_recovery:float
 macro_utility:float; minimum_task_utility:float; weighted_utility:float
 p95_delay:float; deadline_success:float; ledger_bytes:int; decision_ops:int

def category(v:int)->str:return "low" if v<34 else("medium" if v<67 else "high")

def level_interval(v:int,level:str):
 if level=="L0":return(v,v)
 if level=="L1":lo=v//10*10;return(lo,min(100,lo+9))
 if level=="L2":lo=v//20*20;return(lo,min(100,lo+19))
 if level=="L3":return(0,33) if v<34 else((34,66) if v<67 else(67,100))
 return None

def useful(task:str,level:str,interval,value:int)->bool:
 if level=="L5":return False
 if task=="exact":return interval==(value,value)
 if task=="planning":return interval is not None and interval[1]-interval[0]<=20
 if task=="category":return interval is not None and category((interval[0]+interval[1])/2)==category(value)
 if task=="threshold":return interval is not None and(interval[1]<50 or interval[0]>=50)
 if task=="aggregate":return level!="L5"
 raise ValueError(task)

def adaptive_level(progress:float,thresholds):
 for i,b in enumerate(thresholds):
  if progress<=b:return f"L{i}"
 return"L5"

def policy_decision(name:str,step:int,deadline:float):
 progress=step/CELLS; delay=0.0; level="L0"; ledger=0; ops=1
 if name=="release_all":pass
 elif name=="deny_all":level="L5"
 elif name.startswith("rate_"):
  rate=int(name.split("_")[1]);delay=(step//rate)*WINDOW
  if delay>deadline:level="L5"
 elif name.startswith("quota_"):
  cap=float(name.split("_")[1]);level="L0" if progress<cap else"L5";ledger=8;ops=2
 elif name.startswith("coverage_"):
  cap=float(name.split("_")[1]);level="L0" if progress<cap else"L5";ledger=min(step+1,math.ceil(cap*CELLS))*16;ops=3
 elif name=="hybrid_10_0.50":
  delay=(step//10)*WINDOW;level="L0" if progress<.5 and delay<=deadline else"L5";ledger=min(step+1,48)*16;ops=4
 elif name in ADAPTIVE:
  level=adaptive_level(progress,ADAPTIVE[name]);ledger=(step+1)*16;ops=5
 else:raise ValueError(name)
 return level,delay,ledger,ops

def run(trial:int,profile:str,deadline_name:str,policy:str,seed:int)->Row:
 rng=random.Random(seed+trial);values=[rng.randint(0,100) for _ in range(CELLS)];order=list(range(CELLS));rng.shuffle(order)
 task_hits={t:0 for t in TASKS};widths=[];exact=0;delays=[];released=0;ledger=ops=0
 deadline=DEADLINES[deadline_name]
 for step,cell in enumerate(order):
  level,delay,ledger_now,ops_now=policy_decision(policy,step,deadline);ledger=max(ledger,ledger_now);ops+=ops_now
  interval=level_interval(values[cell],level);widths.append(100 if interval is None else interval[1]-interval[0]);exact+=interval==(values[cell],values[cell])
  if level!="L5":released+=1;delays.append(delay)
  for task in TASKS:task_hits[task]+=useful(task,level,interval,values[cell])
 scores={t:task_hits[t]/CELLS for t in TASKS};macro=statistics.fmean(scores.values());weighted=sum(PROFILES[profile][t]*scores[t] for t in TASKS)
 p95=0.0 if not delays else sorted(delays)[min(len(delays)-1,math.ceil(.95*len(delays))-1)]
 return Row(trial,profile,deadline_name,policy,statistics.fmean(1-w/100 for w in widths),exact/CELLS,
            macro,min(scores.values()),weighted,p95,released/CELLS,ledger,ops)

def mean_rows(rows):
 groups={}
 for row in rows:groups.setdefault((row.profile,row.deadline,row.policy),[]).append(row)
 out=[]
 for (profile,deadline,policy),ss in groups.items():
  item={"profile":profile,"deadline":deadline,"policy":policy,"runs":len(ss)}
  for f in ("risk","exact_recovery","macro_utility","minimum_task_utility","weighted_utility","p95_delay","deadline_success","ledger_bytes","decision_ops"):
   item[f]=statistics.fmean(getattr(r,f) for r in ss)
  out.append(item)
 return out

def dominates(a,b,eps=1e-9):
 minimize=("risk","p95_delay","ledger_bytes","decision_ops");maximize=("weighted_utility","minimum_task_utility","deadline_success")
 no_worse=all(a[k]<=b[k]+eps for k in minimize) and all(a[k]>=b[k]-eps for k in maximize)
 better=any(a[k]<b[k]-eps for k in minimize) or any(a[k]>b[k]+eps for k in maximize)
 return no_worse and better

def frontiers(summary):
 output=[]
 for profile in PROFILES:
  for deadline in DEADLINES:
   ss=[r for r in summary if r["profile"]==profile and r["deadline"]==deadline]
   for row in ss:
    dominators=[x["policy"] for x in ss if x is not row and dominates(x,row)]
    output.append({"profile":profile,"deadline":deadline,"policy":row["policy"],"frontier":not dominators,"dominators":dominators})
 return output

def main():
 p=argparse.ArgumentParser();p.add_argument("--runs",type=int,default=1000);p.add_argument("--seed",type=int,default=40504);p.add_argument("--output",type=Path,default=Path(__file__).with_name("results"));a=p.parse_args()
 rows=[run(t,pr,d,c,a.seed) for t in range(a.runs) for pr in PROFILES for d in DEADLINES for c in CONFIGS]
 summary=mean_rows(rows);front=frontiers(summary);a.output.mkdir(parents=True,exist_ok=True)
 for profile in PROFILES:
  selected=(r for r in rows if r.profile==profile)
  with gzip.open(a.output/f"trials-{profile}.csv.gz","wt",newline="",encoding="utf-8") as f:
   w=csv.DictWriter(f,fieldnames=list(asdict(rows[0])));w.writeheader();w.writerows(asdict(r) for r in selected)
 counts={p:sum(x["frontier"] for x in front if x["policy"]==p) for p in CONFIGS}
 payload={"version":"A4-v0.1","runs":a.runs,"root_seed":a.seed,"configurations":len(CONFIGS),"profiles":list(PROFILES),"deadlines":DEADLINES,"trial_rows":len(rows),"summary":summary,"frontier":front,"frontier_counts":counts}
 (a.output/"benchmark.json").write_text(json.dumps(payload,indent=2)+"\n");print(json.dumps(counts,indent=2))

if __name__=="__main__":main()
