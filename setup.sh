#!/bin/bash

set -e

sed -i '/[[:print:]]*MPRES[[:print:]]*/d' ~/.bashrc

(
    echo
    echo "export MPRES='$(pwd)/bin'"
    echo 'export PATH="$MPRES:$PATH"'
) >> ~/.bashrc

echo "execute the following command:"
echo "source ~/.bashrc"

exit 0
