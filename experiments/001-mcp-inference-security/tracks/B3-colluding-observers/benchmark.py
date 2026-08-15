#!/usr/bin/env python3
"""B3 post-hoc colluding-observer benchmark; stdlib only."""
from __future__ import annotations
import argparse,csv,gzip,json,math,random
from collections import defaultdict
from pathlib import Path

ROOT_SEED=40513
COALITIONS=(1,2,4,8,16,32)
OVERLAPS=("disjoint","low","medium","high")
BEHAVIORS=("independent","overlapping","partitioned")
POLICIES=("per_client","organization","behavioral_cohort","diversity_aware","global","oracle")
BUDGETS=(.25,.50,.75)
REQUESTS=96; HIDDEN_UNITS=100
OVERLAP_SHIFT={"disjoint":-.20,"low":0.0,"medium":.20,"high":.40}
BEHAVIOR_COMMON={"partitioned":0.0,"independent":.30,"overlapping":.65}
FIELDS=["trial","coalition_size","overlap","query_behavior","policy","budget","requests",
        "coalition_reconstruction","max_individual_reconstruction","coalition_gain","coalition_amplification",
        "complementarity_efficiency","unique_union_units","sum_individual_units","false_suspicion",
        "legitimate_group_utility","attribution_keys","denied_requests"]

def stable_seed(*parts):
 v=ROOT_SEED
 for p in parts:
  for b in str(p).encode(): v=(v*1_000_003+b)&0xffffffffffffffff
 return v

def common_probability(overlap,behavior):
 return min(.95,max(0.0,BEHAVIOR_COMMON[behavior]+OVERLAP_SHIFT[overlap]))

def query_plan(size,overlap,behavior,rng):
 local=[0]*size; plan=[]; p=common_probability(overlap,behavior)
 for request in range(REQUESTS):
  observer=request%size
  if rng.random()<p: query=local[observer]%HIDDEN_UNITS
  elif behavior=="independent": query=rng.randrange(HIDDEN_UNITS)
  else: query=request%HIDDEN_UNITS
  local[observer]+=1; plan.append((observer,query))
 return plan

def policy_keys(size,policy,overlap,behavior,rng):
 if policy in ("global","oracle"): return [0]*size
 if policy=="diversity_aware": return list(range(size))
 if policy=="per_client": return list(range(size))
 if policy=="organization": return [i//4 for i in range(size)]
 # Similar traffic is server-visible but only probabilistic evidence.
 detect_p=min(.90,.15+.75*common_probability(overlap,behavior))
 keys=[0]
 for i in range(1,size): keys.append(0 if rng.random()<detect_p else i)
 return keys

def simulate_trial(size,overlap,behavior,policy,budget,trial):
 rng=random.Random(stable_seed(size,overlap,behavior,policy,budget,trial))
 plan=query_plan(size,overlap,behavior,rng); keys=policy_keys(size,policy,overlap,behavior,rng)
 cap=round(budget*HIDDEN_UNITS); loads=defaultdict(int); individual=[set() for _ in range(size)]
 denied=0; global_unique=set(); diversity_cap=round(min(1.0,budget*1.5)*HIDDEN_UNITS)
 for observer,query in plan:
  key=keys[observer]
  if loads[key]>=cap or (policy=="diversity_aware" and query not in global_unique and len(global_unique)>=diversity_cap):
   denied+=1; continue
  loads[key]+=1; individual[observer].add(query); global_unique.add(query)
 union=set().union(*individual); union_n=len(union); individual_counts=[len(x) for x in individual]
 max_ind=max(individual_counts)/HIDDEN_UNITS; coalition=union_n/HIDDEN_UNITS
 total_units=sum(individual_counts); efficiency=union_n/total_units if total_units else 0.0
 if policy=="global": false_suspicion=1
 elif policy=="organization": false_suspicion=int(size>1 and rng.random()<.06)
 elif policy=="behavioral_cohort": false_suspicion=int(rng.random()<(.05+.15*common_probability(overlap,behavior)))
 elif policy=="diversity_aware": false_suspicion=int(rng.random()<.18)
 else: false_suspicion=0
 utility=0.0 if policy=="global" else 1.0-false_suspicion
 if policy=="organization": utility*=.95
 if policy=="diversity_aware": utility*=.90
 return {"trial":trial,"coalition_size":size,"overlap":overlap,"query_behavior":behavior,"policy":policy,"budget":budget,"requests":REQUESTS,
  "coalition_reconstruction":round(coalition,6),"max_individual_reconstruction":round(max_ind,6),
  "coalition_gain":round(coalition-max_ind,6),"coalition_amplification":round(coalition/max(max_ind,1e-9),6),
  "complementarity_efficiency":round(efficiency,6),"unique_union_units":union_n,"sum_individual_units":total_units,
  "false_suspicion":false_suspicion,"legitimate_group_utility":round(utility,6),"attribution_keys":len(set(keys)),"denied_requests":denied}

def mean_ci(values):
 mean=sum(values)/len(values)
 if len(values)<2:return mean,mean,mean
 var=sum((v-mean)**2 for v in values)/(len(values)-1); half=1.96*math.sqrt(var/len(values))
 return mean,max(0.0,mean-half),min(max(values),mean+half)

def run(trials,output_dir):
 output_dir.mkdir(parents=True,exist_ok=True); grouped=defaultdict(lambda:defaultdict(list)); rows=0
 with gzip.open(output_dir/'trials.csv.gz','wt',newline='',encoding='utf-8') as h:
  writer=csv.DictWriter(h,fieldnames=FIELDS);writer.writeheader()
  for size in COALITIONS:
   for overlap in OVERLAPS:
    for behavior in BEHAVIORS:
     for policy in POLICIES:
      for budget in BUDGETS:
       key=(size,overlap,behavior,policy,budget)
       for trial in range(trials):
        row=simulate_trial(size,overlap,behavior,policy,budget,trial);writer.writerow(row);rows+=1
        for metric in ("coalition_reconstruction","max_individual_reconstruction","coalition_gain","coalition_amplification","complementarity_efficiency","unique_union_units","sum_individual_units","false_suspicion","legitimate_group_utility","attribution_keys","denied_requests"):
         grouped[key][metric].append(float(row[metric]))
 summaries=[]
 for key,metrics in grouped.items():
  item=dict(zip(("coalition_size","overlap","query_behavior","policy","budget"),key))
  for metric,values in metrics.items():
   mean,low,high=mean_ci(values);item[metric]=round(mean,6);item[metric+'_ci95']=[round(low,6),round(high,6)]
  summaries.append(item)
 result={"schema_version":"b3.v0.1","root_seed":ROOT_SEED,"trial_rows":rows,"trials_per_configuration":trials,
  "configurations":len(grouped),"fixed_total_requests":REQUESTS,"exchange_fraction":1.0,"exchange_timing":"post_hoc",
  "limitations":["Full post-hoc exchange only; partial and online exchange are deferred.","Detector and false-suspicion rates are synthetic assumptions.","Structural union is not semantic reconstruction."],
  "summaries":sorted(summaries,key=lambda x:(x['coalition_size'],x['overlap'],x['query_behavior'],x['policy'],x['budget']))}
 (output_dir/'benchmark.json').write_text(json.dumps(result,indent=2)+'\n');return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=500);p.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'results');a=p.parse_args()
 r=run(a.trials,a.output_dir);print(f"wrote {r['trial_rows']:,} rows across {r['configurations']} configurations")
if __name__=='__main__':main()
