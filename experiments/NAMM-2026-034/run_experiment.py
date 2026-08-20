"""NAMM-2026-034: AMAT multi-embedder gate stability sweep."""



from __future__ import annotations



import json

import logging

from datetime import datetime, timezone

from pathlib import Path



import yaml



from namm.llm.env import load_env

from namm.metrics.gate_calibration import (

    resolve_embedders_for_sweep,

    run_multi_embedder_calibration,

)



ARTIFACTS = Path(__file__).resolve().parent / "artifacts"

EXPERIMENT_ID = "NAMM-2026-034"





def _load_config() -> dict:

    with (Path(__file__).parent / "config.yaml").open(encoding="utf-8") as f:

        return yaml.safe_load(f)





def _load_resume_null(path: Path) -> set[int]:

    indices: set[int] = set()

    if not path.is_file():

        return indices

    for line in path.read_text(encoding="utf-8").splitlines():

        if line.strip():

            rec = json.loads(line)

            if "seed_idx" in rec:

                indices.add(int(rec["seed_idx"]))

    return indices





def _load_resume_chat_keys(path: Path, prompts: list[str]) -> set[tuple[str, int]]:

    keys: set[tuple[str, int]] = set()

    if not path.is_file():

        return keys

    for line in path.read_text(encoding="utf-8").splitlines():

        if not line.strip():

            continue

        rec = json.loads(line)

        cell = rec.get("cell") or rec

        up = cell.get("user_prompt") or cell.get("prompt_preview", "")

        for p in prompts:

            if up in p or p.startswith(up[:40]):

                keys.add((p, int(cell.get("n_turns", 0))))

                break

    return keys





def _load_shared_chat_cells(path: Path) -> list[dict]:
    cells: list[dict] = []
    if not path.is_file():
        return cells
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            if rec.get("cell"):
                cells.append(rec["cell"])
    return cells


def _load_null_d_med(path: Path) -> list[float]:
    vals: list[float] = []
    if not path.is_file():
        return vals
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            vals.append(float(json.loads(line)["d_med"]))
    return vals


