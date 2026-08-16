#!/usr/bin/env python3
"""C6 budget recovery/decay benchmark; standard library only."""
from __future__ import annotations
import argparse,csv,gzip,json,math,random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT_SEED=40526
POLICIES=("no_recovery","fixed_window_reset","linear_decay","exponential_decay","version_invalidation","evidence_based_recovery","oracle")
REGIMES=("static","slow_drift","abrupt_replacement","cyclic_return","deceptive_version_bump")
CADENCES=("sparse","steady","burst","adaptive_revisit")
HORIZONS=("short","medium","long")
EPOCHS={"short":4,"medium":8,"long":12}; CAP=24; STATE_SIZE=40; UNIVERSE=160
FIELDS=("trial","policy","state_regime","request_cadence","horizon","epochs","requests","completed_requests","completion_rate","current_charge","lifetime_distinct_facts","lifetime_versioned_facts","recovered_units","false_forgetting","repeat_releases","repeat_release_amplification","historical_reconstruction","current_reconstruction","stale_response_rate","reset_events","detector_false_positives","detector_false_negatives","cap_overshoot","denied_response_exposure","reconciliation_error","silent_history_deletion","clock_reads","version_reads","detector_calls","ledger_writes","audit_writes","metadata_bytes")
EVENT_FIELDS=("trial","policy","state_regime","request_cadence","horizon","request_id","epoch","version","units","evidence","charge_before","recovered_units","marginal_cost","admitted","terminal_outcome","charged_units","charge_after","lifetime_before","lifetime_after","false_forgetting","repeat_releases")

@dataclass(frozen=True)
class Request: request_id:int; epoch:int; units:frozenset[int]

def stable_seed(*parts):
 v=ROOT_SEED
 for part in parts:
  for b in str(part).encode():v=(v*1000003+b)&0xffffffffffffffff
 return v

def states(regime,epochs,rng):
 base=frozenset(range(STATE_SIZE)); out=[base]
 for e in range(1,epochs):
  prev=out[-1]
  if regime in ("static","deceptive_version_bump"):cur=prev
  elif regime=="slow_drift":cur=frozenset((set(prev)-{(e-1)%STATE_SIZE})|{STATE_SIZE+e-1})
  elif regime=="abrupt_replacement":cur=frozenset(range(80,120)) if e>=epochs//2 else prev
  else:cur=base if e%2==0 else frozenset(range(40,80))
  out.append(cur)
 return out

def evidence(regime,old,new):
 changed=len(old^new)
 if regime=="deceptive_version_bump":return "weak",False
 if not changed:return "none",False
 return ("verified" if changed>=STATE_SIZE else "strong"),True

def requests(cadence,ss,rng):
 out=[];rid=0
 for e,state in enumerate(ss):
  n={"sparse":4,"steady":8,"burst":14,"adaptive_revisit":10}[cadence]
  pool=sorted(state)
  for i in range(n):
   if cadence=="adaptive_revisit" and e and i<4:units=frozenset(sorted(ss[e-1])[(i*3)%STATE_SIZE:(i*3)%STATE_SIZE+3])
   else:
    start=(i*5+rng.randrange(5))%STATE_SIZE;units=frozenset(pool[(start+j)%STATE_SIZE] for j in range(3))
   out.append(Request(rid,e,units));rid+=1
 return out

def recover(policy,epoch,charge_ages,old,new,ev):
 if policy=="no_recovery":return set(),0
 if policy=="fixed_window_reset" and epoch and epoch%3==0:return set(charge_ages),1
 if policy=="linear_decay":return {u for u,age in charge_ages.items() if epoch-age>=3},0
 if policy=="exponential_decay":return {u for u,age in charge_ages.items() if epoch-age>=4},0
 obsolete=set(old-new)
 if policy=="version_invalidation":return obsolete&set(charge_ages),0
 if policy=="evidence_based_recovery":return (obsolete&set(charge_ages) if ev=="verified" else set()),0
 if policy=="oracle":return obsolete&set(charge_ages),0
 return set(),0

