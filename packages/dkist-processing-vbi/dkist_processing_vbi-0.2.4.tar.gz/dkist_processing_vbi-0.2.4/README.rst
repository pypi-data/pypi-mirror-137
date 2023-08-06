dkist-processing-vbi
====================

Overview
--------
The dkist-processing-vbi library contains the implementation of the vbi pipelines as a collection of the
`dkist-processing-core <https://pypi.org/project/dkist-processing-core/>`_ framework and
`dkist-processing-common <https://pypi.org/project/dkist-processing-common/>`_ Tasks.

The recommended project structure is to separate tasks and workflows into seperate packages.  Having the workflows
in their own package facilitates using the build_utils to test the integrity of those workflows in the unit test.
`example <https://bitbucket.org/dkistdc/dkist-processing-test/src/master/dkist_processing_test/workflows/>`_

Build
-----
Artifacts are built through `bitbucket pipelines <bitbucket-pipelines.yml>`_

The pipeline can be used in other repos with a modification of the package and artifact locations
to use the names relevant to the target repo.

e.g. dkist-processing-test -> dkist-processing-vbi and dkist_processing_test -> dkist_processing_vbi

Deployment
----------
Deployment is done with `turtlebot <https://bitbucket.org/dkistdc/turtlebot/src/master/>`_ and follows
the process detailed in `dkist-processing-core <https://pypi.org/project/dkist-processing-core/>`_

Environment Variables
---------------------
Only those specified by `dkist-processing-core <https://pypi.org/project/dkist-processing-core/>`_ and `dkist-processing-common <https://pypi.org/project/dkist-processing-common/>`_.

Development
-----------
.. code-block:: bash

    git clone git@bitbucket.org:dkistdc/dkist-processing-vbi.git
    cd dkist-processing-vbi
    pre-commit install
    pip install -e .[test]
    pytest -v --cov dkist_processing_vbi
