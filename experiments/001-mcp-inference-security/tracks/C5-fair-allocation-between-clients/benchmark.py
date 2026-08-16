#!/usr/bin/env python3
"""C5 fair-allocation benchmark; standard library only."""

from __future__ import annotations

import argparse, csv, gzip, json, math, random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT_SEED = 40525
POLICIES = ("global_fifo", "equal_reservation", "weighted_reservation", "progressive_max_min", "proportional_share", "bounded_borrowing", "oracle")
DEMANDS = ("balanced_steady", "balanced_burst", "asymmetric_heavy", "sparse_clients", "late_high_value")
WEIGHTS = ("equal", "demand_proportional", "value_proportional", "misspecified")
SCARCITY = ("mild", "moderate", "severe")
TICKS, UNIVERSE, PRINCIPALS = 120, 180, tuple(range(5))
INITIAL = frozenset(range(40))
CAPS = {"mild": 70, "moderate": 50, "severe": 34}
FIELDS = ("trial","policy","demand","weight_profile","scarcity","episode_ticks","requests","active_principals","completed_requests","total_utility","requested_utility","utility_completion_ratio","starved_principals","starvation_rate","minimum_principal_utility","jain_utility","charged_units","remaining_cap","utilization","unused_reserved_units","borrowed_units","share_error","oracle_regret","cap_overshoot","duplicate_charge_count","denied_response_exposure","reconciliation_error","silent_budget_reset","policy_reads","ledger_operations","audit_writes","metadata_bytes")
EVENT_FIELDS = ("trial","policy","demand","weight_profile","scarcity","request_id","tick","principal_id","task_value","requested_units","marginal_cost","target_share","admitted","replayed","terminal_outcome","charged_units","ledger_before","ledger_after","remaining_cap","borrowed_units")

@dataclass(frozen=True)
class Request:
    request_id: int
    tick: int
    principal: int
    units: frozenset[int]
    value: int

def stable_seed(*parts: object) -> int:
    value = ROOT_SEED
    for part in parts:
        for byte in str(part).encode():
            value = (value * 1_000_003 + byte) & 0xFFFFFFFFFFFFFFFF
    return value

def generate_requests(demand: str, rng: random.Random) -> list[Request]:
    counts = [12] * 5
    if demand == "asymmetric_heavy": counts = [32, 8, 8, 8, 8]
    if demand == "sparse_clients": counts = [20, 18, 12, 0, 0]
    requests, rid = [], 0
    for principal, count in enumerate(counts):
        for index in range(count):
            if demand == "balanced_burst": tick = 30 + index // 2
            elif demand == "late_high_value": tick = 70 + index
            else: tick = 5 + (index * 105) // max(1, count)
            value = 5 if demand == "late_high_value" and principal >= 3 else 1 + ((principal + index) % 3)
            anchor = 40 + ((principal * 29 + index * 11 + rng.randrange(7)) % 130)
            width = 1 + ((principal + index) % 3)
            units = frozenset((anchor + offset) % UNIVERSE for offset in range(width))
            requests.append(Request(rid, tick, principal, units, value)); rid += 1
    return sorted(requests, key=lambda item: (item.tick, item.request_id))

def weights_for(profile: str, requests: list[Request]) -> dict[int, float]:
    demand = {p: sum(1 for r in requests if r.principal == p) for p in PRINCIPALS}
    value = {p: sum(r.value for r in requests if r.principal == p) for p in PRINCIPALS}
    if profile == "equal": raw = {p: 1.0 for p in PRINCIPALS}
    elif profile == "demand_proportional": raw = {p: float(demand[p]) for p in PRINCIPALS}
    elif profile == "value_proportional": raw = {p: float(value[p]) for p in PRINCIPALS}
    else: raw = {p: float(max(value.values()) + 1 - value[p]) for p in PRINCIPALS}
    total = sum(raw.values())
    return {p: raw[p] / total for p in PRINCIPALS}

