#!/bin/bash

VERSION_JSON="docs/versions.json"
LAYOUT_FILE="sphinx_zama_theme/layout.html"
VERSION_FILE="sphinx_zama_theme/__init__.py"

CURTAG=`git describe --abbrev=0 --tags`;
CURTAG="${CURTAG/v/}"

IFS='.' read -a vers <<< "$CURTAG"

MAJ=${vers[0]}
MIN=${vers[1]}
BUG=${vers[2]}
echo "Current Tag: v$MAJ.$MIN.$BUG"

for cmd in "$@"
do
	case $cmd in
		"--major")
			# $((MAJ+1))
			((MAJ+=1))
			MIN=0
			BUG=0
			echo "Incrementing Major Version#"
			;;
		"--minor")
			((MIN+=1))
			BUG=0
			echo "Incrementing Minor Version#"
			;;
		"--bug")
			((BUG+=1))
			echo "Incrementing Bug Version#"
			;;
	esac
done
NEWTAG="v$MAJ.$MIN.$BUG"
echo "Adding Tag: $NEWTAG";

sed -i "" "s/theme v[[:digit:]]*\.[[:digit:]]*\.[[:digit:]]*/theme ${NEWTAG//./\\.}/" $LAYOUT_FILE
sed -i "" "s/__version__ = \"v[[:digit:]]*\.[[:digit:]]*\.[[:digit:]]*\"/__version__ = \"${NEWTAG//./\\.}\"/" $VERSION_FILE
cat $VERSION_JSON| jq ".menu += [\"$NEWTAG\"]" | jq ".all+=[\"$NEWTAG\"]" | jq ".latest = \"$NEWTAG\"" > $VERSION_JSON.tmp
mv $VERSION_JSON.tmp $VERSION_JSON
git add $VERSION_JSON $LAYOUT_FILE $VERSION_FILE
git commit -m "chore: release $NEWTAG"
git tag -a $NEWTAG -m $NEWTAG
