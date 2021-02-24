# Python and Jupyter Client Extensions for the IncQuery Server

Requires [IncQuery Server (IQS)](https://incquery.io) to operate.

## PyPI packages

* **API client**: [![PyPI version](https://badge.fury.io/py/incqueryserver-api-python-client.svg)](https://badge.fury.io/py/incqueryserver-api-python-client)
* **Jupyter extensions**: [![PyPI version](https://badge.fury.io/py/incqueryserver-jupyter.svg)](https://badge.fury.io/py/incqueryserver-jupyter)

## Conda packages

<table><tr><td>All platforms:</td>
    <td>
      <a href="https://dev.azure.com/conda-forge/feedstock-builds/_build/latest?definitionId=11971&branchName=master">
        <img src="https://dev.azure.com/conda-forge/feedstock-builds/_apis/build/status/incqueryserver-api-python-client-feedstock?branchName=master">
      </a>
    </td>
  </tr>
</table>

| Name | Downloads | Version | Platforms |
| --- | --- | --- | --- |
| [![Conda Recipe](https://img.shields.io/badge/recipe-incqueryserver--api--python--client-green.svg)](https://anaconda.org/conda-forge/incqueryserver-api-python-client) | [![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/incqueryserver-api-python-client.svg)](https://anaconda.org/conda-forge/incqueryserver-api-python-client) | [![Conda Version](https://img.shields.io/conda/vn/conda-forge/incqueryserver-api-python-client.svg)](https://anaconda.org/conda-forge/incqueryserver-api-python-client) | [![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/incqueryserver-api-python-client.svg)](https://anaconda.org/conda-forge/incqueryserver-api-python-client) |

<table><tr><td>All platforms:</td>
    <td>
      <a href="https://dev.azure.com/conda-forge/feedstock-builds/_build/latest?definitionId=11972&branchName=master">
        <img src="https://dev.azure.com/conda-forge/feedstock-builds/_apis/build/status/incqueryserver-jupyter-feedstock?branchName=master">
      </a>
    </td>
  </tr>
</table>

| Name | Downloads | Version | Platforms |
| --- | --- | --- | --- |
| [![Conda Recipe](https://img.shields.io/badge/recipe-incqueryserver--jupyter-green.svg)](https://anaconda.org/conda-forge/incqueryserver-jupyter) | [![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/incqueryserver-jupyter.svg)](https://anaconda.org/conda-forge/incqueryserver-jupyter) | [![Conda Version](https://img.shields.io/conda/vn/conda-forge/incqueryserver-jupyter.svg)](https://anaconda.org/conda-forge/incqueryserver-jupyter) | [![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/incqueryserver-jupyter.svg)](https://anaconda.org/conda-forge/incqueryserver-jupyter) |


## MyBinder shortcuts

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IncQueryLabs/incquery-server-jupyter/master?filepath=example-notebook-home%2Fiqs-demo-mms.ipynb)
[![Binder (develop branch)](https://img.shields.io/badge/launch-binder%20(develop%20branch)-F5A252.svg?logo=data:image/png;base64,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)](https://mybinder.org/v2/gh/IncQueryLabs/incquery-server-jupyter/develop?filepath=example-notebook-home%2Fiqs-demo-mms.ipynb)

[![Model analysis binder](https://img.shields.io/badge/launch-model%20analysis%20binder-579ACA.svg?logo=data:image/png;base64,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)](https://mybinder.org/v2/gh/IncQueryLabs/incquery-server-jupyter/master?filepath=example-notebook-home%2Fmodel-analysis-demo.ipynb)
[![Model analysis binder (develop branch)](https://img.shields.io/badge/launch-model%20analysis%20binder%20(develop%20branch)-F5A252.svg?logo=data:image/png;base64,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)](https://mybinder.org/v2/gh/IncQueryLabs/incquery-server-jupyter/develop?filepath=example-notebook-home%2Fmodel-analysis-demo.ipynb)

[![Acquisition binder](https://img.shields.io/badge/launch-acquisition%20binder-579ACA.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAABZCAMAAABi1XidAAAB8lBMVEX///9XmsrmZYH1olJXmsr1olJXmsrmZYH1olJXmsr1olJXmsrmZYH1olL1olJXmsr1olJXmsrmZYH1olL1olJXmsrmZYH1olJXmsr1olL1olJXmsrmZYH1olL1olJXmsrmZYH1olL1olL0nFf1olJXmsrmZYH1olJXmsq8dZb1olJXmsrmZYH1olJXmspXmspXmsr1olL1olJXmsrmZYH1olJXmsr1olL1olJXmsrmZYH1olL1olLeaIVXmsrmZYH1olL1olL1olJXmsrmZYH1olLna31Xmsr1olJXmsr1olJXmsrmZYH1olLqoVr1olJXmsr1olJXmsrmZYH1olL1olKkfaPobXvviGabgadXmsqThKuofKHmZ4Dobnr1olJXmsr1olJXmspXmsr1olJXmsrfZ4TuhWn1olL1olJXmsqBi7X1olJXmspZmslbmMhbmsdemsVfl8ZgmsNim8Jpk8F0m7R4m7F5nLB6jbh7jbiDirOEibOGnKaMhq+PnaCVg6qWg6qegKaff6WhnpKofKGtnomxeZy3noG6dZi+n3vCcpPDcpPGn3bLb4/Mb47UbIrVa4rYoGjdaIbeaIXhoWHmZYHobXvpcHjqdHXreHLroVrsfG/uhGnuh2bwj2Hxk17yl1vzmljzm1j0nlX1olL3AJXWAAAAbXRSTlMAEBAQHx8gICAuLjAwMDw9PUBAQEpQUFBXV1hgYGBkcHBwcXl8gICAgoiIkJCQlJicnJ2goKCmqK+wsLC4usDAwMjP0NDQ1NbW3Nzg4ODi5+3v8PDw8/T09PX29vb39/f5+fr7+/z8/Pz9/v7+zczCxgAABC5JREFUeAHN1ul3k0UUBvCb1CTVpmpaitAGSLSpSuKCLWpbTKNJFGlcSMAFF63iUmRccNG6gLbuxkXU66JAUef/9LSpmXnyLr3T5AO/rzl5zj137p136BISy44fKJXuGN/d19PUfYeO67Znqtf2KH33Id1psXoFdW30sPZ1sMvs2D060AHqws4FHeJojLZqnw53cmfvg+XR8mC0OEjuxrXEkX5ydeVJLVIlV0e10PXk5k7dYeHu7Cj1j+49uKg7uLU61tGLw1lq27ugQYlclHC4bgv7VQ+TAyj5Zc/UjsPvs1sd5cWryWObtvWT2EPa4rtnWW3JkpjggEpbOsPr7F7EyNewtpBIslA7p43HCsnwooXTEc3UmPmCNn5lrqTJxy6nRmcavGZVt/3Da2pD5NHvsOHJCrdc1G2r3DITpU7yic7w/7Rxnjc0kt5GC4djiv2Sz3Fb2iEZg41/ddsFDoyuYrIkmFehz0HR2thPgQqMyQYb2OtB0WxsZ3BeG3+wpRb1vzl2UYBog8FfGhttFKjtAclnZYrRo9ryG9uG/FZQU4AEg8ZE9LjGMzTmqKXPLnlWVnIlQQTvxJf8ip7VgjZjyVPrjw1te5otM7RmP7xm+sK2Gv9I8Gi++BRbEkR9EBw8zRUcKxwp73xkaLiqQb+kGduJTNHG72zcW9LoJgqQxpP3/Tj//c3yB0tqzaml05/+orHLksVO+95kX7/7qgJvnjlrfr2Ggsyx0eoy9uPzN5SPd86aXggOsEKW2Prz7du3VID3/tzs/sSRs2w7ovVHKtjrX2pd7ZMlTxAYfBAL9jiDwfLkq55Tm7ifhMlTGPyCAs7RFRhn47JnlcB9RM5T97ASuZXIcVNuUDIndpDbdsfrqsOppeXl5Y+XVKdjFCTh+zGaVuj0d9zy05PPK3QzBamxdwtTCrzyg/2Rvf2EstUjordGwa/kx9mSJLr8mLLtCW8HHGJc2R5hS219IiF6PnTusOqcMl57gm0Z8kanKMAQg0qSyuZfn7zItsbGyO9QlnxY0eCuD1XL2ys/MsrQhltE7Ug0uFOzufJFE2PxBo/YAx8XPPdDwWN0MrDRYIZF0mSMKCNHgaIVFoBbNoLJ7tEQDKxGF0kcLQimojCZopv0OkNOyWCCg9XMVAi7ARJzQdM2QUh0gmBozjc3Skg6dSBRqDGYSUOu66Zg+I2fNZs/M3/f/Grl/XnyF1Gw3VKCez0PN5IUfFLqvgUN4C0qNqYs5YhPL+aVZYDE4IpUk57oSFnJm4FyCqqOE0jhY2SMyLFoo56zyo6becOS5UVDdj7Vih0zp+tcMhwRpBeLyqtIjlJKAIZSbI8SGSF3k0pA3mR5tHuwPFoa7N7reoq2bqCsAk1HqCu5uvI1n6JuRXI+S1Mco54YmYTwcn6Aeic+kssXi8XpXC4V3t7/ADuTNKaQJdScAAAAAElFTkSuQmCC)](https://mybinder.org/v2/gh/IncQueryLabs/incquery-server-jupyter/master?filepath=example-notebook-home%2Facquisition-test.ipynb)
[![Acquisition binder (develop branch)](https://img.shields.io/badge/launch-acquisition%20binder%20(develop%20branch)-F5A252.svg?logo=data:image/png;base64,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)](https://mybinder.org/v2/gh/IncQueryLabs/incquery-server-jupyter/develop?filepath=example-notebook-home%2Facquisition-test.ipynb)

## Try it first

Click the __binder__ shield above to spin up a deployment publicly hosted on [MyBinder](https://mybinder.org/), with wired-in guest access to [a public IQS demo instance](https://openmbee.incquery.io) and [the OpenMBEE public MMS model repository](https://mms.openmbee.org/).

**Warning:** The resulting notebook will not be persistent, it cannot be shared and it can be deleted anytime! This usage is recommended only for one-time, short-lived experiments!


## Getting started 

Assuming that you have cloned this repository to your computer at path `${this-git-repo}`, the following instructions will help you get the Jupyter extensions for IQS running. As a main dependency, this involves the installation of the (automatically generated) Python-based IQS API client. 

### Prerequisites 

For first-time users, we generally recommend Miniconda3/Anaconda and `conda` (see below), but it is possible to do without. 

#### Installing Jupyter using Conda 

1. Make sure Miniconda3/Anaconda is installed, along with Python 3.7+ and the `conda` package manager 
1. Make sure Jupyter is installed: 

        conda install jupyter
        
    See details at: [jupyter.org](https://jupyter.org/install)

#### Installing Jupyter using `pip`

If you already have Python 3.7+, you can alternatively use the `pip` package manager to acquire Jupyter and install the rest of the packages. 

        pip install jupyter
        

### Installing the Python-based IQS API client

You must install the generated Python client package by executing ONE of the following options.

#### Release version from public repository 

Builds are available [on PyPI](https://pypi.org/project/incqueryserver-api-python-client/) and [on Conda forge](https://anaconda.org/conda-forge/incqueryserver-api-python-client).

The Conda-forge package is maintained in the incqueryserver-api-python-client [feedstock repository](https://github.com/conda-forge/incqueryserver-api-python-client-feedstock.git)

* Install from PyPI: `pip install incqueryserver-api-python-client`
* Install from Conda forge: `conda install -c conda-forge incqueryserver-api-python-client`

Note that these publicly available builds have been generated to support basic authentication. If your IQS instance uses another authentication method, you need to install the package build shipped with your IQS instance.

#### Version supplied with IQS instance  

Locate the Python client library hosted at your IQS installation; e.g. the library accompanying the public IQS demo server is available at https://openmbee.incquery.io/client/ for installation; copy the link to the actual package archive (*sdist*) file. Install this *sdist* using `pip`. If you are using Anaconda, make sure to issue the below command line from your Anaconda console.

        pip install ${address-of-python-client-sdist}

#### Roll your own: generate Python client for your own IQS instance   


1. Make sure you have OpenAPI Generator. We have verified that OpenAPI 3.3.4 works; OpenAPI 4+ has some issues. Just download the [.jar](https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/3.3.4/openapi-generator-cli-3.3.4.jar) from the [Mvn Repository](https://mvnrepository.com/artifact/org.openapitools/openapi-generator-cli/3.3.4).   
1. Locate the OpenAPI definition file (`.yaml`) shipped with your IQS instance. You will find the link in the "*Swagger UI*" tab of the *IncQuery Server Web Console*; e.g. the API definition of the public demo instance is available [here](https://openmbee.incquery.io/iqs4twc.yaml).
1. Within the OpenAPI definition file, find a line that looks like `version: 0.16.0`; it will be found near the top, below `info:`. This version number is the API version of your IQS installation.
1. At the end of the OpenAPI definition file, append a few lines (continuing the section `components:` and then adding a new section `security:`) to specify the authentication method of your IQS instance. Be mindful of proper indentation. For instance, in case of basic authentication, you would add these lines: 
 
         securitySchemes:
           basicAuth:
             type: http
             scheme: basic       
       
       security:
         - basicAuth: []

1. Generate a Python API into `${this-git-repo}/source-gen/incqueryserver-api-python-client` using the following command line:
 
            java -jar ${path-to-OpenAPI/openapi-generator-cli-3.3.4.jar} generate -i ${path-to-API-definition-yaml} -g python -o ${this-git-repo}/source-gen/incqueryserver-api-python-client -DpackageVersion="${API-version-of-your-IQS-instance}" -DpackageUrl="https://incquery.io" -DpackageName=iqs_client -DprojectName=incqueryserver-api-python-client  

1. Ensure that the generated Python client implementation is available to notebooks by executing ONE of the following options: 
   * For end users: 

            pip install ${this-git-repo}/source/incqueryserver-jupyter

   * For IQS developers who repeatedly edit the `.yaml` definition file and regenerate the Python code: issue one of the following commands to perform a "developer" install directly from the generated source project; changes to the source will be reflected immediately to newly (re)started Python interpreters / Jupyter kernels (previously started kernels that already executed the `import` will keep the old content until restarted). Select the appropriate command line depending whether you use `pip` or `conda`.

            pip install -e ${this-git-repo}/source-gen/incqueryserver-api-python-client
            conda develop ${this-git-repo}/source-gen/incqueryserver-api-python-client

Note: the generated client will only include the Acquisition API in versions 0.16 and above.

### Installing the Jupyter-specific client extensions

You must install the Jupyter support itself by executing ONE of the following options.

#### Release version from public repository 

Builds are available [on PyPI](https://pypi.org/project/incqueryserver-jupyter/) and [on Conda-forge](https://anaconda.org/conda-forge/incqueryserver-jupyter)

The Conda-forge package is maintained in the incqueryserver-jupyter [feedstock repository](https://github.com/conda-forge/incqueryserver-jupyter-feedstock.git)

* Install from PyPI: `pip install incqueryserver-jupyter`
* Install from Conda-forge: `conda install -c conda-forge incqueryserver-jupyter`

#### Install from source using Conda 

Ensure that the non-generated Jupyter-specific client extensions are available to notebooks by executing ONE of the following options: 
   * For end users (in the Anaconda console environment):
       * Clone the  [feedstock repository](https://github.com/conda-forge/incqueryserver-jupyter-feedstock.git) where the package is maintained
       * Build a conda package from the client extensions sources, then install it:
            ```
            git clone https://github.com/conda-forge/incqueryserver-jupyter-feedstock.git
            conda build -c conda-forge ${feedstock-git-repo}/recipe
            conda install -c conda-forge --use-local incqueryserver-jupyter
           ```
       * **Plase note that this will install the release version from PyPI**

   * For developers: issue the following command to perform a "developer" install directly from the source project; changes to the source will be reflected immediately to newly (re)started Python interpreters / Jupyter kernels (previously started kernels that already executed the `import` will keep the old content until restarted).

            conda develop ${this-git-repo}/source/incqueryserver-jupyter

#### Install from source using `pip`

Ensure that the non-generated Jupyter-specific client extensions are available to notebooks by executing ONE of the following options: 
   * For end users: 

    pip install ${this-git-repo}/source/incqueryserver-jupyter

   * For developers: issue the following command to perform a "developer" install directly from the source project; changes to the source will be reflected immediately to newly (re)started Python interpreters / Jupyter kernels (previously started kernels that already executed the `import` will keep the old content until restarted).

    pip install -e ${this-git-repo}/source/incqueryserver-jupyter

Note that since we rely on `conda` packaging by default, the dependencies may have to be installed manually in case of using `pip`.

### Final steps

Whether you installed from source or from the public repository, it is a good idea to verify your installation. Also, you might need a few additional components if you want to run our demo notebooks.

#### Smoke test

Run [test_iqs_client.py](https://github.com/IncQueryLabs/incquery-server-jupyter/blob/master/test-scripts/test_iqs_client.py) and [test_iqs_jupyter.py](https://github.com/IncQueryLabs/incquery-server-jupyter/blob/master/test-scripts/test_iqs_jupyter.py) as a quick smoke test to verify correct installation of the generated client package and the Jupyter extensions package, respectively.

        python ${this-git-repo}/test-scripts/test_iqs_client.py
        python ${this-git-repo}/test-scripts/test_iqs_jupyter.py


#### Additional dependencies

The demo notebook uses `plotly` and `cufflinks` to demonstrate possible applications of the client extensions package. It is not recommended to install `cufflinks-py` using conda, as conda-forge seems to host an obsolete version not compatible with the demo; simply issue `pip install cufflinks` from the Anaconda console instead. 

The direct connection to the MMS server additionally requires the installation of `mms-python-client`; you might have missed this dependency if you installed the Jupyter extensions in development mode.
 * **CAUTION** pin to `mms-python-client==3.4.2.1` until https://github.com/Open-MBEE/mms-alfresco/issues/346 is resolved, see https://github.com/IncQueryLabs/incquery-server-jupyter/issues/35

## Running the notebook

### Optional: set up environment variables first
  
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

1. Designate a location as the notebook home, where notebook files will be stored. For example, use `${this-git-repo}/example-notebook-home`.
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
       
   1. You can now interact with the IQS instance. For example, if your IQS installation is connected to MMS, browse for an MMS commit using 
   
            commit_selector = iqs.jupyter_tools.mms_commit_selector_widget()
   
   1. Access the full JSON/RPC API of IQS in the form of (you may use TAB completion):
   
            iqs.${api-category-label}.${api-call}
