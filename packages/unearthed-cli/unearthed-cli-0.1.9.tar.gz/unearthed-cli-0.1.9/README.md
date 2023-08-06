# Crowd ML CLI

This is the command line tool for [Unearthed Solutions CrowdML challenges](https://unearthed.solutions/).

It is designed to make model validation and submission straightforward.

Please see the [Unearthed Solutions Terms and Conditions](https://unearthed.solutions/u/terms)

# Commands

## `unearthed login`

Prompts the user for their innovator portal login and stores the tokens. You must be logged in to run other commands.

## `unearthed new`

This command asks the user which challenge they wish to download and unpack the model template for. The template will be unpacked in a named folder inside the current directory. A custom path can be specified with `unearthed new /path/to/dir/`

## `unearthed submit`

This will bundle the source code in a Docker container and then submit the code to the submission pipeline. The user is provided a link to the submission tracker, which will auto-popup in their browser, so they can track the progress and logs of their submission.

You can disable the tracker from opening in the browser by specifying `unearthed submit --no-tracker`

## `unearthed tracker`

Will open the tracker for the last submission that was made.

## `unearthed preprocess`

This command will run the preprocess code in a Docker container similar to how it will execute in the submission pipeline. It can be used to validate the preprocessing code is working before submitting.

### `unearthed train`

This command will train a model, including calling the preprocessing code, in a Docker container similar to how it will execute in the submission pipeline. It can be used to validate the training code is working before submitting.

### `unearthed predict`

This command will simulate generating predictions on the public dataset so that the predictions can be inspected locally before submitting.

### `unearhted score`

This command will run the scoring function to generate a score against the public dataset. It can be used to check the score against the public dataset before submitting.
