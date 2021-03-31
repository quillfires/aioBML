## Contributing to aioBML

First off, thanks for taking the time to contribute. It makes the library substantially better. :+1:

The following is a set of guidelines for contributing to the repository. These are guidelines, not hard rules.

## This is too much to read! I want to ask a question!

Generally speaking questions are better suited in our resources below.

- The [discord server](https://discord.gg/fm4HNF6Ted)

Please try your best not to ask questions in our issue tracker. Most of them don't belong there unless they provide value to a larger audience.

## We Develop with Github
We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.
If you are proposing new features, please discuss them with us in the [discord server](https://discord.gg/fm4HNF6Ted) before you start working on them!

## We Use [Git Flow](https://atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
![Simple Image Of A Git Flow Workflow](https://nvie.com/img/hotfix-branches@2x.png)  
When contributing to this project, please make sure you follow this and name your branches appropriately! 

## All Code Changes Happen Through Pull Requests
Make sure you know how Git Flow works before contributing! 
Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `master` or `development` according to Git Flow.
2. Update the CHANGELOG.
3. If you've made a breaking change, mark changelog as "BREAKING".
4. Make sure your code passes the lint checks.
5. Create Issues and pull requests!

## Any contributions you make will be under the MIT License
In short, when you submit code changes, your submissions are understood to be under the same [MIT License](https://github.com/quillfires/aioBML/blob/main/LICENSE) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using [Github Issues](https://github.com/quillfires/aioBML/issues)
We use GitHub issues to track public bugs. Report a bug by [opening a new Issue](https://github.com/quillfires/aioBML/issues/new); it's that easy!
Please be aware of the following things when filing bug reports.

1. Don't open duplicate issues. Please search your issue to see if it has been asked already. Duplicate issues will be closed.
2. When filing a bug about exceptions or tracebacks, please include the *complete* traceback. Without the complete traceback the issue might be **unsolvable** and you will be asked to provide more information.
3. Make sure to provide enough information to make the issue workable. The issue template will generally walk you through the process but they are enumerated here as well:
    - A **summary** of your bug report. This is generally a quick sentence or two to describe the issue in human terms.
    - Guidance on **how to reproduce the issue**. Ideally, this should have a small code sample that allows us to run and see the issue for ourselves to debug. **Please make sure that your username and password is not displayed**. If you cannot provide a code snippet, then let us know what the steps were, how often it happens, etc.
    - Tell us **what you expected to happen**. That way we can meet that expectation.
    - Tell us **what actually happens**. What ends up happening in reality? It's not helpful to say "it fails" or "it doesn't work". Say *how* it failed, do you get an exception? Does it hang? How are the expectations different from reality?
    - Tell us **information about your environment**. What operating system are you running on? What version of aioBML or other libraries are you using alongside? How was it installed? These are valuable questions and information that we use.

If the bug report is missing this information then it'll take us longer to fix the issue. We will probably ask for clarification, and barring that if no response was given then the issue will be closed.

## Submitting a Pull Request

Submitting a pull request is fairly simple, just make sure it focuses on a single aspect and doesn't manage to have scope creep and it's probably good to go. It would be incredibly lovely if the style is consistent to that found in the project.

### Git Commit Guidelines

- Use present tense (e.g. "Add feature" not "Added feature")
- Reference issues or pull requests outside of the first line.
    - Please use the shorthand `#123` and not the full URL.

If you do not meet any of these guidelines, don't fret. Chances are they will be fixed upon rebasing but please do try to meet them to remove some of the workload.
