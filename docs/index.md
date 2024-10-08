# Getting started on Earth Observation Application Packaging with CWL

This guide supports "Getting started on Earth Observation Application Packaging with CWL" tutorial events, where participants are introduced to the world of Earth Observation (EO) Application Packages and explore how to effectively package, share, and execute EO workflows using the Common Workflow Language (CWL) standard.

This tutorial event is designed for developers, scientists, and EO enthusiasts who want to get started and increase their skills in creating and sharing EO Application Packages. 

Whether you are new to CWL or already have some experience, this event will provide valuable insights and practical knowledge to boost your expertise.

During the event, you will learn:

* The fundamentals of EO Application Packages and their role in the EO domain.
* How to leverage CWL to describe, package, and share workflows.
* Techniques for incorporating data, code, configuration files, and documentation into an EO Application Package.
* Best practices for creating portable and reproducible EO workflows.
* Hands-on exercises to reinforce your understanding and gain practical experience.

When developers package an EO Application, they are in fact packaging their own software, written in a specific programming language, as a containerized application (or a set of containerized applications), to be described as an EO Application Package using the Common Workflow Language as described in the OGC proposed best practices.

To achieve this, developers follow the steps described below.

* Prepare one or more container images containing the execution dependencies of the software.
* Prepare the CWL *CommandLineTool* document(s) wrapping the command line tool available in container(s).
* Prepare the CWL *Workflow* orchestrating CWL *CommandLineTool* document(s) wrapping the command line tool available container(s).
* Test the application package in one or more execution scenarios.

This tutorial will guide you through step-by-step tutorials, demonstrating the process of creating EO Application Packages using CWL with a simple EO application for water bodies detection using the Normalised Difference Water Index (NDWI). 