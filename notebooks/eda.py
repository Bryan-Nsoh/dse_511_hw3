import os
import math
import textwrap
import pandas as pd
import seaborn as sns
import matplotlib

# Use non-interactive backend for headless environments
matplotlib.use("Agg")
import matplotlib.pyplot as plt


DATA_PATH = "data/cleaned/SGO-ADS-crash-data-clean.csv"
FIG_DIR = "notebooks/figures"
SUMMARY_MD = "notebooks/eda_summary.md"


def safe_numeric(s):
    return pd.to_numeric(s, errors="coerce")


def main():
    os.makedirs(FIG_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    # Standardize expected columns if present
    # Work defensively: only operate on columns that exist
    cols = set(df.columns.str.strip())

    # Rename common variations to expected names
    rename_map = {}
    for cand, target in [
        ("sv_pre_crash_movement", "sv_pre_crash_movement"),
        ("sv_precrash_speed_mph", "sv_precrash_speed_mph"),
        ("model_year", "model_year"),
        ("make", "make"),
        ("year", "year"),
    ]:
        if cand in df.columns and cand != target:
            rename_map[cand] = target

    if rename_map:
        df = df.rename(columns=rename_map)

    # Coerce numeric columns
    if "sv_precrash_speed_mph" in df.columns:
        df["sv_precrash_speed_mph"] = safe_numeric(df["sv_precrash_speed_mph"])  # type: ignore
    if "model_year" in df.columns:
        df["model_year"] = safe_numeric(df["model_year"])  # type: ignore
    if "year" in df.columns:
        df["year"] = safe_numeric(df["year"])  # type: ignore

    # Basic stats
    n_rows = int(len(df))
    n_cols = int(df.shape[1])

    speed_stats = {}
    if "sv_precrash_speed_mph" in df.columns:
        sp = df["sv_precrash_speed_mph"].dropna()
        if len(sp) > 0:
            speed_stats = {
                "count": int(sp.count()),
                "mean": float(sp.mean()),
                "median": float(sp.median()),
                "std": float(sp.std(ddof=1)) if len(sp) > 1 else math.nan,
                "min": float(sp.min()),
                "max": float(sp.max()),
            }

    top_makes = []
    if "make" in df.columns:
        top_makes = (
            df["make"].dropna().astype(str).str.strip().value_counts().head(10).to_dict()
        )

    counts_by_year = {}
    if "year" in df.columns:
        counts_by_year = (
            df["year"].dropna().astype(int).value_counts().sort_index().to_dict()
        )

    corr_speed_modelyear = None
    if set(["sv_precrash_speed_mph", "model_year"]).issubset(df.columns):
        corr = (
            df[["sv_precrash_speed_mph", "model_year"]]
            .dropna()
            .corr(numeric_only=True)
            .iloc[0, 1]
        )
        if pd.notna(corr):
            corr_speed_modelyear = float(corr)

    # Figures
    if "sv_precrash_speed_mph" in df.columns and df["sv_precrash_speed_mph"].notna().any():
        plt.figure(figsize=(7, 4))
        sns.histplot(df["sv_precrash_speed_mph"], bins=20, kde=True, color="#3366cc")
        plt.xlabel("Pre-crash speed (mph)")
        plt.ylabel("Count")
        plt.title("Distribution of Pre-crash Speed (mph)")
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, "speed_hist.png"), dpi=150)
        plt.close()

    if "make" in df.columns and df["make"].notna().any():
        top10 = (
            df["make"].dropna().astype(str).str.strip().value_counts().head(10)
        )
        if len(top10) > 0:
            plt.figure(figsize=(8, 4.5))
            sns.barplot(x=top10.values, y=top10.index, color="#33a02c")
            plt.xlabel("Count")
            plt.ylabel("Make (top 10)")
            plt.title("Top 10 Makes in ADS Crash Reports")
            plt.tight_layout()
            plt.savefig(os.path.join(FIG_DIR, "top_makes.png"), dpi=150)
            plt.close()

    # Persist human-readable summary only (JSON removed per project scope)

    def fmt_speed(stats):
        if not stats:
            return "(sv_precrash_speed_mph not available)"
        def f(v):
            return "NA" if (v is None or (isinstance(v, float) and math.isnan(v))) else f"{v:,.2f}"
        return (
            f"count={stats.get('count', 0)}, mean={f(stats.get('mean'))}, "
            f"median={f(stats.get('median'))}, std={f(stats.get('std'))}, min={f(stats.get('min'))}, max={f(stats.get('max'))}"
        )

    lines = [
        "# EDA Summary",
        "",
        f"Rows: {n_rows}  |  Columns: {n_cols}",
        "",
        "## Pre-crash Speed (mph) Stats",
        fmt_speed(speed_stats),
        "",
        "## Top 10 Makes",
        "(none)" if not top_makes else "\n".join([f"- {k}: {v}" for k, v in top_makes.items()]),
        "",
        "## Counts by Year",
        "(none)" if not counts_by_year else "\n".join([f"- {int(k)}: {v}" for k, v in sorted(counts_by_year.items())]),
        "",
        "## Correlation",
        (
            "sv_precrash_speed_mph vs model_year: NA"
            if corr_speed_modelyear is None
            else f"sv_precrash_speed_mph vs model_year: {corr_speed_modelyear:.4f}"
        ),
        "",
        "## Figures",
        "- speed_hist.png",
        "- top_makes.png",
        "",
    ]
    with open(SUMMARY_MD, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
