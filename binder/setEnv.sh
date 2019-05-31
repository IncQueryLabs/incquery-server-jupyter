#!/bin/bash

IQS_DEMO_HOST=https://mms-demo.iqs.incquery.io
API_SUFFIX=/api
CLIENT_SDIST_SUFFIX=/client/incqueryserver-api-python-client-0.11.0.tar.gz

CLIENT_SDIST_ARCHIVE_LOC=${IQS_DEMO_HOST}${CLIENT_SDIST_SUFFIX}

export IQS_JUPYTER_default_IQS_address=${IQS_DEMO_HOST}${API_SUFFIX}
export IQS_JUPYTER_default_IQS_username=guest
export IQS_JUPYTER_default_IQS_password=incqueryserverguest

export IQS_JUPYTER_default_mms_org=tmtorg
export IQS_JUPYTER_default_mms_project=PROJECT-d94630c2-576c-4edd-a8cd-ae3ecd25d16c
export IQS_JUPYTER_default_mms_ref=master
export IQS_JUPYTER_default_mms_commit=5739c537-faa3-48bc-b1ea-aa0837a4f23d