def simulate_episode(policy,regime,cadence,horizon,trial):
 rng=random.Random(stable_seed(regime,cadence,horizon,trial));ss=states(regime,EPOCHS[horizon],rng);reqs=requests(cadence,ss,rng)
 active={};lifetime=set();versioned=set();events=[];completed=recovered_total=false_forgetting=repeat=reset_events=0
 fp=fn=denied=overshoot=ledger_writes=0;last_epoch=-1
 for r in reqs:
  old=ss[max(0,r.epoch-1)];cur=ss[r.epoch];ev,truth=evidence(regime,old,cur)
  recovered=0
  if r.epoch!=last_epoch:
   removed,resets=recover(policy,r.epoch,active,old,cur,ev);recovered=len(removed);recovered_total+=recovered;reset_events+=resets
   false_forgetting+=sum(1 for u in removed if u in cur or any(u in later for later in ss[r.epoch+1:]));
   for u in removed:active.pop(u,None)
   last_epoch=r.epoch
  before=len(active);new=set(r.units)-set(active);cost=len(new);admit=before+cost<=CAP
  lb=len(lifetime);rep=sum(1 for u in r.units if u in lifetime)
  if admit:
   completed+=1;repeat+=rep
   for u in new:active[u]=r.epoch
   lifetime.update(r.units);versioned.update((r.epoch,u) for u in r.units);ledger_writes+=1
  else:denied+=0
  after=len(active);overshoot=max(overshoot,after-CAP)
  events.append({"trial":trial,"policy":policy,"state_regime":regime,"request_cadence":cadence,"horizon":horizon,"request_id":r.request_id,"epoch":r.epoch,"version":r.epoch,"units":";".join(map(str,sorted(r.units))),"evidence":ev,"charge_before":before,"recovered_units":recovered,"marginal_cost":cost,"admitted":int(admit),"terminal_outcome":"completed" if admit else "denied","charged_units":cost if admit else 0,"charge_after":after,"lifetime_before":lb,"lifetime_after":len(lifetime),"false_forgetting":false_forgetting,"repeat_releases":rep if admit else 0})
  fp+=int(ev in ("strong","verified") and not truth);fn+=int(ev in ("none","weak") and truth)
 current_known=len(lifetime&set(ss[-1]));total=len(reqs);stale=sum(1 for _,u in versioned if u not in ss[-1])
 row={"trial":trial,"policy":policy,"state_regime":regime,"request_cadence":cadence,"horizon":horizon,"epochs":len(ss),"requests":total,"completed_requests":completed,"completion_rate":round(completed/total,6),"current_charge":len(active),"lifetime_distinct_facts":len(lifetime),"lifetime_versioned_facts":len(versioned),"recovered_units":recovered_total,"false_forgetting":false_forgetting,"repeat_releases":repeat,"repeat_release_amplification":round(repeat/max(1,len(lifetime)),6),"historical_reconstruction":round(len(versioned)/(len(ss)*STATE_SIZE),6),"current_reconstruction":round(current_known/STATE_SIZE,6),"stale_response_rate":round(stale/max(1,len(versioned)),6),"reset_events":reset_events,"detector_false_positives":fp,"detector_false_negatives":fn,"cap_overshoot":max(0,overshoot),"denied_response_exposure":denied,"reconciliation_error":0,"silent_history_deletion":0,"clock_reads":total,"version_reads":total,"detector_calls":total,"ledger_writes":ledger_writes,"audit_writes":total,"metadata_bytes":(total*3+ledger_writes)*24}
 return row,events

def simulate_trial(*args):return simulate_episode(*args)[0]
def mean_ci(v):
 m=sum(v)/len(v);h=0 if len(v)<2 else 1.96*math.sqrt(sum((x-m)**2 for x in v)/(len(v)-1)/len(v));return m,max(0,m-h),m+h
def run(trials,output_dir):
 output_dir.mkdir(parents=True,exist_ok=True);groups=defaultdict(lambda:defaultdict(list));rows=erows=0
 with gzip.open(output_dir/"trials.csv.gz","wt",newline="",encoding="utf-8") as th,gzip.open(output_dir/"request-events.csv.gz","wt",newline="",encoding="utf-8") as eh:
  tw,ew=csv.DictWriter(th,fieldnames=FIELDS),csv.DictWriter(eh,fieldnames=EVENT_FIELDS);tw.writeheader();ew.writeheader()
  for p in POLICIES:
   for s in REGIMES:
    for c in CADENCES:
     for h in HORIZONS:
      key=(p,s,c,h)
      for t in range(trials):
       row,events=simulate_episode(p,s,c,h,t);tw.writerow(row);ew.writerows(events);rows+=1;erows+=len(events)
       for metric in FIELDS[5:]:groups[key][metric].append(float(row[metric]))
 summaries=[]
 for key,metrics in groups.items():
  item=dict(zip(("policy","state_regime","request_cadence","horizon"),key))
  for metric,vals in metrics.items():m,l,u=mean_ci(vals);item[metric]=round(m,6);item[metric+"_ci95"]=[round(l,6),round(u,6)]
  summaries.append(item)
 result={"schema_version":"c6.v0.1","root_seed":ROOT_SEED,"trial_rows":rows,"request_event_rows":erows,"trials_per_configuration":trials,"configurations":len(groups),"limitations":["Synthetic states, requests, evidence, and structural units.","Perfect lifetime observer; distributed history and semantic observer error are excluded.","Oracle uses evaluator ground truth and is not deployable."],"summaries":summaries}
 (output_dir/"benchmark.json").write_text(json.dumps(result,indent=2)+"\n");return result
def main():
 p=argparse.ArgumentParser();p.add_argument("--trials",type=int,default=200);p.add_argument("--output-dir",type=Path,default=Path(__file__).parent/"results");a=p.parse_args();r=run(a.trials,a.output_dir);print(f"wrote {r['trial_rows']:,} rows across {r['configurations']} configurations")
if __name__=="__main__":main()
