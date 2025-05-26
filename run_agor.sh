#!/bin/bash
cd /mnt/persist/workspace
PYTHONPATH=/mnt/persist/workspace/src python -c "from agor.main import app; app()" "$@"
