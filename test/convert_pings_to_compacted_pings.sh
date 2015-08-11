#!/bin/bash

BASE=./test
LIST=$BASE/inputs.txt
WORK=$BASE/work
OUT=$BASE/out
SCHEMA=./telemetry/telemetry_schema.json
SOURCE=$BASE/sample_data.log

cd ..
cp $SOURCE $WORK/a.log
# we don't clean up in dry-run mode, so we should still wipe the output dir.
if [ -d $OUT ]; then
    echo "Cleaning up '$OUT'..."
    rm -rfv $OUT
    mkdir $OUT
    echo "Done."
fi
time python -u -m process_incoming.process_incoming_standalone \
    --dry-run --config "$BASE/telemetry_aws.dev.json" \
    --input-files "$LIST" --bad-data-log "$BASE/bad_records.txt" \
    -w "$WORK" -o "$OUT" -t "$SCHEMA" \
    -s "$BASE/stats_log.txt" | tee "$BASE/run_convert.$(date +%Y%m%d%H%M%S).log"
