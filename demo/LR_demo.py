#!/usr/bin/env python
# Backward-compatible launcher.

import os
import runpy

if __name__ == '__main__':
    target = os.path.join(os.path.dirname(__file__), 'project_logreg_baseline.py')
    runpy.run_path(target, run_name='__main__')
