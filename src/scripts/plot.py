from typing import Optional

import fire
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


class PlotGenerator:
    """A CLI tool for generating plots from CSV files using Seaborn with multiple y columns."""

    def __init__(self):
        self.fig_counter = 0

    def _save_fig(self, fig: plt.Figure, filename: Optional[str] = None):
        """Helper method to save the figure with a default or custom filename."""
        if filename is None:
            filename = f"plot_{self.fig_counter}.png"
        fig.savefig(filename)
        self.fig_counter += 1
        return f"Plot saved as {filename}"

    def _load_data(self, csv_file: str):
        """Load data from CSV file."""
        try:
            return pd.read_csv(csv_file)
        except FileNotFoundError:
            return f"Error: CSV file '{csv_file}' not found"
        except Exception as e:
            return f"Error loading CSV file: {str(e)}"

    def line(
        self,
        csv_file: str,
        x_col: str,
        y_cols: list[str],
        title: str = "Line Plot",
        x_label: str = "X-axis",
        y_label: str = "Y-axis",
        filename: Optional[str] = None,
    ):
        """Generate a line plot with multiple y columns from CSV data.

        Args:
            csv_file: Path to CSV file
            x_col: Column name for x-axis
            y_cols: List of column names for y-axis (multiple lines)
            title: Plot title (default: "Line Plot")
            x_label: Label for x-axis (default: "X-axis")
            y_label: Label for y-axis (default: "Y-axis")
            filename: Output filename (default: plot_N.png)
        """
        df = self._load_data(csv_file)
        if isinstance(df, str):  # Error message
            return df

        if x_col not in df.columns:
            return f"Error: x_col '{x_col}' not found in CSV. Available columns: {list(df.columns)}"

        missing_cols = [col for col in y_cols if col not in df.columns]
        if missing_cols:
            return f"Error: y_cols {missing_cols} not found in CSV. Available columns: {list(df.columns)}"

        # Melt the DataFrame to long format for multiple y columns
        df_long = df.melt(
            id_vars=[x_col], value_vars=y_cols, var_name="Config", value_name="value"
        )

        fig, ax = plt.subplots()
        sns.lineplot(data=df_long, x=x_col, y="value", hue="Config", ax=ax)

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)

        return self._save_fig(fig, filename)


def main():
    """Entry point for the CLI application."""
    fire.Fire(PlotGenerator)


if __name__ == "__main__":
    main()
