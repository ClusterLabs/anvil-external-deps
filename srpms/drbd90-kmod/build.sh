#!/bin/sh

set -e

rm -f *.tar.gz
# spectool on centos doesn´t like our spec file (works on fedora)
wget https://www.linbit.com/downloads/drbd/9.0/drbd-9.0.27-1.tar.gz
rpmbuild --define "_srcrpmdir $(pwd)" --define "_sourcedir $(pwd)" --nodeps -bs drbd90-kmod.spec
rm -f *.tar.gz
