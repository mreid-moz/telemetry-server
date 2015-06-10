#!/bin/bash

mkdir -p test-pings test-pings-outputs
rm -f test-pings/*
rm -f test-pings-outputs/*

# find all compressed ping results
for i in `find ./out/ -type f`
do
    cp "$i" test-pings/
done

pushd test-pings/
unxz --keep *.lzma
rm *.lzma # delete the LZMA files separately since unxz occasionally silently fails to, even if we don't use the `--keep` flag
cd  ../test-pings-outputs/
awk 'BEGIN { FS="\t" } { print $2 > $1 }' ../test-pings/*
ls -l | awk '{ print $NF }'
popd
