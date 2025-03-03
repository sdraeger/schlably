import wandb
import click


@click.command()
@click.option(
    "--entity",
    type=str,
    required=True,
    help="The entity (user or team) to use for the run.",
)
@click.option(
    "--project",
    type=str,
    required=True,
    help="The project name to use for the run.",
)
@click.option(
    "--run_id",
    type=str,
    required=True,
    help="The ID of the run to download results from.",
)
def main(entity, project, run_id):
    api = wandb.Api()

    # A run is specified by <entity>/<project>/<run_id>
    run = api.run(f"{entity}/{project}/{run_id}")

    metrics_dataframe = run.history()
    metrics_dataframe.to_csv("metrics.csv")


if __name__ == "__main__":
    main()
