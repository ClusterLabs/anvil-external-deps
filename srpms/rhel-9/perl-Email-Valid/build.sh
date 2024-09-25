#!/bin/sh

set -e

rm -f *.tar.gz
wget $(spectool --define "_srcrpmdir $(pwd)" --define "_sourcedir $(pwd)" -S perl-Email-Valid.spec | grep "^Source0:" | awk '{print $NF}')
rpmbuild --define "_srcrpmdir $(pwd)" --define "_sourcedir $(pwd)" --nodeps -bs perl-Email-Valid.spec
rm -f *.tar.gz
