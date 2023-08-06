Dagster Faculty
===============
Python library for using Dagster in Faculty platform.

**Release Steps**

1. To test pypi after applying your changes, run ``release-testpypi`` job from the Gitlab CI pipeline

    Note that if you get the error `File already exists` in the Pipeline, this is likely because of
    the `use_scm_version.local_scheme` value in `setup.py`. We believe this will be suitably rare
    enough to not need a workaround at present.

2. Verify the new test release version on https://test.pypi.org/project/dagster-faculty/

3. Once you have verified the test release, create an annotated tag on master, and then push it.

    ``git tag -a <version>``

    ``git push origin --tags``

4. Verify the new production release version on https://pypi.org/project/dagster-faculty/
