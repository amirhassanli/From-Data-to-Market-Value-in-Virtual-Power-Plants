#!/usr/bin/env python3
"""
01_prisma_pipeline.py
Reads raw database exports (Scopus CSV, Web of Science tab-delimited .txt, IEEE Xplore CSV),
deduplicates, applies the eligibility filters, builds the screening sheet, computes the PRISMA counts,
runs the recall check of the coded core, and draws Fig. 1 (PRISMA 2020 flow).

Folder layout (default):
  exports/scopus*.csv      exports/wos*.txt      exports/ieee*.csv
  search_log.csv           columns: database,date,query      (database in {Scopus,WoS,IEEE})
  dmdi_matrix.csv          (optional, for the recall check; needs columns key,label,doi,verified)
Outputs: prisma_values.json, screening_sheet.csv, core_recall.csv, fig1_prisma.png

Usage: python 01_prisma_pipeline.py --exports exports --log search_log.csv --core dmdi_matrix.csv
Run it again after you fill ta_decision / ft_decision in screening_sheet.csv (decisions are preserved).
"""
import argparse, glob, json, re, unicodedata
from pathlib import Path
import pandas as pd

YEAR_MIN, YEAR_MAX = 2018, 2026
OK_TYPES = ("article", "conference paper", "review", "proceedings paper", "journals",
            "conferences", "early access")
VPP_RE = re.compile(r"virtual power plant|\bVPPs?\b|virtual aggregator|flexibility aggregator", re.I)
TOPIC_RE = re.compile(r"bidding|market|scheduling|dispatch|energy management|uncertaint|stochastic|robust|"
                      r"unit commitment|reinforcement|deep learning|data-driven|forecast|carbon|"
                      r"green certificate|ancillary|reserve|settlement|imbalance", re.I)
FIELDS = {"Scopus": "Title/Abstract/Keywords", "WoS": "Topic", "IEEE": "Full text & metadata"}


def pick(df, *names):
    for n in names:
        if n in df.columns:
            return df[n].fillna("").astype(str)
    return pd.Series([""] * len(df), index=df.index)


def norm_doi(x):
    x = str(x).strip().lower()
    x = re.sub(r"^https?://(dx\.)?doi\.org/", "", x)
    return x if x.startswith("10.") else ""


def norm_title(t):
    t = unicodedata.normalize("NFKD", str(t)).lower()
    return re.sub(r"[^a-z0-9]", "", t)


