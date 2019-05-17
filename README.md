# incquery-server-jupyter
IncQuery Server Client Extensions for Jupyter and Python

Requires [IncQuery Server](https://incquery.io) to operate.


## Getting started with the proof-of-concept Jupyter client

1. Make sure Python 3.7+ is installed, along with the `pip` package manager 
1. Make sure Jupyter is installed: 
```pip install jupyter```
See details at: [jupyter.org](https://jupyter.org/install)
1. Obtain a current version of IncQuery Server and locate the the `iqs4twc.yaml` API specification file using ONE of the following methods:
 a. If you have access to the IQS source code, find the specification at `${path-to-iqs-git}/web-api-twc/src/main/resources/webroot/iqs4twc.yaml`
 b. If you have access to a running IQS instance, visit the Swagger API browser (probably at `${iqs-web-address}/swagger`) and find the link to `iqs4twc.yaml` in small print directly under the main heading `IncQuery Server`.
1. Generate and install a Python-based OpenAPI client for your version of IQS by performing the following steps:
 a. Get a current version of the OpenAPI Generator, e.g. by simply downloading [openapi-generator-cli-3.3.4.jar](http://central.maven.org/maven2/org/openapitools/openapi-generator-cli/3.3.4/openapi-generator-cli-3.3.4.jar); for further options, see [here](https://openapi-generator.tech/docs/installation)
 b. Execute the following command to generate python sources into a target directory:
```java -jar ${path-to-openapi-generator-cli-3.3.4.jar} generate -i ${path-to-iqs4twc.yaml} -l python -o ${path-to-python-client-package-folder} -DpackageName=iqs_client -DprojectName=iqs-twc-api  > ${path-to-logfile} ```
 c. Install the generated Python package as an _editable_ pip package, so that if you fetch a new version and regenerate it, then changes will be correctly reflected:
```pip install -e ${path-to-python-client-package-folder}```
1. Designate a location as the notebook home, where notebook files will be stored. If different from `${this-git-repo}/example-notebook-home`, please manually copy over the non-generated Jupyter-specific components, which are currently not installable yet.  These components are currently located in a single file `${this-git-repo}/example-notebook-home/iqs_jupyter.py`, but this might change.
1. Start a Jupyter server from `${path-to-notebook-home}`: 
```jupyter notebook```
1. Interact with Jupyter either via the newly opened browser window, or using the URL or token printed by the Jupyter server to its stdout. Create a new notebook or open an existing one within the notebook folder; see an example in `${this-git-repo}/example-notebook-home/iqs-demo-twc.ipynb` (if the parent folder is designated as notebook home, you should already see this notebook as a starting point).
1. Within the notebook, get started by:
 a. Import the Jupyter-specific client library (the accompanying `.py` file) 
 ```import iqs_jupyter```
 b. Create a widget to specify an access point
 ```connector = iqs_jupyter.IQSConnectorWidget()``` 
 c. Fill out the text field of the widget to specify the address to a running IQS server instance. It is possible to specify the initial content of the address field using the optional parameter `defaultValue='127.0.0.1:47700/api'`. If such a default value is given, it is possible to skip this step by not displaying the widget at all (pass `auto_display=False`).
 d. Create the main client object `iqs`:
 ```iqs = connector.connect()``` 
 e. Browse for a TWC revision using 
 ```revision_selector = iqs.jupyter_tools.revision_selector_widget()```
 f. Access the full JSON/RPC API of IQS in the form of (you may use TAB completion):
 ```iqs.${api-category-label}.${api-call}```