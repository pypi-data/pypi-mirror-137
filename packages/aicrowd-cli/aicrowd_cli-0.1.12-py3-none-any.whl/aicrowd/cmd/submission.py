"""
Submission subcommand
"""
import click

from aicrowd.contexts import (
    ChallengeContext,
    ConfigContext,
    pass_challenge,
    pass_config,
)
from aicrowd.utils.utils import exception_handler
from aicrowd.utils import AliasedGroup, CommandWithExamples


@click.group(name="submission", cls=AliasedGroup)
def submission_command():
    """
    Create and view submissions
    """


@click.command(name="create", cls=CommandWithExamples)
@click.option(
    "-c",
    "--challenge",
    type=str,
    help="Specify challenge explicitly",
)
@click.option(
    "-f",
    "--file",
    "file_path",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    help="The file to submit",
)
@click.option(
    "-d",
    "--description",
    type=str,
    help="Submission description",
    default="",
)
@click.option(
    "-t", "--tag", "submission_tag", type=str, help="[Git submissions] The tag to push"
)
@click.option(
    "--no-verify",
    is_flag=True,
    help="Disbale pre-submission sanity checks",
    default=False,
)
@pass_challenge
@pass_config
@exception_handler
def create_subcommand(
    config_ctx: ConfigContext,
    challenge_ctx: ChallengeContext,
    challenge: str,
    file_path: str,
    description: str,
    submission_tag: str,
    no_verify: bool,
):
    """
    Create a submission on AIcrowd

    You can use this same command to create both normal submissions and git based submissions.

    Examples:
      # submit a file for a challenge
      aicrowd submission create -c CHALLENGE -f submission.file -d "this is a sample submission"

      # or, you can create git submissions too
      # note that:
      #   1. no -f (the whole repo is submitted)
      #   2. no -c (the challenge is inferred from local git config)
      aicrowd submission create -t v3.0 -d "tried out some cool stuff"
    """
    from aicrowd.submission import create_submission

    print(
        create_submission(
            challenge,
            file_path,
            description,
            True,
            submission_tag,
            config_ctx,
            challenge_ctx,
            no_verify,
        )
    )


submission_command.add_command(create_subcommand)
