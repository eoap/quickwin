# Quickwin - Getting started on Earth Observation Application Packaging with CWL

This repository supports "**Getting started on Earth Observation Application Packaging with CWL**" tutorial events, where participants are introduced to the world of Eearth Observation (EO) Application Packages and explore how to effectively package, share, and execute EO workflows using the Common Workflow Language (CWL) standard.

This tutorial event is designed for developers, scientists, and EO enthusiasts who want to get started and increase their skills in creating and sharing EO Application Packages. Whether you are new to CWL or already have some experience, this event will provide valuable insights and practical knowledge to boost your expertise.

With this tutorial, developers will learn:

* The fundamentals of EO Application Packages and their role in the EO domain.
* How to leverage CWL to describe, package, and share workflows.
* Techniques for incorporating data, code, configuration files, and documentation into an EO Application Package.
* Best practices for creating portable and reproducible EO workflows.
* Hands-on exercises to reinforce your understanding and gain practical experience.

When developers package an EO Application, they are in fact packaging their own software, written in a specific programming language, as a containerized application (or a set of containerized applications), to be described as an EO Application Package using the CWL as described in the OGC proposed best practices.

This tutorial will guide developers through step-by-step examples, demonstrating the process of creating EO Application Packages using CWL with a simple EO application for water bodies detection using the Normalised Difference Water Index (NDWI). 

## Implementation

To facilitate this process, developers are guided through the tutorial using interactive Jupyter Notebooks to test the Application Package across various execution scenarios:

1) **Application**: it describes a simple EO application for water bodies detection using the Normalised Difference Water Index (NDWI). The application is written in Python and invoked with `CliRunner` from within the Notebook.
2) **Container**: it creates the container image containing the execution dependencies of the application developed in the previous Notebook, and it executes it in `bash` using `podman`.
3) **CWL-CommandLineTool**: it prepares the CWL *CommandLineTool* document(s) wrapping the command line tool available in container(s).
4) **CWL-Workflow**: it prepares the CWL *Workflow* that orchestrates the *CommandLineTool* document(s) wrapping the command line tool available container(s).

The webpage of the documentation is https://eoap.github.io/quickwin. 

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
## Typed CWL release preparation

The `feature/typed-cwl-release` branch prepares version 2.0.0. Both standalone
CWL documents use CWL v1.2 with published URI schema imports, module-defined bounding-box records and CRS
and band enums. Jobs are in `cwl-cli/params.yaml` and `cwl-workflow/params.yaml`.
The four notebooks process real Sentinel-2 data around Lake Almanor; they build
the locked processing image locally before running the CWL lessons.

Install `requirements-notebooks.txt` with `uv pip sync --require-hashes` using
Python 3.12. Run `python scripts/cwl-docs.py --validate` to validate standalone
contracts and generate Markdown. Run `scripts/run-practice-labs.py` with the
Quickwin workspace and `quickwin_env` kernel, then `scripts/check-results.py`
to verify the generated STAC assets, geographic bounds and binary water masks.
CI repeats all four notebooks from a clean checkout. Stable publication is an
explicit workflow dispatch on main after acceptance; artifacts contain immutable
GHCR image references, matching typed jobs and checksums. No CWL packing is used.

## Processing-package model

The water-detection package under `water-bodies/command-line-tools/detect-water-body`
uses Hatchling, Python 3.12 and hash-locked runtime/development requirements.
Run `hatch run dev:check` and `hatch run test:test` from that directory. Its
Rocky Linux 10.1 builder produces a wheel; its separate runtime runs as `neo`
(UID/GID 2000), checks dependencies and CLI startup, and removes venv pip.
Both `detect-water-body` and the existing `python -m app` entrypoint are installed.
The application and container lessons use the same package implementation, and
release CI requires these quality gates before real-data notebook acceptance.
