#!/usr/bin/env python3
"""B2 coordinated-Sybil benchmark; Python standard library only."""

from __future__ import annotations

import argparse, csv, gzip, json, math, random
from collections import defaultdict
from pathlib import Path

ROOT_SEED = 40512
POOL_SIZES = (1, 2, 4, 8, 16, 32, 64)
SCOPES = ("per_identity", "per_session", "attributed_cluster", "global", "proof_cost", "oracle")
COORDINATION = ("duplicate", "random", "partition", "adaptive")
BUDGETS = (0.25, 0.50, 0.75)
QUALITIES = ("clean", "noisy", "missing")
REQUESTS = HIDDEN_UNITS = 100
LINK_P = {"clean": .98, "noisy": .80, "missing": .50}
FALSE_MERGE_P = {"clean": .02, "noisy": .06, "missing": .10}

FIELDS = ["trial","pool_size","ledger_scope","coordination","budget","signal_quality",
          "requests","admitted_requests","unique_queries","exposure","excess_exposure",
          "sybil_amplification","false_split_rate","false_merge","legitimate_utility",
          "attribution_keys","denied_requests"]


def stable_seed(*parts):
    value = ROOT_SEED
    for part in parts:
        for byte in str(part).encode(): value = (value * 1_000_003 + byte) & 0xffffffffffffffff
    return value


def identity_keys(pool, scope, quality, rng):
    if scope in ("global", "oracle"): return [0] * pool, 0.0
    if scope in ("per_identity", "per_session", "proof_cost"): return list(range(pool)), 1.0 if pool > 1 else 0.0
    keys, splits = [0], 0
    for identity in range(1, pool):
        if rng.random() < LINK_P[quality]: keys.append(0)
        else:
            keys.append(identity)
            splits += 1
    return keys, splits / (pool - 1) if pool > 1 else 0.0


def query_plan(pool, mode, rng):
    local = [0] * pool
    plan = []
    for request in range(REQUESTS):
        identity = request % pool
        if mode == "duplicate": query = local[identity]
        elif mode == "random": query = rng.randrange(HIDDEN_UNITS)
        else: query = request % HIDDEN_UNITS
        local[identity] += 1
        plan.append((identity, query))
    return plan


def simulate_trial(pool, scope, mode, budget, quality, trial):
    rng = random.Random(stable_seed(pool, scope, mode, budget, quality, trial))
    keys, split_rate = identity_keys(pool, scope, quality, rng)
    cap = round(budget * HIDDEN_UNITS)
    loads = defaultdict(int)
    disclosed = set()
    denied = admitted = 0
    proof_limit = max(1, math.ceil(math.sqrt(pool))) if scope == "proof_cost" else pool
    plan = query_plan(pool, mode, rng)
    if mode == "adaptive":
        # Same unique query universe, but identities with remaining independent budget act first.
        plan.sort(key=lambda pair: (keys[pair[0]], pair[1]))
    for identity, query in plan:
        if identity >= proof_limit:
            denied += 1
            continue
        admitted += 1
        key = keys[identity]
        if loads[key] >= cap:
            denied += 1
            continue
        loads[key] += 1
        disclosed.add(query)
    exposure = len(disclosed) / HIDDEN_UNITS
    excess = max(0.0, exposure - budget)
    false_merge = int(scope in ("attributed_cluster", "global") and rng.random() < FALSE_MERGE_P[quality])
    if scope == "global": false_merge = 1
    utility = 0.0 if false_merge and loads.get(0, 0) >= cap else 1.0
    if scope == "proof_cost": utility *= proof_limit / pool
    return {
        "trial":trial,"pool_size":pool,"ledger_scope":scope,"coordination":mode,
        "budget":budget,"signal_quality":quality,"requests":REQUESTS,
        "admitted_requests":admitted,"unique_queries":len(disclosed),
        "exposure":round(exposure,6),"excess_exposure":round(excess,6),
        "sybil_amplification":round(exposure / budget,6),"false_split_rate":round(split_rate,6),
        "false_merge":false_merge,"legitimate_utility":round(utility,6),
        "attribution_keys":len(set(keys[:proof_limit])),"denied_requests":denied,
    }


def mean_ci(values):
    mean = sum(values)/len(values)
    if len(values)<2: return mean,mean,mean
    var=sum((v-mean)**2 for v in values)/(len(values)-1)
    half=1.96*math.sqrt(var/len(values))
    return mean,max(0.0,mean-half),min(max(values),mean+half)


def run(trials, output_dir):
    output_dir.mkdir(parents=True,exist_ok=True)
    grouped=defaultdict(lambda:defaultdict(list)); rows=0
    with gzip.open(output_dir/"trials.csv.gz","wt",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=FIELDS); writer.writeheader()
        for pool in POOL_SIZES:
          for scope in SCOPES:
           for mode in COORDINATION:
            for budget in BUDGETS:
             for quality in QUALITIES:
              key=(pool,scope,mode,budget,quality)
              for trial in range(trials):
               row=simulate_trial(pool,scope,mode,budget,quality,trial); writer.writerow(row); rows+=1
               for metric in ("admitted_requests","unique_queries","exposure","excess_exposure","sybil_amplification","false_split_rate","false_merge","legitimate_utility","attribution_keys","denied_requests"):
                grouped[key][metric].append(float(row[metric]))
    summaries=[]
    for key,metrics in grouped.items():
        item=dict(zip(("pool_size","ledger_scope","coordination","budget","signal_quality"),key))
        for metric,values in metrics.items():
            mean,low,high=mean_ci(values); item[metric]=round(mean,6); item[metric+"_ci95"]=[round(low,6),round(high,6)]
        summaries.append(item)
    result={"schema_version":"b2.v0.1","root_seed":ROOT_SEED,"trial_rows":rows,
            "trials_per_configuration":trials,"configurations":len(grouped),
            "fixed_requests":REQUESTS,
            "limitations":["Fixed-request experiment only; the separate deadline experiment is deferred.",
             "Attribution and false-merge probabilities are synthetic declared assumptions.",
             "Proof cost is modeled as an admission cap, not a real identity technology."],
            "summaries":sorted(summaries,key=lambda x:(x["pool_size"],x["ledger_scope"],x["coordination"],x["budget"],x["signal_quality"]))}
    (output_dir/"benchmark.json").write_text(json.dumps(result,indent=2)+"\n")
    return result


def main():
    p=argparse.ArgumentParser(); p.add_argument("--trials",type=int,default=500); p.add_argument("--output-dir",type=Path,default=Path(__file__).parent/"results")
    a=p.parse_args(); result=run(a.trials,a.output_dir)
    print(f"wrote {result['trial_rows']:,} rows across {result['configurations']} configurations")


if __name__=="__main__": main()
