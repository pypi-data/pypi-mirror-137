..
    This file is part of Invenio.
    Copyright (C) 2015-2020 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version 1.2.4 (released 2022-02-02)

- Changed version bounds on Celery to 5.1-5.3.

Version 1.2.3 (released 2021-10-18)

- Changed version bounds on Celery to 5.1-5.2 (v4.x has reached end of life
  August 2021), and there's no new LTS release yet.

Version 1.2.2 (released 2020-12-09)

- Removes the pytest-celery dependency as the package is still in prerelease
  and it only affects tests. If you are using Celery 5 you may need to enable
  the pytest celery plugin - see
  https://docs.celeryproject.org/en/stable/userguide/testing.html#enabling

Version 1.2.1 (released 2020-09-28)

- Change version bounds on Celery to 4.4 to 5.1.

- Adds dependency on pytest-celery which now installs the celery_config pytest
  fixture.

Version 1.2.0 (released 2020-03-05)

- added dependency on invenio-base to centralise package management

Version 1.1.3 (released 2020-02-21)

- Removed redundant version specifier for Celery dependency.

Version 1.1.2 (released 2020-02-17)

- Unpinned Celery version to allow support of Celery 4.4

Version 1.1.1 (released 2019-11-19)

- pinned version of celery lower than 4.3 due to Datetime serialization
  issues

Version 1.1.0 (released 2019-06-21)

- Changed the ``msgpack-python`` dependency to ``msgpack``.
  Please first uninstall ``msgpack-python`` before installing
  the new ``msgpack`` dependency (``pip uninstall msgpack-python``).


Version 1.0.1 (released 2018-12-06)

- Adds support for Celery v4.2. Technically this change is backward
  incompatible because it is no longer possible to load tasks from bare modules
  (e.g. mymodule.py in the Python root). This is a constraint imposed by Celery
  v4.2. We however do not known of any cases where bare modules have been used,
  and also this design is discouraged so we are not flagging it as a backward
  incompatible change, in order to have the change readily available for
  current Invenio version.

Version 1.0.0 (released 2018-03-23)

- Initial public release.
