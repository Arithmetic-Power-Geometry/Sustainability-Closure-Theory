from pathlib import Path
import json
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "external" / "peese_equal_size_witness.csv"
OUT = ROOT / "results"

def load_witness():
    return pd.read_csv(DATA)

def baseline_pairs(df):
    pairs=[]
    for i,j in itertools.combinations(range(len(df)),2):
        dp=float(df.iloc[i]["pue"]-df.iloc[j]["pue"])
        dw=float(df.iloc[i]["wue"]-df.iloc[j]["wue"])
        if dp != 0 and dw != 0 and np.sign(dp) != np.sign(dw):
            pairs.append((i,j))
    return pairs

def pareto_mask(p,w):
    n=len(p)
    keep=np.ones(n,dtype=bool)
    for i in range(n):
        for j in range(n):
            if i==j:
                continue
            if p[j] <= p[i] and w[j] <= w[i] and (p[j] < p[i] or w[j] < w[i]):
                keep[i]=False
                break
    return keep

def weighted_winner(p,w,alpha):
    pn=(p-p.min())/max(p.max()-p.min(),1e-12)
    wn=(w-w.min())/max(w.max()-w.min(),1e-12)
    return int(np.argmin(alpha*pn+(1-alpha)*wn))

def run_sensitivity(n=5000, seed=20260914):
    df=load_witness()
    states=df["state_abbr"].astype(str).tolist()
    p0=df["pue"].to_numpy(float)
    w0=df["wue"].to_numpy(float)
    base_pairs=baseline_pairs(df)
    base_front=tuple(np.where(pareto_mask(p0,w0))[0].tolist())
    rng=np.random.default_rng(seed)
    rows=[]
    trial_sample=[]
    pairs_all=list(itertools.combinations(range(len(df)),2))
    for sigma in [0.0,0.005,0.01,0.02,0.05]:
        if sigma==0:
            P=np.repeat(p0[None,:],n,axis=0)
            W=np.repeat(w0[None,:],n,axis=0)
        else:
            P=p0[None,:]*np.exp(rng.normal(0,sigma,size=(n,len(p0))))
            W=w0[None,:]*np.exp(rng.normal(0,sigma,size=(n,len(w0))))
        alphas=rng.uniform(0,1,size=n)
        rev_counts=np.zeros(n,dtype=int)
        base_surv=np.zeros(n,dtype=float)
        for t in range(n):
            rev=set()
            for i,j in pairs_all:
                dp=P[t,i]-P[t,j]
                dw=W[t,i]-W[t,j]
                if dp!=0 and dw!=0 and np.sign(dp)!=np.sign(dw):
                    rev.add((i,j))
            rev_counts[t]=len(rev)
            if base_pairs:
                base_surv[t]=sum((i,j) in rev for i,j in base_pairs)/len(base_pairs)
        fronts=[]
        winners=np.empty(n,dtype=int)
        for t in range(n):
            fronts.append(tuple(np.where(pareto_mask(P[t],W[t]))[0].tolist()))
            winners[t]=weighted_winner(P[t],W[t],alphas[t])
        vals, counts=np.unique(winners,return_counts=True)
        mc=vals[np.argmax(counts)]
        probs=counts/counts.sum()
        rows.append({
            "sigma":sigma,
            "trials":n,
            "prob_any_pairwise_reversal":float(np.mean(rev_counts>0)),
            "mean_baseline_reversal_survival":float(base_surv.mean()),
            "prob_baseline_pareto_front_preserved":float(np.mean([f==base_front for f in fronts])),
            "most_common_weighted_winner":states[int(mc)],
            "most_common_winner_fraction":float(counts.max()/n),
            "winner_entropy":float(-(probs*np.log(probs)).sum()),
            "number_of_distinct_winners":int(len(vals))
        })
        for t in range(min(100,n)):
            trial_sample.append({
                "sigma":sigma,
                "trial":t,
                "pairwise_reversal_count":int(rev_counts[t]),
                "pareto_front":"|".join(states[i] for i in fronts[t]),
                "weight_pue":float(alphas[t]),
                "winner":states[int(winners[t])]
            })
    return pd.DataFrame(rows), pd.DataFrame(trial_sample), {
        "baseline_reversal_count":len(base_pairs),
        "baseline_reversals":[[states[i],states[j]] for i,j in base_pairs],
        "baseline_pareto_front":[states[i] for i in base_front]
    }

def main():
    OUT.mkdir(exist_ok=True)
    summary,trials,baseline=run_sensitivity()
    summary.to_csv(OUT/"phase6de_robustness_summary.csv",index=False)
    trials.to_csv(OUT/"phase6de_robustness_trials_sample.csv",index=False)
    fig,ax=plt.subplots(figsize=(7,4))
    ax.plot(summary["sigma"],summary["prob_any_pairwise_reversal"],marker="o",label="Any ordering reversal")
    ax.plot(summary["sigma"],summary["prob_baseline_pareto_front_preserved"],marker="o",label="Baseline Pareto front preserved")
    ax.set_xlabel("multiplicative perturbation sigma")
    ax.set_ylabel("probability")
    ax.set_ylim(0,1.02)
    ax.set_title("External ordering robustness")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT/"phase6de_robustness.png",dpi=180)
    plt.close(fig)
    payload={
        "seed":20260914,
        "trials_per_sigma":5000,
        "scope_note":"Perturbation scales are sensitivity stress tests, not empirical measurement-error estimates.",
        "baseline":baseline,
        "sensitivity":summary.to_dict(orient="records")
    }
    (OUT/"phase6de_summary.json").write_text(json.dumps(payload,indent=2))
    print(json.dumps(payload,indent=2))

if __name__=="__main__":
    main()
