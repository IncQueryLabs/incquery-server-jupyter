#!/bin/bash

IQS_DEMO_HOST=https://openmbee.incquery.io
API_SUFFIX=/api
CLIENT_SDIST_SUFFIX=/client/incqueryserver-api-python-client-0.11.0.tar.gz

CLIENT_SDIST_ARCHIVE_LOC=${IQS_DEMO_HOST}${CLIENT_SDIST_SUFFIX}

export IQS_JUPYTER_default_IQS_address=${IQS_DEMO_HOST}${API_SUFFIX}
export IQS_JUPYTER_default_IQS_username=guest
export IQS_JUPYTER_default_IQS_password=incqueryserverguest

export IQS_JUPYTER_default_mms_org=9ff6af30-af8a-4f9d-a26b-499010ba5b6e
export IQS_JUPYTER_default_mms_project=PROJECT-0e791c0e-16fe-422f-8f85-462ab035ce99
export IQS_JUPYTER_default_mms_ref=master
export IQS_JUPYTER_default_mms_commit=8598d33b-4950-4355-a404-18b0d8148b47
