#!/usr/bin/env python3
"""B5 cross-server accumulation benchmark; stdlib only."""
from __future__ import annotations
import argparse,csv,gzip,json,math,random
from collections import defaultdict
from pathlib import Path

ROOT_SEED=40515
SERVERS=(1,2,4,8,16,32)
MODELS=("local","central","eventual","signed_token","sketch","oracle")
OVERLAPS=("disjoint","low","medium","high")
SYNC=("healthy","delayed","partitioned")
BUDGETS=(.25,.50,.75)
REQUESTS=96;HIDDEN_UNITS=100
COMMON_P={"disjoint":0.0,"low":.2,"medium":.5,"high":.8}
BYTES_PER_UPDATE={"local":0,"central":64,"eventual":32,"signed_token":16,"sketch":8,"oracle":0}
FIELDS=["trial","server_count","accounting_model","output_overlap","sync_condition","budget","requests",
 "aggregate_exposure","excess_federated_exposure","cross_server_amplification","unique_union_units",
 "denied_requests","legitimate_utility","federated_view_divergence","metadata_bytes","linked_operators",
 "accounting_groups","fail_closed"]

def stable_seed(*parts):
 v=ROOT_SEED
 for p in parts:
  for b in str(p).encode():v=(v*1_000_003+b)&0xffffffffffffffff
 return v

def request_plan(servers,overlap,rng):
 local=[0]*servers;plan=[];p=COMMON_P[overlap]
 for i in range(REQUESTS):
  server=i%servers
  query=local[server] if rng.random()<p else i%HIDDEN_UNITS
  local[server]+=1;plan.append((server,query))
 return plan

def group_keys(servers,model,sync):
 if model=="local":return list(range(servers))
 if model in ("central","oracle"):return [0]*servers
 if sync=="healthy":return [0]*servers
 if sync=="partitioned":return list(range(servers))
 if model=="eventual":return [i//4 for i in range(servers)]
 if model=="signed_token":return [i%2 for i in range(servers)]
 return [i//2 for i in range(servers)]

def simulate_trial(servers,model,overlap,sync,budget,trial):
 rng=random.Random(stable_seed(servers,model,overlap,sync,budget,trial));plan=request_plan(servers,overlap,rng)
 keys=group_keys(servers,model,sync);cap=round(budget*HIDDEN_UNITS);caps=defaultdict(lambda:cap)
 if model=="sketch" and sync!="partitioned":
  # Approximation error can deny early or overshoot slightly.
  caps[0]=max(1,cap+rng.choice((-3,-2,-1,0,0,1,2,3)))
 group_units=defaultdict(set);union=set();denied=0;fail_closed=0
 central_outage=(model=="central" and sync=="partitioned")
 for server,query in plan:
  if central_outage:
   denied+=1;fail_closed=1;continue
  key=keys[server];limit=caps[key]
  if query not in group_units[key] and len(group_units[key])>=limit:
   denied+=1;continue
  group_units[key].add(query);union.add(query)
 exposure=len(union)/HIDDEN_UNITS
 values=[len(v) for v in group_units.values()];divergence=(max(values)-min(values))/HIDDEN_UNITS if values else 0.0
 updates=0 if model=="local" else (REQUESTS if sync=="healthy" else math.ceil(REQUESTS/8) if sync=="delayed" else 0)
 metadata=updates*BYTES_PER_UPDATE[model]
 utility=(REQUESTS-denied)/REQUESTS
 linked=0 if model in ("local","oracle") else servers
 return {"trial":trial,"server_count":servers,"accounting_model":model,"output_overlap":overlap,"sync_condition":sync,"budget":budget,"requests":REQUESTS,
  "aggregate_exposure":round(exposure,6),"excess_federated_exposure":round(max(0.0,exposure-budget),6),
  "cross_server_amplification":round(exposure/budget,6),"unique_union_units":len(union),"denied_requests":denied,
  "legitimate_utility":round(utility,6),"federated_view_divergence":round(divergence,6),"metadata_bytes":metadata,
  "linked_operators":linked,"accounting_groups":len(set(keys)),"fail_closed":fail_closed}

def mean_ci(values):
 mean=sum(values)/len(values)
 if len(values)<2:return mean,mean,mean
 var=sum((x-mean)**2 for x in values)/(len(values)-1);half=1.96*math.sqrt(var/len(values));return mean,max(0,mean-half),min(max(values),mean+half)

def run(trials,output_dir):
 output_dir.mkdir(parents=True,exist_ok=True);groups=defaultdict(lambda:defaultdict(list));rows=0
 with gzip.open(output_dir/'trials.csv.gz','wt',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=FIELDS);w.writeheader()
  for servers in SERVERS:
   for model in MODELS:
    for overlap in OVERLAPS:
     for sync in SYNC:
      for budget in BUDGETS:
       key=(servers,model,overlap,sync,budget)
       for trial in range(trials):
        row=simulate_trial(servers,model,overlap,sync,budget,trial);w.writerow(row);rows+=1
        for metric in ("aggregate_exposure","excess_federated_exposure","cross_server_amplification","unique_union_units","denied_requests","legitimate_utility","federated_view_divergence","metadata_bytes","linked_operators","accounting_groups","fail_closed"):
         groups[key][metric].append(float(row[metric]))
 summaries=[]
 for key,metrics in groups.items():
  item=dict(zip(("server_count","accounting_model","output_overlap","sync_condition","budget"),key))
  for metric,values in metrics.items():
   mean,low,high=mean_ci(values);item[metric]=round(mean,6);item[metric+'_ci95']=[round(low,6),round(high,6)]
  summaries.append(item)
 result={"schema_version":"b5.v0.1","root_seed":ROOT_SEED,"trial_rows":rows,"trials_per_configuration":trials,"configurations":len(groups),"fixed_total_requests":REQUESTS,
  "limitations":["Complementary round-robin routing only.","Synchronization groups and sketch error are synthetic abstractions.","Central partition uses fail-closed behavior.","Structural union is not semantic reconstruction."],
  "summaries":sorted(summaries,key=lambda x:(x['server_count'],x['accounting_model'],x['output_overlap'],x['sync_condition'],x['budget']))}
 (output_dir/'benchmark.json').write_text(json.dumps(result,indent=2)+'\n');return result
def main():
 p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=450);p.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'results');a=p.parse_args();r=run(a.trials,a.output_dir);print(f"wrote {r['trial_rows']:,} rows across {r['configurations']} configurations")
if __name__=='__main__':main()
