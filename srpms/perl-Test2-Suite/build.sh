#!/bin/sh

set -e

rm -f *.tar.gz
wget $(spectool --define "_srcrpmdir $(pwd)" --define "_sourcedir $(pwd)" -S perl-Test2-Suite.spec | grep "^Source0:" | awk '{print $NF}')
rpmbuild --define "_srcrpmdir $(pwd)" --define "_sourcedir $(pwd)" --nodeps -bs perl-Test2-Suite.spec
rm -f *.tar.gz