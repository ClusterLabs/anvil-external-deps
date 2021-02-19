#!/bin/sh

set -e

rm -f *.tar.gz
wget $(spectool -S perl-Log-Journald.spec | grep ^S | awk '{print $NF}')
rpmbuild --define "_srcrpmdir $(pwd)" --nodeps -bs perl-Log-Journald.spec
rm -f *.tar.gz
