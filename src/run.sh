#/bin/sh

# This script is used to run the entire project
pushd init_db > /dev/null
python3 datalake_gen.py
./init_db.sh --clean
./init_db.sh
popd > /dev/null
pushd populate_db > /dev/null
python3 populate_db.py
popd > /dev/null