def jain(values: list[float]) -> float:
    total, denominator = sum(values), len(values) * sum(v * v for v in values)
    return total * total / denominator if denominator else 0.0

def decide(policy: str, request: Request, cost: int, cap: int, weights: dict[int,float], charges: dict[int,int], counts: dict[int,int]) -> tuple[bool,int]:
    used, remaining = sum(charges.values()), cap - sum(charges.values())
    if cost > remaining: return False, 0
    if cost == 0: return True, 0
    p = request.principal
    if policy == "global_fifo": return True, 0
    if policy == "equal_reservation": return charges[p] + cost <= cap // 5, 0
    if policy == "weighted_reservation": return charges[p] + cost <= math.floor(cap * weights[p]), 0
    if policy == "progressive_max_min":
        active = [p for p in PRINCIPALS if counts[p] > 0]
        active_min = min(charges[p] for p in active)
        return charges[p] <= active_min + 2, 0
    if policy == "proportional_share":
        allowance = math.ceil(cap * weights[p]) + 2
        return charges[p] + cost <= allowance, 0
    if policy == "bounded_borrowing":
        guarantee = cap // 5
        before_borrow = max(0, charges[p] - guarantee)
        after_borrow = max(0, charges[p] + cost - guarantee)
        return after_borrow <= 4, after_borrow - before_borrow
    raise AssertionError("oracle handled separately")

def simulate_episode(policy: str, demand: str, weight_profile: str, scarcity: str, trial: int):
    rng = random.Random(stable_seed(demand, weight_profile, scarcity, trial))
    requests, cap = generate_requests(demand, rng), CAPS[scarcity]
    weights = weights_for(weight_profile, requests)
    ordered = requests if policy != "oracle" else sorted(requests, key=lambda r: (-r.value / len(r.units), r.tick, r.request_id))
    released, charges, counts, utility = set(INITIAL), defaultdict(int), defaultdict(int), defaultdict(int)
    events, completed, borrowed_total = [], 0, 0
    duplicate_charge = denied_exposure = policy_reads = ledger_ops = audit_writes = 0
    for request in ordered:
        before = len(released - INITIAL); new = set(request.units) - released; cost = len(new)
        counts[request.principal] += 1; policy_reads += 1
        if policy == "oracle": admitted, borrowed = cost <= cap - before, 0
        else: admitted, borrowed = decide(policy, request, cost, cap, weights, charges, counts)
        charged = 0
        if admitted:
            charged = cost; released.update(new); charges[request.principal] += charged
            utility[request.principal] += request.value; completed += 1; borrowed_total += borrowed; ledger_ops += 1
            outcome = "completed"
        else: outcome = "denied"
        after = len(released - INITIAL)
        if after > cap: raise AssertionError("cap exceeded")
        audit_writes += 1
        events.append({"trial":trial,"policy":policy,"demand":demand,"weight_profile":weight_profile,"scarcity":scarcity,"request_id":request.request_id,"tick":request.tick,"principal_id":request.principal,"task_value":request.value,"requested_units":";".join(map(str,sorted(request.units))),"marginal_cost":cost,"target_share":round(weights[request.principal],6),"admitted":int(admitted),"replayed":int(admitted and cost==0),"terminal_outcome":outcome,"charged_units":charged,"ledger_before":before,"ledger_after":after,"remaining_cap":cap-after,"borrowed_units":borrowed})
    active = [p for p in PRINCIPALS if any(r.principal == p for r in requests)]
    utilities = [utility[p] for p in active]; requested = sum(r.value for r in requests)
    starved = sum(1 for p in active if utility[p] == 0 and charges[p] == 0)
    charged = len(released - INITIAL)
    unused_reserved = sum(max(0, math.floor(cap * weights[p]) - charges[p]) for p in active) if "reservation" in policy else 0
    actual_shares = {p: charges[p] / charged if charged else 0 for p in active}
    share_error = sum(abs(actual_shares[p] - weights[p]) for p in active)
    total_utility = sum(utilities)
    row={"trial":trial,"policy":policy,"demand":demand,"weight_profile":weight_profile,"scarcity":scarcity,"episode_ticks":TICKS,"requests":len(requests),"active_principals":len(active),"completed_requests":completed,"total_utility":total_utility,"requested_utility":requested,"utility_completion_ratio":round(total_utility/requested,6),"starved_principals":starved,"starvation_rate":round(starved/len(active),6),"minimum_principal_utility":min(utilities),"jain_utility":round(jain(utilities),6),"charged_units":charged,"remaining_cap":cap-charged,"utilization":round(charged/cap,6),"unused_reserved_units":unused_reserved,"borrowed_units":borrowed_total,"share_error":round(share_error,6),"oracle_regret":requested-total_utility,"cap_overshoot":max(0,charged-cap),"duplicate_charge_count":duplicate_charge,"denied_response_exposure":denied_exposure,"reconciliation_error":abs(sum(charges.values())-charged),"silent_budget_reset":0,"policy_reads":policy_reads,"ledger_operations":ledger_ops,"audit_writes":audit_writes,"metadata_bytes":(policy_reads+ledger_ops+audit_writes)*24}
    return row, events

