
### Goal 

Wrap the water bodies detection Python command line tool as a Common Workflow Language `CommandLineTool` and execute it with a CWL runner.

### Lab

This step has a dedicated lab available at `/workspace/quickwin/practice-labs/CommandLineTool.ipynb`

### How to wrap a step as a CWL CommandLineTool 

The CWL document below shows the water bodies detection Python command line tool step wrapped as a CWL CommandLineTool:

```yaml linenums="1" hl_lines="9-12 49-53" title="cwl-cli/detect-water-body"
--8<--
cwl-cli/detect-water-body.cwl
--8<--
```

Let's break down the key components of this CWL document:

* `cwlVersion: v1.2`: Specifies the version of the CWL specification that this document follows.
* `class: CommandLineTool`: Indicates that this CWL document defines a command-line tool.
* `id: detect-water-body`: Provides a unique identifier for this tool, which can be used to reference it in workflows.
* `requirements`: Specifies the requirements and dependencies of the tool. In this case, it defines the following:
    * `InlineJavascriptRequirement`: This requirement allows the use of inline JavaScript expressions in the tool.
    * `EnvVarRequirement`: It sets environment variables. In this case, it sets the `PYTHONPATH` environment variable to "/app."
    * `ResourceRequirement`: Specifies resource requirements for running the tool, including the maximum number of CPU cores and maximum RAM.
    * `DockerRequirement`: This requirement specifies the Docker container to be used. It indicates that the tool should be executed in a Docker container with the image `localhost/detect-water-body:latest`.
* `baseCommand`: Defines the base command to be executed in the container. In this case, it's running a Python module called "app" with the command `python -m app`.
* `arguments`: This section is empty, meaning there are no additional command-line arguments specified here. The tool is expected to receive its arguments via the input parameters.
* `inputs`: Describes the input parameters for the tool, including their types and how they are bound to command-line arguments. The tool expects the following inputs:
    * `item`: A URI record containing the input STAC item URL (image) to be processed, bound to the `--input-item` argument.
    * `aoi`: A BBox record containing west, south, east and north coordinates, bound to the `--aoi` argument.
    * `epsg`: A CRS enum representing the EPSG code for the coordinate system, bound to the `--epsg` argument.
    * `band`: An array of Band enums representing the names of the bands to be extracted, bound to the `--band` argument.
* `outputs`: Specifies the tool's output. It defines an output parameter named `water-body`, which is of type `Directory`. The outputBinding section specifies that the tool is expected to produce one or more files (glob: .) as output.

### Steps

Clean-up the `/workspace/quickwin/runs` folder: 

```
rm -fr /workspace/quickwin/runs/*
```

Run the CWL document using the `cwltool` CWL runner to execute the water bodies detection:


```console hl_lines="9-12 49-53" title="terminal"
--8<--
scripts/cwl-cli.sh
--8<--
```

### Expected outcome

The folder `/workspace/quickwin/runs` contains: 

```
(base) jovyan@jupyter-fbrito--training:~/quickwin$ tree runs
runs
└── poz7ftyy
    ├── S2B_10TFK_20210713_0_L2A
    │   ├── S2B_10TFK_20210713_0_L2A.json
    │   └── otsu.tif
    ├── catalog.json
    └── otsu.tif

2 directories, 4 files
```

### Extra 

The CWL runner `cwltool` allows you to do a YAML file with the parameters:

```yaml title="params.yaml"
--8<--
cwl-cli/params.yaml
--8<--
```

and run it with:

```console hl_lines="5" title="terminal"
export WORKSPACE=/workspace/quickwin

cwltool \
    --podman \
    --outdir ${WORKSPACE}/runs \
    ${WORKSPACE}/cwl-cli/detect-water-body.cwl \
    ${WORKSPACE}/cwl-cli/params.yaml 
```