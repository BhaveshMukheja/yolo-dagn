import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def compute_statistics(values, bins=80, column_name=None):
    """
    Compute standard descriptive statistics used in scientific analysis.
    """

    stats = {}

    stats["N"] = len(values)
    stats["mean"] = values.mean()
    stats["median"] = values.median()
    stats["std"] = values.std()
    stats["min"] = values.min()
    stats["max"] = values.max()

    # Mode (may return multiple values)
    mode_vals = values.mode()
    stats["mode"] = mode_vals.iloc[0] if not mode_vals.empty else None
    stats["mode_frequency"] = (values == stats["mode"]).sum() if stats["mode"] is not None else 0

    # Percentiles
    stats["p25"] = values.quantile(0.25)
    stats["p75"] = values.quantile(0.75)

    # Histogram bin analysis
    counts, bin_edges = np.histogram(values, bins=bins)
    max_bin_index = np.argmax(counts)

    stats["max_bin_count"] = counts[max_bin_index]
    stats["max_bin_range"] = (
        bin_edges[max_bin_index],
        bin_edges[max_bin_index + 1]
    )

    # --- Arcsec-specific thresholds ---
    if column_name == "dist_arcsec":
        stats["count_gt_5_arcsec"] = (values > 5).sum()
        stats["count_gt_6_arcsec"] = (values > 6).sum()

        stats["fraction_gt_5_arcsec"] = stats["count_gt_5_arcsec"] / stats["N"]
        stats["fraction_gt_6_arcsec"] = stats["count_gt_6_arcsec"] / stats["N"]

    return stats


def plot_histogram(data, column_name, bins=80, output_dir="histograms"):
    """
    Create histogram and compute statistics.
    """

    if column_name not in data.columns:
        logging.error(f"Column '{column_name}' not found.")
        return

    os.makedirs(output_dir, exist_ok=True)

    values = data[column_name].dropna()

    stats = compute_statistics(values, bins, column_name)

    plt.figure(figsize=(8, 5))

    plt.hist(
        values,
        bins=bins,
        color="#A37FD3",
        edgecolor="white",
        linewidth=0.8,
        alpha=0.9
    )

    plt.xlabel("Projected Separation in Arcseconds" if column_name == "dist_arcsec" else column_name, fontsize=12)
    plt.ylabel("Count", fontsize=12)

    # Annotate key stats
    text = (
        f"Mean = {stats['mean']:.3f}\n"
        f"Median = {stats['median']:.3f}\n"
        f"Std = {stats['std']:.3f}"
    )

    # Add arcsec thresholds if applicable
    if column_name == "dist_arcsec":
        text += (
            f"\n>5\" = {stats['count_gt_5_arcsec']}"
            f"\n>6\" = {stats['count_gt_6_arcsec']}"
        )

    plt.text(
        0.97,
        0.97,
        text,
        transform=plt.gca().transAxes,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(facecolor="white", alpha=0.8)
    )

    plt.tight_layout()

    output_file = os.path.join(output_dir, f"{column_name}_histogram.png")
    plt.savefig(output_file, dpi=300)
    plt.close()

    logging.info(f"{column_name} histogram saved: {output_file}")
    logging.info(f"{column_name} statistics: {stats}")

    return stats


def generate_histograms_from_csv(csv_file, bins=80, output_dir="histograms"):

    df = pd.read_csv(csv_file)

    stats_arcsec = plot_histogram(df, "dist_arcsec", bins, output_dir)
    stats_kpc = plot_histogram(df, "dist_kpc", bins, output_dir)

    # Combine stats safely (handle missing keys)
    stats_df = pd.DataFrame([stats_arcsec, stats_kpc],
                            index=["dist_arcsec", "dist_kpc"])

    stats_file = os.path.join(output_dir, "statistics_summary.csv")
    stats_df.to_csv(stats_file)

    logging.info(f"Statistics saved to {stats_file}")

# def generate_histograms_from_csv(csv_file, bins=80, output_dir="histograms"):

#     df = pd.read_csv(csv_file)

#     stats_arcsec = plot_histogram(df, "dist_arcsec", bins, output_dir)
#     stats_kpc = plot_histogram(df, "dist_kpc", bins, output_dir)

#     # --- Top 5 largest separations ---
#     if "objID" in df.columns and "dist_arcsec" in df.columns:
#         top5 = df.nlargest(5, "dist_arcsec")[["objID", "dist_arcsec"]]

#         logging.info("Top 5 largest separations (arcsec):")
#         logging.info(f"\n{top5}")

#         # Save to CSV (useful for paper/reference)
#         top5_file = os.path.join(output_dir, "top5_largest_separations.csv")
#         top5.to_csv(top5_file, index=False)

#         logging.info(f"Top 5 separations saved to {top5_file}")
#     else:
#         logging.warning("Columns 'objID' or 'dist_arcsec' not found. Skipping top 5 extraction.")

#     # Save statistics
#     stats_df = pd.DataFrame([stats_arcsec, stats_kpc],
#                             index=["dist_arcsec", "dist_kpc"])

#     stats_file = os.path.join(output_dir, "statistics_summary.csv")
#     stats_df.to_csv(stats_file)

#     logging.info(f"Statistics saved to {stats_file}")

def main():
    csv_filename = r"results\finalModel\projected_separations.csv"
    generate_histograms_from_csv(csv_filename)


if __name__ == "__main__":
    main()