def load(db, files):
    frames = []
    for f in files:
        if db == "WoS":
            df = pd.read_csv(f, sep="\t", quoting=3, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
            m = pd.DataFrame({"title": pick(df, "TI"), "year": pick(df, "PY"), "doi": pick(df, "DI"),
                              "doctype": pick(df, "DT"), "language": pick(df, "LA"), "abstract": pick(df, "AB"),
                              "keywords": pick(df, "DE"), "source": pick(df, "SO")})
        elif db == "Scopus":
            df = pd.read_csv(f, encoding="utf-8-sig", dtype=str)
            m = pd.DataFrame({"title": pick(df, "Title"), "year": pick(df, "Year"), "doi": pick(df, "DOI"),
                              "doctype": pick(df, "Document Type"),
                              "language": pick(df, "Language of Original Document"),
                              "abstract": pick(df, "Abstract"), "keywords": pick(df, "Author Keywords"),
                              "source": pick(df, "Source title")})
        else:  # IEEE
            df = pd.read_csv(f, encoding="utf-8-sig", dtype=str)
            m = pd.DataFrame({"title": pick(df, "Document Title"), "year": pick(df, "Publication Year"),
                              "doi": pick(df, "DOI"), "doctype": pick(df, "Content Type"),
                              "language": "", "abstract": pick(df, "Abstract"),
                              "keywords": pick(df, "Author Keywords"), "source": pick(df, "Publication Title")})
        m["db"] = db
        frames.append(m)
    if not frames:
        return pd.DataFrame(columns=["title", "year", "doi", "doctype", "language", "abstract",
                                     "keywords", "source", "db"])
    return pd.concat(frames, ignore_index=True)


def prisma_figure(v, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig, ax = plt.subplots(figsize=(7.2, 8.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")
    def box(x, y, w, h, txt, fc="#eaf1fb"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=fc, ec="#27496d", lw=1))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=7.6)
    def arrow(x, y1, y2):
        ax.annotate("", xy=(x, y2), xytext=(x, y1), arrowprops=dict(arrowstyle="->", color="#27496d"))
    box(0.3, 10.2, 6.2, 1.5, f"Records identified from databases (n = {v['N_IDENTIFIED']})\n"
        f"Scopus n = {v['N_SCOPUS']}; Web of Science n = {v['N_WOS']}; IEEE Xplore n = {v['N_IEEE']}")
    box(6.9, 10.2, 2.8, 1.5, f"Duplicates removed\n(n = {v['N_DUPLICATES']})", "#fdf0e0")
    arrow(3.4, 10.2, 9.3)
    box(0.3, 7.9, 6.2, 1.4, f"Records after deduplication (n = {v['N_AFTER_DEDUP']})")
    box(6.9, 7.9, 2.8, 1.4, f"Excluded by automated filters\n(year, language, type, topic)\n(n = {v['N_AUTO_EXCL']})", "#fdf0e0")
    arrow(3.4, 7.9, 7.0)
    box(0.3, 5.6, 6.2, 1.4, f"Records screened on title/abstract (n = {v['N_TA_SCREENED']})")
    box(6.9, 5.6, 2.8, 1.4, f"Excluded at title/abstract\n(n = {v['N_TA_EXCL']})", "#fdf0e0")
    arrow(3.4, 5.6, 4.7)
    box(0.3, 3.3, 6.2, 1.4, f"Reports assessed for eligibility (n = {v['N_FT_ASSESSED']})")
    box(6.9, 3.3, 2.8, 1.4, f"Excluded after full-text\nassessment (n = {v['N_FT_EXCL']})", "#fdf0e0")
    arrow(3.4, 3.3, 2.4)
    box(0.3, 0.9, 6.2, 1.5, f"Eligible records from database search (n = {v['N_INCLUDED']})\n"
        f"Coded core: n = {v['N_CORE']}; retrieved by the search: {v['N_CORE_RECALLED']}/{v['N_CORE_DOI']} "
        f"({v['RECALL_PCT']}%)", "#e6f4ea")
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exports", default="exports")
    ap.add_argument("--log", default="search_log.csv")
    ap.add_argument("--core", default="dmdi_matrix.csv")
    ap.add_argument("--sheet", default="screening_sheet.csv")
    ap.add_argument("--out", default="prisma_values.json")
    a = ap.parse_args()

    ex = Path(a.exports)
    files = {"Scopus": sorted(glob.glob(str(ex / "scopus*.csv"))),
             "WoS": sorted(glob.glob(str(ex / "wos*.txt"))),
             "IEEE": sorted(glob.glob(str(ex / "ieee*.csv")))}
    raw = pd.concat([load(db, fl) for db, fl in files.items()], ignore_index=True)
    raw["doi"] = raw["doi"].map(norm_doi)
    raw["tkey"] = raw["title"].map(norm_title)
    raw["year_i"] = pd.to_numeric(raw["year"], errors="coerce")
    n_by_db = raw["db"].value_counts().to_dict()

    # --- deduplication: DOI first, then normalised title + year
    raw["order"] = raw["db"].map({"Scopus": 0, "WoS": 1, "IEEE": 2})
    raw = raw.sort_values("order")
    dbs_per_doi = raw[raw.doi != ""].groupby("doi")["db"].agg(lambda s: "+".join(sorted(set(s))))
    d1 = pd.concat([raw[raw.doi != ""].drop_duplicates("doi"), raw[raw.doi == ""]])
    d2 = d1.drop_duplicates(["tkey", "year"])
    n_ident = len(raw); n_dedup = len(d2)

    # --- automated eligibility filters
    def ok_row(r):
        if not (YEAR_MIN <= (r.year_i if pd.notna(r.year_i) else 0) <= YEAR_MAX):
            return "year"
        if r.language and "english" not in r.language.lower() and r.language.lower() not in ("en", "eng"):
            return "language"
        if r.doctype and not any(t in r.doctype.lower() for t in OK_TYPES):
            return "document_type"
        text = f"{r.title} {r.abstract} {r.keywords}"
        if not (VPP_RE.search(text) and TOPIC_RE.search(text)):
            return "topic"
        return ""
    d2 = d2.copy()
    d2["auto_reason"] = d2.apply(ok_row, axis=1)
    elig = d2[d2.auto_reason == ""].copy()
    reasons = d2[d2.auto_reason != ""]["auto_reason"].value_counts().to_dict()

    # --- screening sheet (existing decisions are preserved)
    elig["id"] = elig.apply(lambda r: r.doi if r.doi else r.tkey, axis=1)
    elig["dbs"] = elig["doi"].map(dbs_per_doi).fillna(elig["db"])
    sheet = elig[["id", "title", "year", "doi", "source", "dbs", "abstract"]].copy()
    for c in ("ta_decision", "ta_reason", "ft_decision", "ft_reason"):
        sheet[c] = ""
    p = Path(a.sheet)
    if p.exists():
        old = pd.read_csv(p, dtype=str).fillna("").set_index("id")
        for c in ("ta_decision", "ta_reason", "ft_decision", "ft_reason"):
            sheet[c] = sheet["id"].map(old[c]).fillna("")
    sheet.to_csv(p, index=False, encoding="utf-8-sig")

    ta = sheet.ta_decision.str.lower().str.strip()
    ft = sheet.ft_decision.str.lower().str.strip()
    pending_ta = int((ta == "").sum())
    ta_ex = int((ta == "exclude").sum())
    ft_set = sheet[ta == "include"]
    ft_ass = len(ft_set)
    ft_dec = ft_set.ft_decision.str.lower().str.strip()
    pending_ft = int((ft_dec == "").sum())
    ft_ex = int((ft_dec == "exclude").sum())
    incl = int((ft_dec == "include").sum())

    v = {"N_SCOPUS": n_by_db.get("Scopus", 0), "N_WOS": n_by_db.get("WoS", 0), "N_IEEE": n_by_db.get("IEEE", 0),
         "N_IDENTIFIED": n_ident, "N_DUPLICATES": n_ident - n_dedup, "N_AFTER_DEDUP": n_dedup,
         "N_AUTO_EXCL": n_dedup - len(elig), "N_TA_SCREENED": len(elig),
         "N_TA_EXCL": ta_ex if pending_ta == 0 else "PENDING",
         "N_FT_ASSESSED": ft_ass if pending_ta == 0 else "PENDING",
         "N_FT_EXCL": ft_ex if (pending_ta == 0 and pending_ft == 0) else "PENDING",
         "N_INCLUDED": incl if (pending_ta == 0 and pending_ft == 0) else "PENDING",
         "AUTO_EXCL_BREAKDOWN": reasons}

    # --- search log (dates, table)
    rows = []
    if Path(a.log).exists():
        lg = pd.read_csv(a.log, dtype=str).fillna("")
        for _, r in lg.iterrows():
            key = {"scopus": "Scopus", "wos": "WoS", "web of science": "WoS", "ieee": "IEEE"}.get(r["database"].lower(), r["database"])
            v[f"DATE_{key.upper()}"] = r["date"]
    names = {"Scopus": "Scopus", "WoS": "Web of Science Core Collection", "IEEE": "IEEE Xplore"}
    tab = ["| Database | Search date | Fields searched | Records retrieved |", "|---|---|---|---|"]
    for k in ("Scopus", "WoS", "IEEE"):
        tab.append(f"| {names[k]} | {v.get('DATE_' + k.upper(), 'MISSING')} | {FIELDS[k]} | {n_by_db.get(k, 0)} |")
    tab.append(f"| Total (before deduplication) | | | {n_ident} |")
    v["TABLE_SEARCH_LOG"] = "\n".join(tab)

    # --- recall check of the coded core
    v.update({"N_CORE_DOI": "NA", "N_CORE_RECALLED": "NA", "RECALL_PCT": "NA"})
    if Path(a.core).exists():
        core = pd.read_csv(a.core, dtype=str).fillna("")
        core = core[core["verified"].str.upper() != "FALSE"]
        core["doi_n"] = core["doi"].map(norm_doi)
        all_dois = set(raw["doi"])
        core["in_database_export"] = core["doi_n"].map(lambda d: (d in all_dois) if d else None)
        withdoi = core[core.doi_n != ""]
        found = int(withdoi.in_database_export.sum())
        v["N_CORE_DOI"], v["N_CORE_RECALLED"] = len(withdoi), found
        v["RECALL_PCT"] = round(100 * found / max(len(withdoi), 1), 1)
        core[["key", "label", "doi", "in_database_export"]].to_csv("core_recall.csv", index=False)
        print("Core studies WITHOUT a DOI in the CSV (fill them in):",
              core[core.doi_n == ""]["label"].tolist())
        print("Core studies NOT retrieved by the search strings:",
              withdoi[~withdoi.in_database_export.astype(bool)]["label"].tolist())
    v["N_CORE"] = int(len(core)) if Path(a.core).exists() else "NA"

    Path(a.out).write_text(json.dumps(v, indent=2, default=str), encoding="utf-8")
    try:
        prisma_figure({k: v.get(k, "NA") for k in v} | {"N_CORE": v["N_CORE"]}, "fig1_prisma.png")
    except Exception as e:  # figure is optional
        print("Figure skipped:", e)
    if pending_ta or pending_ft:
        print(f"NOTE: screening incomplete -> title/abstract pending: {pending_ta}, full-text pending: {pending_ft}")
    print(json.dumps({k: v[k] for k in v if not k.startswith("TABLE")}, indent=2, default=str))


if __name__ == "__main__":
    main()
