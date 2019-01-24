#!/bin/bash

tmpdir=$(mktemp -d)
trap "popd; rm -rf $tmpdir; exit" INT TERM EXIT
pushd $tmpdir
curl -c tmpcookie -d user_name=$1 -d password=$2 -d login=1 http://localhost/bkr/login || exit 1

curl -H "Accept: application/json" -H "Content-Type: application/json" -b tmpcookie -d "{\"name\":\"$3\"}" http://localhost/bkr/powertypes/

popd
rm -rf $tmpdir
trap - INT TERM EXIT

