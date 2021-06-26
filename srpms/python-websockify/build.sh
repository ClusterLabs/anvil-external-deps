#!/bin/sh

set -e

spec_filename="python-websockify.spec"
working_directory="$(pwd)"

rm -f *.tar.gz
spectool --get-files --sources --define "_srcrpmdir $working_directory" --define "_sourcedir $working_directory" "$spec_filename"
rpmbuild --define "_srcrpmdir $working_directory" --define "_sourcedir $working_directory" --nodeps -bs "$spec_filename"
rm -f *.tar.gz

