#!/bin/sh

set -e

rpmbuild --define "_srcrpmdir $(pwd)" --define "_sourcedir $(pwd)" --nodeps -bs alteeve-el8-repo.spec