def run_namm_2026_034(*, skip_chat: bool = False) -> dict:

    load_env()

    cfg = _load_config()

    llm = cfg.get("llm") or {}

    loop = cfg.get("loop") or {}

    cal_cfg = cfg.get("gate_calibration") or {}

    null_cfg = cal_cfg.get("null_sampling") or {}

    cross_cfg = cfg.get("cross_embedder") or {}

    ARTIFACTS.mkdir(parents=True, exist_ok=True)



    prompts = loop.get("prompts") or []

    n_seeds = int(null_cfg.get("n_seeds", 20))

    embedders = resolve_embedders_for_sweep(cfg)

    logging.info("embedders=%s", [e["provider"] for e in embedders])



    chat_cells_path = ARTIFACTS / "shared_chat_cells.jsonl"

    resume_chat = _load_resume_chat_keys(chat_cells_path, prompts)
    preloaded_cells = _load_shared_chat_cells(chat_cells_path)



    def on_null(provider: str, rec: dict) -> None:

        path = ARTIFACTS / f"null_samples_{provider}.jsonl"

        with path.open("a", encoding="utf-8") as f:

            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        logging.info("[%s] null seed=%s d_med=%.4f", provider, rec["seed_idx"], rec["d_med"])



    resume_null: dict[str, set[int]] = {}
    preloaded_null: dict[str, list[float]] = {}
    for emb in embedders:
        p = emb["provider"]
        null_path = ARTIFACTS / f"null_samples_{p}.jsonl"
        resume_null[p] = _load_resume_null(null_path)
        preloaded_null[p] = _load_null_d_med(null_path)

    def on_chat_cell(cell: dict) -> None:
        rec = {"ts": datetime.now(timezone.utc).isoformat(), "cell": cell}
        with chat_cells_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        logging.info("chat cell turns=%s prompt=%s...", cell["n_turns"], cell["prompt_preview"][:40])

    result = run_multi_embedder_calibration(
        embedders=embedders,
        prompts=prompts,
        turn_values=[int(t) for t in loop.get("turn_values", [3, 6])],
        cal_cfg=cal_cfg,
        null_cfg=null_cfg,
        chat_provider=llm.get("chat_provider"),
        chat_model=llm.get("chat_model"),
        pause_s=float(llm.get("pause_s", 2.0)),
        skip_chat=skip_chat,
        on_null_sample=on_null,
        resume_null_by_embedder=resume_null,
        preloaded_null_by_embedder=preloaded_null,
        resume_chat_keys=resume_chat,
        cross_cfg=cross_cfg,
        on_chat_cell=on_chat_cell,
        preloaded_chat_cells=preloaded_cells or None,
    )

    for br in result.get("branches", []):
        prov = br["embed_provider"]
        (ARTIFACTS / f"calibrated_thresholds_{prov}.json").write_text(
            json.dumps(br["calibrated_thresholds"], indent=2), encoding="utf-8"
        )
        cells_path = ARTIFACTS / f"live_loop_cells_{prov}.jsonl"
        cell_lines = []
        for cell in br["cells"]:
            rec = {"ts": datetime.now(timezone.utc).isoformat(), "embed_provider": prov, "cell": cell}
            cell_lines.append(json.dumps(rec, ensure_ascii=False))
        cells_path.write_text("\n".join(cell_lines) + ("\n" if cell_lines else ""), encoding="utf-8")



    (ARTIFACTS / "cross_embedder.json").write_text(

        json.dumps(result.get("cross_embedder", {}), indent=2, ensure_ascii=False), encoding="utf-8"

    )



    s = result.get("summary") or {}

    cross = result.get("cross_embedder") or {}

    cert_tiers = cfg.get("certificate_tiers") or {}
    required_names = [
        e["provider"]
        for e in embedders
        if e["provider"] in (cfg.get("embedders") or {}).get("required", ["openai"])
    ]
    completed = result.get("embedders_completed", [])
    required_done = all(r in completed for r in required_names)

    if skip_chat:
        cert = "PROMPT_PILOT"
    elif required_done:
        cert = "CALIBRATION_PARTIAL"
        rho = cross.get("mean_spearman_rho")
        agree = cross.get("lift_agreement_fraction") or 0.0
        if len(completed) >= 2 and ((rho is not None and rho >= 0.5) or agree >= 0.5):
            cert = "LIVE_PARTIAL"
        pass_fracs = [b["summary"]["calibrated_lock_gate_pass_fraction"] for b in result.get("branches", [])]
        if len(completed) >= 2 and sum(1 for pf in pass_fracs if pf > 0.3) >= 2 and agree >= 0.5:
            cert = "LIVE_EVIDENCE"
    else:
        cert = "NULL"

    payload = {

        "experiment_id": EXPERIMENT_ID,

        "domain": cfg.get("domain"),

        "hypothesis_id": cfg.get("hypothesis_id"),

        "protocol_version": cfg.get("protocol_version"),

        "timestamp": datetime.now(timezone.utc).isoformat(),

        "mode": result.get("mode"),

        "llm": {k: v for k, v in llm.items() if k != "api_key"},

        "embedders": embedders,

        "embedders_completed": result.get("embedders_completed", []),

        "metrics": s,

        "cross_embedder": cross,

        "branches_summary": [

            {

                "embed_provider": b["embed_provider"],

                "calibrated_thresholds": b["calibrated_thresholds"],

                "summary": b["summary"],

            }

            for b in result.get("branches", [])

        ],

        "hypothesis_support": result.get("hypothesis_support", {}),

        "certificate": cert,

        "certificate_tiers": cert_tiers,

        "errors": result.get("errors", []),

        "prior_experiments": cfg.get("prior_experiments"),

    }



    (ARTIFACTS / "summary.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    (ARTIFACTS / "full_multi_embedder.json").write_text(

        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"

    )

    return payload





if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    res = run_namm_2026_034()

    lines = [

        f"{res['timestamp']} {EXPERIMENT_ID} complete",

        f"certificate={res['certificate']}",

        f"embedders={res.get('embedders_completed')}",

        f"mean_spearman={res['cross_embedder'].get('mean_spearman_rho')}",

        f"lift_agreement={res['cross_embedder'].get('lift_agreement_fraction')}",

        f"errors={len(res.get('errors', []))}",

    ]

    log_text = "\n".join(lines) + "\n"

    for log_path in (ARTIFACTS / "experiment.log", Path(__file__).parent / "run.log"):

        try:

            log_path.write_text(log_text, encoding="utf-8")

            break

        except OSError:

            continue

    print(f"{EXPERIMENT_ID} complete. certificate={res['certificate']}")

    print(f"embedders={res.get('embedders_completed')} spearman={res['cross_embedder'].get('mean_spearman_rho')}")