def simulate_trial(policy, demand, weight_profile, scarcity, trial):
    return simulate_episode(policy,demand,weight_profile,scarcity,trial)[0]

def mean_ci(values):
    mean=sum(values)/len(values)
    if len(values)<2:return mean,mean,mean
    variance=sum((v-mean)**2 for v in values)/(len(values)-1); half=1.96*math.sqrt(variance/len(values))
    return mean,max(0,mean-half),mean+half

def run(trials:int, output_dir:Path):
    output_dir.mkdir(parents=True,exist_ok=True); groups=defaultdict(lambda:defaultdict(list)); rows=event_rows=0
    with gzip.open(output_dir/"trials.csv.gz","wt",newline="",encoding="utf-8") as th, gzip.open(output_dir/"request-events.csv.gz","wt",newline="",encoding="utf-8") as eh:
        tw,ew=csv.DictWriter(th,fieldnames=FIELDS),csv.DictWriter(eh,fieldnames=EVENT_FIELDS);tw.writeheader();ew.writeheader()
        for policy in POLICIES:
            for demand in DEMANDS:
                for weight in WEIGHTS:
                    for scarcity in SCARCITY:
                        key=(policy,demand,weight,scarcity)
                        for trial in range(trials):
                            row,events=simulate_episode(policy,demand,weight,scarcity,trial);tw.writerow(row);ew.writerows(events);rows+=1;event_rows+=len(events)
                            for metric in FIELDS[5:]:groups[key][metric].append(float(row[metric]))
    summaries=[]
    for key,metrics in groups.items():
        item=dict(zip(("policy","demand","weight_profile","scarcity"),key))
        for metric,values in metrics.items():
            mean,low,high=mean_ci(values);item[metric]=round(mean,6);item[f"{metric}_ci95"]=[round(low,6),round(high,6)]
        summaries.append(item)
    result={"schema_version":"c5.v0.1","root_seed":ROOT_SEED,"trial_rows":rows,"request_event_rows":event_rows,"trials_per_configuration":trials,"configurations":len(groups),"episode_ticks":TICKS,"principals":5,"limitations":["Synthetic requests, values, weights, and structural units.","Exact durable identities and marginal exposure accounting are assumed.","One atomic ledger; malicious behavior, Sybils, decay, and semantic observer error are excluded.","Oracle sees evaluator task value and is not deployable."],"summaries":sorted(summaries,key=lambda x:tuple(x[k] for k in ("policy","demand","weight_profile","scarcity")))}
    (output_dir/"benchmark.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8");return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--trials",type=int,default=200);parser.add_argument("--output-dir",type=Path,default=Path(__file__).parent/"results")
    args=parser.parse_args();result=run(args.trials,args.output_dir);print(f"wrote {result['trial_rows']:,} rows across {result['configurations']} configurations")
if __name__=="__main__":main()
