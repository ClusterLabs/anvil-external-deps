#!/bin/sh

set -e

rm -f *.tar.gz
wget $(spectool --define "_srcrpmdir $(pwd)" --define "_sourcedir $(pwd)" -S libssh2.spec | grep "^Source0:" | awk '{print $NF}')
rpmbuild --define "_srcrpmdir $(pwd)" --define "_sourcedir $(pwd)" --nodeps -bs libssh2.spec
rm -f *.tar.gz
