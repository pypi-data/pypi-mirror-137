# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['Checkpointing',
 'Checkpointing.ChkptDescFileGen',
 'Checkpointing.DumpHTIF',
 'CpuTraceAnalysis',
 'CpuTraceAnalysis.libcputrace',
 'CpuTraceAnalysis.libcputrace.MachineCode',
 'CpuTraceAnalysis.libcputrace.StackAnalysis',
 'CpuTraceAnalysis.libcputrace.StackAnalysis.Recorder',
 'CpuTraceAnalysis.libcputrace.Trace',
 'SimEnvControl',
 'SimEnvControl.libsimenv',
 'SimEnvControl.libsimenv.makefile_generator',
 'SpecResultVerification',
 'SyscallAnalysis',
 'SyscallAnalysis.libsyscall',
 'SyscallAnalysis.libsyscall.analyzer',
 'SyscallAnalysis.libsyscall.syscalls',
 'SyscallAnalysis.test',
 'TetherSim']

package_data = \
{'': ['*'],
 'CpuTraceAnalysis': ['trace_vis/*',
                      'trace_vis/node_modules/vis-timeline/*',
                      'trace_vis/node_modules/vis-timeline/declarations/*',
                      'trace_vis/node_modules/vis-timeline/dist/*',
                      'trace_vis/node_modules/vis-timeline/dist/types/*',
                      'trace_vis/node_modules/vis-timeline/esnext/*',
                      'trace_vis/node_modules/vis-timeline/esnext/esm/*',
                      'trace_vis/node_modules/vis-timeline/esnext/umd/*',
                      'trace_vis/node_modules/vis-timeline/peer/*',
                      'trace_vis/node_modules/vis-timeline/peer/esm/*',
                      'trace_vis/node_modules/vis-timeline/peer/umd/*',
                      'trace_vis/node_modules/vis-timeline/standalone/*',
                      'trace_vis/node_modules/vis-timeline/standalone/esm/*',
                      'trace_vis/node_modules/vis-timeline/standalone/umd/*',
                      'trace_vis/node_modules/vis-timeline/styles/*',
                      'trace_vis/node_modules/vis-timeline/types/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'bashlex>=0.15,<0.16',
 'click>=7.1.2,<8.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'pyparsing>=2.4.7,<3.0.0',
 'python-Levenshtein>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['atool-app-repo = SimEnvControl.app_repo_cli:cli',
                     'atool-simenv = SimEnvControl.sim_env_cli:cli',
                     'atool_SimTetheringController = '
                     'TetherSim.SimTetheringController:main',
                     'atool_chkpt_htif_dump = '
                     'Checkpointing.DumpHTIF.chkpt_htif_dump:main',
                     'atool_smpt2ckptdesc = '
                     'Checkpointing.ChkptDescFileGen.smpt2ckptdesc:main',
                     'atool_spike_trim = '
                     'SpecResultVerification.spike_trim:main',
                     'atool_trace2google = CpuTraceAnalysis.trace2google:main',
                     'atool_trace2tracevis = '
                     'CpuTraceAnalysis.trace2tracevis:main',
                     'atool_trace_diff = CpuTraceAnalysis.trace_diff:main']}

