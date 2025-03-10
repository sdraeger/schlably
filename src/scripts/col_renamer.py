import fire
import pandas as pd
import re
from typing import Optional


class ColumnRenamer:
    """A CLI tool to rename CSV columns to 'jobX_taskY' format."""

    def rename(self, input_csv: str, output_csv: Optional[str] = None):
        """Rename columns in a CSV file to 'jobX_taskY' format.

        Args:
            input_csv: Path to input CSV file
            output_csv: Path to output CSV file (default: input_csv with '_renamed' suffix)
        """
        # Load the CSV file
        try:
            df = pd.read_csv(input_csv)
        except FileNotFoundError:
            return f"Error: Input file '{input_csv}' not found"
        except Exception as e:
            return f"Error loading CSV file: {str(e)}"

        # Function to extract job and task numbers and create new name
        def get_new_name(col_name):
            if col_name == "Step":
                return col_name
            # Extract jobX_taskY using regex
            match = re.search(r"job(\d+)_task(\d+)", col_name)
            if match:
                job_num = match.group(1)
                task_num = match.group(2)

                # Check for MIN/MAX suffixes
                if "__MIN" in col_name:
                    return f"job{job_num}_task{task_num}_min"
                elif "__MAX" in col_name:
                    return f"job{job_num}_task{task_num}_max"
                else:
                    return f"job{job_num}_task{task_num}"
            return col_name  # Return original if no match (shouldn't happen with given format)

        # Create new column names
        new_columns = {col: get_new_name(col) for col in df.columns}

        # Rename columns
        df.rename(columns=new_columns, inplace=True)

        # Determine output filename
        if output_csv is None:
            output_csv = input_csv.replace(".csv", "_renamed.csv")

        # Save the modified DataFrame
        try:
            df.to_csv(output_csv, index=False)
            return f"Columns renamed successfully. Output saved to '{output_csv}'"
        except Exception as e:
            return f"Error saving output file: {str(e)}"


def main():
    """Entry point for the CLI application."""
    fire.Fire(ColumnRenamer)


if __name__ == "__main__":
    main()
