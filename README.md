# Python and Jupyter Client Extensions for the IncQuery Server
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IncQueryLabs/incquery-server-jupyter/master?filepath=example-notebook-home%2Fiqs-demo-mms.ipynb)

Requires [IncQuery Server (IQS)](https://incquery.io) to operate.


## Try it first

Click the __binder__ shield above to spin up a deployment publicly hosted on [MyBinder](https://mybinder.org/), with wired-in guest access to [a public IQS demo instance](https://openmbee.incquery.io) and [the OpenMBEE public MMS model repository](https://mms.openmbee.org/).


## Getting started 

### Using Conda

1. Make sure Miniconda3/Anaconda is installed, along with Python 3.7+ and the `conda` package manager 
1. Make sure Jupyter is installed: 

        conda install jupyter
See details at: [jupyter.org](https://jupyter.org/install)
1. Obtain the Python client library in one of the following ways:
   * download a released version from https://github.com/IncQueryLabs/incquery-server-jupyter/releases, then extract contents into `${this-git-repo}/releng/source-gen`
   * OR generate and install a Python-based OpenAPI client for your version of IQS by performing the following steps:
   1. Obtain a current version of IncQuery Server and locate the the `iqs4twc.yaml` API specification file using ONE of the following methods:
      * If you have access to the IQS source code, find the specification at `${path-to-iqs-git}/web-api-twc/src/main/resources/webroot/iqs4twc.yaml`
      * If you have access to a running IQS instance, visit the Swagger API browser (probably at `${iqs-web-address}/swagger`) and find the link to `iqs4twc.yaml` in small print directly under the main heading `IncQuery Server`.
   1. Get a current version of the OpenAPI Generator, e.g. by simply downloading [openapi-generator-cli-3.3.4.jar](http://central.maven.org/maven2/org/openapitools/openapi-generator-cli/3.3.4/openapi-generator-cli-3.3.4.jar); for further options, see [here](https://openapi-generator.tech/docs/installation)
   1. Execute the following command to generate python sources into a target directory:

            java -jar ${path-to-openapi-generator-cli-3.3.4.jar} generate -i ${path-to-iqs4twc.yaml} -l python -o ${this-git-repo}/source-gen/incqueryserver-api-python-client -DpackageVersion="0.10.0" -DpackageUrl="https://incquery.io" -DpackageName=iqs_client -DprojectName=incqueryserver-api-python-client  > ${path-to-logfile}

1. (In the Anaconda console environment) build a conda package from the downloaded or generated sources, then install it (or alternatively use `conda develop`, see later):

            conda build ${this-git-repo}/releng/iqs-jupyter-packaging/conda/incqueryserver-api-python-client
            conda install --use-local incqueryserver-api-python-client

1. Designate a location as the notebook home, where notebook files will be stored. For example, use `${this-git-repo}/example-notebook-home`.
1. Ensure that the non-generated Jupyter-specific client extensions are available to notebooks by executing ONE of the following options: 
   * For end users: (in the Anaconda console environment) build a conda package from the client extensions sources, then install it:

            conda build ${this-git-repo}/releng/iqs-jupyter-packaging/conda/incqueryserver-jupyter
            conda install --use-local incqueryserver-jupyter

   * For developers: issue the following command to perform a "developer" install directly from the source project; changes to the source will be reflected immediately to newly (re)started Python interpreters / Jupyter kernels (previously started kernels that already executed the `import` will keep the old content until restarted).

            conda develop ${this-git-repo}/source/incqueryserver-jupyter

### Using `pip`

The above instructions mostly apply here as well. However, instead of issuing `conda build` and `conda install` on the conda recipe directories, run instead 

    pip install ${this-git-repo}/source-gen/incqueryserver-api-python-client

and then 

    pip install ${this-git-repo}/source/incqueryserver-jupyter

Specifying `install -e` will install these pip packages in "editable" mode, similarly to `conda develop`.

### Additional dependencies

The demo notebook uses `ploty` and `cufflinks` to demonstrate possible applications of the client extensions package. It is not recommended to install `cufflinks-py` using conda, as conda-forge seems to host an obsolete version not compatible with the demo; simply issue `pip install cufflinks` from the Anaconda console instead. 

## Running the notebook

### Set up environment variables first
  
Several functions and classes defined in client extension take optional arguments whose default values can be injected via environment variables. This allows the notebook itself to be much simpler, by omitting connection data etc. 

Here is an example `start-jupyter.cmd` file you may wish to place into your notebook home, and use it to start jupyter with the right default values: 

```cmd
@echo off

set IQS_JUPYTER_default_IQS_address=127.0.0.1:47700/api
set IQS_JUPYTER_default_IQS_username=...
set IQS_JUPYTER_default_IQS_password=...

set IQS_JUPYTER_default_twc_workspace=4d6ce495-1273-452c-a548-36fcd922184e
set IQS_JUPYTER_default_twc_resource=34cc77c8-d3ef-40a6-9b91-65786117fe67
set IQS_JUPYTER_default_twc_branch=bd03a239-7836-4d4c-9bcb-eba73b001b1e
set IQS_JUPYTER_default_twc_revision=1

set IQS_JUPYTER_default_mms_org=6384a103-766c-46e0-830d-8a3b1f479479
set IQS_JUPYTER_default_mms_project=PROJECT-bef4f459-5d90-41fb-bc86-4f6d4ebd2dfd
set IQS_JUPYTER_default_mms_ref=master
set IQS_JUPYTER_default_mms_commit=560d3959-3912-434a-a914-8d039d3c9a06

set IQS_JUPYTER_default_twc_osmc_address=https://twc.demo.iqs.beta.incquerylabs.com:8111/osmc
set IQS_JUPYTER_default_twc_osmc_username=...
set IQS_JUPYTER_default_twc_osmc_password=...

jupyter notebook
```
  
Caution: beware of whitespace, make sure there is none before/after the `=`.
A similar shell script can be used in case of *nix systems; a docker file might be another good way to provide environment variables. 

### Run the notebook

1. (in the Anaconda console environment) start a Jupyter server from `${path-to-notebook-home}`: 
```jupyter notebook```
1. Interact with Jupyter either via the newly opened browser window, or using the URL or token printed by the Jupyter server to its stdout. Create a new notebook or open an existing one within the notebook folder; see an example in `${this-git-repo}/example-notebook-home/iqs-demo-twc.ipynb` (if the parent folder is designated as notebook home, you should already see this notebook as a starting point).
1. Within the notebook, get started by:
   1. Import the Jupyter-specific client library

            import iqs_jupyter

   1. Create a widget to specify an access point

            connector = iqs_jupyter.IQSConnectorWidget()

   1. Fill out the text field of the widget to specify the address to a running IQS server instance, then create the main client object `iqs`:

            iqs = connector.connect()
   
      * To skip manual form filling, it is possible to specify the initial content of the widget fields using a number of ways. First, `IQSConnectorWidget` has the optional parameters `initial_address`, `initial_user`, `initial_password`. Second, if such parameters are not given, results may be automatically filled from environment variables (see below). If such default values are known, it is possible to skip this step and the previous one by not displaying a widget at all:
      
                iqs = iqs_jupyter.connect()
       
   1. Browse for a TWC revision using 
   
            revision_selector = iqs.jupyter_tools.twc_revision_selector_widget()
   
   1. Access the full JSON/RPC API of IQS in the form of (you may use TAB completion):
   
            iqs.${api-category-label}.${api-call}
