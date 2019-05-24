# incquery-server-jupyter
IncQuery Server Client Extensions for Jupyter and Python

Requires [IncQuery Server](https://incquery.io) to operate.


## Getting started with the proof-of-concept Jupyter client, using conda

1. Make sure Miniconda3/Anaconda is installed, along with Python 3.7+ and the `conda` package manager 
1. Make sure Jupyter is installed: 

        conda install jupyter
See details at: [jupyter.org](https://jupyter.org/install)
1. Generate and install a Python-based OpenAPI client for your version of IQS by performing the following steps:
   1. Obtain a current version of IncQuery Server and locate the the `iqs4twc.yaml` API specification file using ONE of the following methods:
      * If you have access to the IQS source code, find the specification at `${path-to-iqs-git}/web-api-twc/src/main/resources/webroot/iqs4twc.yaml`
      * If you have access to a running IQS instance, visit the Swagger API browser (probably at `${iqs-web-address}/swagger`) and find the link to `iqs4twc.yaml` in small print directly under the main heading `IncQuery Server`.
   1. Get a current version of the OpenAPI Generator, e.g. by simply downloading [openapi-generator-cli-3.3.4.jar](http://central.maven.org/maven2/org/openapitools/openapi-generator-cli/3.3.4/openapi-generator-cli-3.3.4.jar); for further options, see [here](https://openapi-generator.tech/docs/installation)
   1. Execute the following command to generate python sources into a target directory:

            java -jar ${path-to-openapi-generator-cli-3.3.4.jar} generate -i ${path-to-iqs4twc.yaml} -l python -o ${this-git-repo}/python-client-iqs -DpackageName=iqs_client -DprojectName=iqs-twc-api  > ${path-to-logfile}

   1. (In the Anaconda console environment) build a conda package from the generated sources, then install it:

            conda build ${this-git-repo}/releng/iqs-jupyter-packaging/conda/iqs-twc-api
            conda install --use-local iqs-twc-api

1. Designate a location as the notebook home, where notebook files will be stored. 
1. Ensure that the non-generated Jupyter-specific client extensions are available to notebooks by executing ONE of the following options: 
   * For end users: (in the Anaconda console environment) build a conda package from the client extensions sources, then install it:

            conda build ${this-git-repo}/releng/iqs-jupyter-packaging/conda/iqs-jupyter
            conda install --use-local iqs-jupyter

   * For developers: issue the following command to perform a "developer" install; changes to the source will be reflected immediately to newly (re)started Python interpreters / Jupyter kernels (previously started kernels that already executed the `import` will keep the old content until restarted).

            conda develop ${this-git-repo}/source/iqs-jupyter-extensions/src

1. (in the Anaconda console environment) start a Jupyter server from `${path-to-notebook-home}`: 
```jupyter notebook```
1. Interact with Jupyter either via the newly opened browser window, or using the URL or token printed by the Jupyter server to its stdout. Create a new notebook or open an existing one within the notebook folder; see an example in `${this-git-repo}/example-notebook-home/iqs-demo-twc.ipynb` (if the parent folder is designated as notebook home, you should already see this notebook as a starting point).
1. Within the notebook, get started by:
   1. Import the Jupyter-specific client library

            import iqs_jupyter

   1. Create a widget to specify an access point

            connector = iqs_jupyter.IQSConnectorWidget()

   1. Fill out the text field of the widget to specify the address to a running IQS server instance. It is possible to specify the initial content of the address field using the optional parameter `defaultValue='127.0.0.1:47700/api'`. If such a default value is given, it is possible to skip this step by not displaying the widget at all (pass `auto_display=False`).
   1. Create the main client object `iqs`:
 
            iqs = connector.connect()
 
   1. Browse for a TWC revision using 
   
            revision_selector = iqs.jupyter_tools.revision_selector_widget()
   
   1. Access the full JSON/RPC API of IQS in the form of (you may use TAB completion):
   
            iqs.${api-category-label}.${api-call}
  
## Getting started without Anaconda/Miniconda, for `pip` users

The above instructions mostly apply here as well. However, instead of issuing `conda build` and `conda install` on the conda recipe directories, run instead 

    pip install ${this-git-repo}/python-client-iqs

and then 

    pip install ${this-git-repo}/source/iqs-jupyter-extensions/src

Specifying `install -e` will install these pip packages in "editable" mode, similarly to `conda develop`.
  
  
## Demo notes

The demo notebook uses `ploty` and `cufflinks` to demonstrate possible applications of the client extensions package. It is not recommended to install `cufflinks-py` using conda, as conda-forge seems to host an obsolete version not compatible with the demo; simply issue `pip install cufflinks` from the Anaconda console instead. 


