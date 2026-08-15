#!/usr/bin/env python3
"""B4 cross-session accumulation benchmark; stdlib only."""
from __future__ import annotations
import argparse,csv,gzip,json,math,random
from collections import defaultdict
from pathlib import Path

ROOT_SEED=40514
SESSIONS=(1,2,4,8,16,32)
POLICIES=("session_reset","persistent","fixed_ttl","rolling_window","exponential_decay")
GAPS=("immediate","short","medium","long")
GAP_VALUE={"immediate":0,"short":1,"medium":4,"long":16}
BUDGETS=(.25,.50,.75)
WORKLOADS=("duplicate_heavy","random","partitioned")
REQUESTS=96; HIDDEN_UNITS=100; TTL=4; WINDOW=8; HALF_LIFE=4.0
FIELDS=["trial","session_count","memory_policy","session_gap","budget","workload","requests",
 "observer_known_exposure","policy_accounted_exposure","exposure_gap","excess_historical_exposure",
 "cross_session_amplification","expired_but_known_exposure","legitimate_continuity_utility",
 "denied_requests","retained_entries","final_logical_time"]

def stable_seed(*parts):
 v=ROOT_SEED
 for p in parts:
  for b in str(p).encode():v=(v*1_000_003+b)&0xffffffffffffffff
 return v

def partition_requests(sessions):
 q,r=divmod(REQUESTS,sessions);return [q+(i<r) for i in range(sessions)]

def query_plan(sessions,workload,rng):
 plan=[];global_index=0
 for session,count in enumerate(partition_requests(sessions)):
  for local in range(count):
   if workload=="partitioned":query=global_index%HIDDEN_UNITS
   elif workload=="random":query=rng.randrange(HIDDEN_UNITS)
   else:query=local%12
   plan.append((session,query));global_index+=1
 return plan

def accounted(entries,policy,now,current_session,last_session_time):
 if policy=="session_reset":return float(sum(1 for _,s in entries.values() if s==current_session))
 if policy=="persistent":return float(len(entries))
 if policy=="fixed_ttl":return float(len(entries))
 if policy=="rolling_window":return sum(1.0 for t,_ in entries.values() if now-t<=WINDOW)
 return sum(2**(-(now-t)/HALF_LIFE) for t,_ in entries.values())

def simulate_trial(sessions,policy,gap,budget,workload,trial):
 rng=random.Random(stable_seed(sessions,policy,gap,budget,workload,trial));plan=query_plan(sessions,workload,rng)
 cap=round(budget*HIDDEN_UNITS);entries={};observer=set();denied=0;now=0;current=-1;last_session_time=None
 final_accounted=0.0
 for session,query in plan:
  if session!=current:
   if current>=0:last_session_time=now
   now+=GAP_VALUE[gap]+1;current=session
   if policy=="fixed_ttl" and last_session_time is not None and now-last_session_time>TTL:entries={}
  if query in observer:continue
  current_accounted=accounted(entries,policy,now,current,last_session_time)
  if current_accounted+1>cap:denied+=1;continue
  observer.add(query);entries[query]=(now,current)
 final_accounted=accounted(entries,policy,now,current,last_session_time)
 known=len(observer)/HIDDEN_UNITS;acc=final_accounted/HIDDEN_UNITS;gap_value=max(0.0,known-acc)
 expired_known=sum(1 for q in observer if q not in entries or (policy=="rolling_window" and now-entries[q][0]>WINDOW))/HIDDEN_UNITS
 utility=(REQUESTS-denied)/REQUESTS
 return {"trial":trial,"session_count":sessions,"memory_policy":policy,"session_gap":gap,"budget":budget,"workload":workload,"requests":REQUESTS,
  "observer_known_exposure":round(known,6),"policy_accounted_exposure":round(acc,6),"exposure_gap":round(gap_value,6),
  "excess_historical_exposure":round(max(0.0,known-budget),6),"cross_session_amplification":round(known/budget,6),
  "expired_but_known_exposure":round(expired_known,6),"legitimate_continuity_utility":round(utility,6),
  "denied_requests":denied,"retained_entries":len(entries),"final_logical_time":now}

def mean_ci(values):
 mean=sum(values)/len(values)
 if len(values)<2:return mean,mean,mean
 var=sum((x-mean)**2 for x in values)/(len(values)-1);half=1.96*math.sqrt(var/len(values));return mean,max(0,mean-half),min(max(values),mean+half)

def run(trials,output_dir):
 output_dir.mkdir(parents=True,exist_ok=True);groups=defaultdict(lambda:defaultdict(list));rows=0
 with gzip.open(output_dir/'trials.csv.gz','wt',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=FIELDS);w.writeheader()
  for sessions in SESSIONS:
   for policy in POLICIES:
    for gap in GAPS:
     for budget in BUDGETS:
      for workload in WORKLOADS:
       key=(sessions,policy,gap,budget,workload)
       for trial in range(trials):
        row=simulate_trial(sessions,policy,gap,budget,workload,trial);w.writerow(row);rows+=1
        for metric in ("observer_known_exposure","policy_accounted_exposure","exposure_gap","excess_historical_exposure","cross_session_amplification","expired_but_known_exposure","legitimate_continuity_utility","denied_requests","retained_entries","final_logical_time"):
         groups[key][metric].append(float(row[metric]))
 summaries=[]
 for key,metrics in groups.items():
  item=dict(zip(("session_count","memory_policy","session_gap","budget","workload"),key))
  for metric,values in metrics.items():
   mean,low,high=mean_ci(values);item[metric]=round(mean,6);item[metric+'_ci95']=[round(low,6),round(high,6)]
  summaries.append(item)
 result={"schema_version":"b4.v0.1","root_seed":ROOT_SEED,"trial_rows":rows,"trials_per_configuration":trials,"configurations":len(groups),"fixed_total_requests":REQUESTS,
  "parameters":{"ttl":TTL,"rolling_window":WINDOW,"decay_half_life":HALF_LIFE,"gap_values":GAP_VALUE},
  "limitations":["Static hidden state only.","Fixed total requests; per-session traffic scaling is deferred.","Logical time and retention parameters are synthetic."],
  "summaries":sorted(summaries,key=lambda x:(x['session_count'],x['memory_policy'],x['session_gap'],x['budget'],x['workload']))}
 (output_dir/'benchmark.json').write_text(json.dumps(result,indent=2)+'\n');return result
def main():
 p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=500);p.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'results');a=p.parse_args();r=run(a.trials,a.output_dir);print(f"wrote {r['trial_rows']:,} rows across {r['configurations']} configurations")
if __name__=='__main__':main()
