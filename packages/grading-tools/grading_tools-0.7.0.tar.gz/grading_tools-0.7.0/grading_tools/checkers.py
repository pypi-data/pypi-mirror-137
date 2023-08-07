from grading_tools import graders  # noQA F401,F403
from grading_tools.graders import *  # noQA F401,F403
from grading_tools.loaders import *  # noQA F401,F403


def check_submission(defaults, submission):
    """Function that loads grader defaults, submission, answer, and executes grading."""
    # Check for grader key
    if "grader" not in defaults:
        raise TypeError(
            "The definition for this task in index.json "
            "is missing the `'grader'` key."
        )

    grader = defaults["grader"]

    # Check that grader has required keys
    if "type" not in grader:
        raise TypeError("Your grader defaults must specify a 'type' key.")
    if "answer" not in grader:
        raise TypeError("Your grader defaults must specify an 'answer' key.")

    # Check that grader specified exists
    if not hasattr(graders, grader["type"]):
        raise NameError(f"There is no {grader['type']} grader.")

    # Load answer, if needed
    if "loader" in defaults:
        loader = defaults["loader"]
        l_params = defaults.get("loadingParams", {})  # noQA F841
        # Add Dom's filepath thing
        ans_path = grader["answer"]
        try:
            answer = eval(f"{loader}('{ans_path}', **l_params)")
        except (NameError, TypeError) as e:
            f"There is a problem with your loader: {e}."
    else:
        answer = grader["answer"]

    # Set up args for grader
    grader_dict = {"submission": submission, "answer": answer}
    if "points" in grader:
        grader_dict["points"] = grader["points"]

    # Create grader
    g = eval(f"{defaults['grader']['type']}(**grader_dict)")

    # Execute grading
    if "gradingParams" in defaults:
        params_dict = defaults["gradingParams"]
        try:
            method = params_dict.pop("method")
        except KeyError:
            raise KeyError(
                "The 'gradingParams' in the definition for this task "
                "is missing a 'method'."
            )
    else:
        params_dict = {}

    eval(f"g.{method}(**params_dict)")

    return g.return_feedback(**defaults.get("feedbackParams", {}))
