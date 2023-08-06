# ebranch

Tool for branching Fedora packages for EPEL

```
$ ebranch
Usage: ebranch [OPTIONS] COMMAND [ARGS]...
Options:
--help Show this message and exit.
Commands:
build-reqs lists build requirements for a package
is-branched checks if a package is branched
iterate-report computes missing BRs for new top-level packages
ls-branches lists branches for a package
missing-build-reqs lists missing build requirements to build for a branch
unfold-report adds new missing BRs to the top-level list
```

## Presentation
Presented at [CentOS Dojo FOSDEM
2022](https://wiki.centos.org/Events/Dojo/FOSDEM2022#Bootstrapping)
([slides](https://salimma.fedorapeople.org/slides/2022/centos_dojo-202202-epel_branching_with_ebranch.pdf),
[video](https://www.youtube.com/watch?v=VjPZmq_h2Rk)).

## Installation
[![Copr build status](https://copr.fedorainfracloud.org/coprs/salimma/ebranch/package/python-ebranch/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/salimma/ebranch/package/python-ebranch/)

This tool is still in active development, so for the time being it is not
packaged in Fedora proper. This will happen once the commands and data
structures are reasonably stable.

You can install on Fedora 35, CentOS Stream 9 (with EPEL enabled), and Rawhide using:

``` bash
sudo dnf copr enable salimma/ebranch
sudo dnf install ebranch
```

## Local development
``` bash
python -m venv .venv-dev
source .venv-dev/bin/activate
pip install --upgrade pip
pip install -q build
make dist install
make install
```

