import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import click


@click.command()
@click.option(
    "--file_path",
    type=click.Path(exists=True),
)
@click.option(
    "--output_path",
    type=click.Path(),
)
@click.option(
    "--dpi",
    type=int,
    default=300,
)
@click.option(
    "--title",
    type=str,
    default="Mean Reward by Agent",
)
def main(file_path: str, output_path: str, dpi: int, title: str):
    df = pd.read_csv(file_path)
    df["Agent"] = df["Agent"].replace("agent", "RL")

    # Determine which reward column to use
    reward_column = "Mean Reward" if "Mean Reward" in df.columns else "Reward"
    if reward_column not in df.columns:
        raise ValueError("Neither 'Mean Reward' nor 'Reward' column found in the CSV.")

    # Calculate the mean for each agent
    mean_rewards = df.groupby("Agent")[reward_column].mean().reset_index()

    # Set the style for better visualization
    fig, ax = plt.subplots()

    # Create a line plot using seaborn
    sns.lineplot(
        data=mean_rewards,
        x="Agent",
        y=reward_column,
        marker="o",  # Add markers at data points
        ax=ax,
        color="blue",  # Customize line color
        linewidth=2,  # Line thickness
    )

    # Customize the plot
    ax.set_title(title, fontsize=14, pad=15)
    ax.set_xlabel("Agent", fontsize=12)
    ax.set_ylabel("Mean Reward", fontsize=12)
    ax.tick_params(axis="x", rotation=45)  # Rotate labels using tick_params

    # Add value labels on top of each bar
    offset = 0.2
    for i, v in enumerate(mean_rewards[reward_column]):
        ax.text(
            i,
            v + offset if v >= 0 else v - offset,  # Add offset above or below
            f"{v:.2f}",
            ha="center",
            va="bottom" if v >= 0 else "top",
            fontsize=10,
        )

    # Adjust layout to prevent label cutoff
    fig.tight_layout()

    # Save the plot to the specified output path
    fig.savefig(output_path, dpi=dpi)

    # Print the mean values for reference
    print("\nMean Rewards by Agent:")
    print(mean_rewards)


if __name__ == "__main__":
    main()