setup_kwargs = {
    'name': 'anycore-dbg-supplement',
    'version': '0.6.0',
    'description': 'A bundle of auxiliary scripts for the Anycore project',
    'long_description': '## SimEnv\nA new toolset to reliably packing, and spawning a RISC-V workload (app) for any simulation purpose.\n\nAn app is packed into a `simenv`, which is basically the rootfs containing all the essentials for a simulation. The tool learns what are the essentials by analyzing the workload\'s syscall trace. When simulating with the proper PK/FESVR, the dynamic instruction stream is even reproducible.  \n\nThe motivation is to help Dr. Rotenberg\'s microarchitecture research group and ECE721 students using SPEC CPU2006 and CPU2017 workloads (usually checkpointed workloads) with ease.\n\nRun `atool-app-repo --help` to learn how to create a workload repository, and `atool-simenv --help` to learn how to use a workload repository.\n\n```\n$ atool-app-repo --help\nUsage: atool-app-repo [OPTIONS] COMMAND [ARGS]...\n\n  The app repository management utility\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  addckpt     Import a checkpoint.\n  addsysroot  Import a pristine sysroot.\n  init        Create an empty app repository.\n  learn       Analyze an app for how to create SimEnv.\n  subrepo     Spawn a sub-repository with the selected apps.\n```\n\n```\n$ atool-simenv --help\nUsage: atool-simenv [OPTIONS] COMMAND [ARGS]...\n\n  The simenv utility\n\nOptions:\n  --repo-path DIRECTORY  Override the SimEnv repository path given by the\n                         environmental variable "ATOOL_SIMENV_REPO_PATH".\n\n  --help                 Show this message and exit.\n\nCommands:\n  list    List available apps and checkpoints in the SimEnv repository.\n  mkgen   Generate a Makefile for a simenv, at current dir.\n  spawn   Spawn a simenv.\n  verify  Perform integrity checking for a simenv.\n```\n\n\\* If you are using bash/zsh/fish, you can:\n- run `eval "$(_ATOOL_SIMENV_COMPLETE=source_$(basename $SHELL) atool-simenv)"` to enable the auto completion for atool-simenv.\n- run `eval "$(_ATOOL_APP_REPO_COMPLETE=source_$(basename $SHELL) atool-app-repo)"` to enable the auto completion for atool-app-repo.\n\n## Misc.\n\n- `SpecResultVerification/spike_trim.py` - Trim out the extra header/tail message produced by spike or pk during the simulation. Useful if you want to automatically verify the STDOUT output of a SPEC simulation.\n- `Checkpointing/ChkptDescFileGen/smpt2ckptdesc.py` - Convert the Simpoint output file to the checkpoint job description file accepted by Spike.\n- `Checkpointing/DumpHTIF/chkpt_htif_dump.py` - Show the HTIF syscalls recorded in a checkpoint file. When restoring a checkpoint, those syscalls will be executed in sequence to bring back the state of [HTIF FESVR](https://github.com/s117/riscv-fesvr).\n- `TetherSim/SimTetheringController.py` - Controller for [721sims](https://github.ncsu.edu/jli95/721sim/tree/trace_support) working in tethering mode.\n\n\n## To work with trace dump\n\n- `CpuTraceAnalysis/trace2google.py` - Analyze the trace dumped by [spike](https://github.com/s117/riscv-isa-sim/tree/WIB_trace_support) or [721sim](https://github.ncsu.edu/jli95/721sim/tree/trace_support) and output the result in Google\'s Trace Event Format.\n- To visualize the result, use [speedscope](https://github.com/jlfwong/speedscope) (recommend) or Chromium\'s *about://tracing* .\n  - if `ignore_symbol.yaml` exists in CWD, it will be read to filter out the defined function calls. See `CpuTraceAnalysis/ignore_symbol.yaml` for an example.\n\n- `CpuTraceAnalysis/trace2tracevis.py` - Analyze and visualize the trace dumped by [spike](https://github.com/s117/riscv-isa-sim/tree/WIB_trace_support) or [721sim](https://github.ncsu.edu/jli95/721sim/tree/trace_support) in a homebrew timeline frontend (using [timeline-js](https://github.com/visjs/vis-timeline)).\n  - if `ignore_symbol.yaml` exists in CWD - Will be read to filter out the defined function calls. See `CpuTraceAnalysis/ignore_symbol.yaml` for an example.\n  - **It\'s recommended to use `trace2google.py`.** Because the trace_vis frontend uses timeline-js, which is not intended for visualizing tracing result, it can be very slow and unresponsive when working with trace with a large amount of event.\n\n![image-20201105011703029](https://raw.githubusercontent.com/s117/anycore-dbg-supplement/master/README.assets/image-20201105011703029.png)\n\n<p align=center>Viewing the trace2google.py output with speedscope</p>\n\n![image-20201105011839379](https://raw.githubusercontent.com/s117/anycore-dbg-supplement/master/README.assets/image-20201105011839379.png)\n\n<p align=center>Viewing the trace2google.py output with Chrome\'s about:tracing</p>\n\n![image-20200813043919822](https://raw.githubusercontent.com/s117/anycore-dbg-supplement/master/README.assets/image-20200813043919822.png)\n\n<p align=center>Viewing the trace using homebrew TraceVis frontend (use timeline-js)</p>\n\n**WIP**.',
    'author': 'Jiayang Li',
    'author_email': 'jli95@ncsu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/s117/anycore-dbg-supplement.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
