#!/bin/bash

IQS_DEMO_HOST=https://openmbee.incquery.io
CLIENT_SDIST_SUFFIX=/client/incqueryserver-api-python-client-0.12.0.tar.gz

CLIENT_SDIST_ARCHIVE_LOC=${IQS_DEMO_HOST}${CLIENT_SDIST_SUFFIX}

export IQS_JUPYTER_default_IQS_address=${IQS_DEMO_HOST}
export IQS_JUPYTER_default_IQS_username=guest
export IQS_JUPYTER_default_IQS_password=incqueryserverguest

export IQS_JUPYTER_default_mms_org=9ff6af30-af8a-4f9d-a26b-499010ba5b6e
export IQS_JUPYTER_default_mms_project=PROJECT-0e791c0e-16fe-422f-8f85-462ab035ce99
export IQS_JUPYTER_default_mms_ref=master
export IQS_JUPYTER_default_mms_commit=081c34aa-871f-4404-bfb0-9bd25ac80c33

export IQS_JUPYTER_default_mms_address=https://mms.openmbee.org/alfresco/service
export IQS_JUPYTER_default_mms_username=openmbeeguest
export IQS_JUPYTER_default_mms_password=guest
