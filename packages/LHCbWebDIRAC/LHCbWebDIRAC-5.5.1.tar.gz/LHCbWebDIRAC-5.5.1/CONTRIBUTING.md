LHCbWebDIRAC is the LHCb extension of [WebAppDIRAC](https://github.com/DIRACGrid/WebAppDIRAC).

# Repository structure

Due to the fact that we support only the production version, the only branch is _master_, which should be as much as possible a stable branch. Production tags are created starting from this branch.

# Repositories

Developers should have 2 remote repositories (which is the typical GitHub/GitLab workflow):

- _origin_ : cloned from your private fork done on GitLab
- _upstream_ : add it via git remote add upstream and pointing to the blessed repository (https://gitlab.cern.ch/lhcb-dirac/LHCbWebDIRAC.git)

# Code quality

The contributions are subject to reviews.

Pylint is run regularly on the source code. The .pylintrc file defines the expected coding rules and peculiarities (e.g.: tabs consists of 2 spaces instead of 4)

# Testing

ToDo
