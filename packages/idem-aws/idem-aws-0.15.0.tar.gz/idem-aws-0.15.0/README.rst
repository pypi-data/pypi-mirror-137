========
IDEM_AWS
========
AWS Cloud Provider for Idem

INSTALLATION
============

The aws idem provider can be installed via pip::

    pip install "idem-aws [full]"

DEVELOPMENT
===========

Clone the `idem-aws` repository and install with pip.
Install extra requirements by specifying "localstack" or "full"
in brackets (in ZSH you will have to escape the brackets).

.. code:: bash

    git clone git@gitlab.com:saltstack/pop/idem-aws.git
    pip install -e idem_aws[full] # [google_auth,localstack,full]

Set UP
======
After installation the AWS Idem Provider execution and state modules will be accessible to the pop `hub`.
In order to use them we need to set up our credentials.

Create a new file called `credentials.yaml` and populate it with credentials.
If you are using localstack, then the `id` and `key` can be bogus values.
The `default` profile will be picked up automatically by `idem`.

There are many ways aws providers/profiles can be stored. See `acct backends <https://gitlab.com/Akm0d/acct-backends>`_
for more information.

There are multiple authentication backends for `idem-aws` which each have their own unique set of parameters.
The following examples show some of the parameters that can be used in these backends to define profiles.
All backends end up creating a boto3 session under the hood and storing it in the `ctx` variable that gets passed
to all idem `exec` and `state` functions.

All authentication backends support two optional parameters, `endpoint_url` and `provider_tag_key`.  The `endpoint url`
is used to specify an alternate destination for boto3 calls, such as a localstack server or custom dynamodb server.
The `provider_tag_key` is used when creating new resources.  `idem-aws` will only interact with resources that are tagged
with the the customizable `provider_tag_key` key.

credentials.yaml:

..  code:: sls

    aws:
      default:
        endpoint_url: http://localhost:4566
        use_ssl: False
        aws_access_key_id: localstack
        aws_secret_access_key: _
        region_name: us-west-1

You can also authenticate with `aws-google-auth` if it is installed.

.. code:: sls

    aws.gsuite:
      my-staging-env:
        username: user@gmail.com
        password: this_is_available_but_avoid_it
        role_arn: arn:aws:iam::999999999999999:role/xacct/developer
        idp_id: 9999999
        sp_id: 999999999999
        region: us-east-1
        duration: 36000
        account: developer

The google profile example is not named `default`. To use it, it will need to be specified explicitly in an idem state.

.. code:: sls

    ensure_resource_exists:
      aws.ec2.vpc.present:
        - acct_profile: my-staging-env
        - name: idem_aws_vpc
        - cidr_block: 10.0.0.0/24

It can also be specified from the command line when executing states.

.. code:: bash

    idem state --acct-profile my-staging-env my_state.sls

It can also be specified from the command line when calling an exec module directly.

.. code:: bash

    idem exec --acct-profile my-staging-env boto3.client.ec2.describe_vpcs


The last step to get up and running is to encrypt the credentials file and add the encryption key and encrypted file
path to the ENVIRONMENT.

The `acct` command should be available as `acct` is a requisite of `idem` and `idem-aws`.
Encrypt the the credential file.

.. code:: bash

    acct encrypt credentials.yaml

output::

    -A9ZkiCSOjWYG_lbGmmkVh4jKLFDyOFH4e4S1HNtNwI=

Add these to your environment:

.. code:: bash

    export ACCT_KEY="-A9ZkiCSOjWYG_lbGmmkVh4jKLFDyOFH4e4S1HNtNwI="
    export ACCT_FILE=$PWD/credentials.yaml.fernet


You are ready to use idem-aws!!!

LOCALSTACK
==========
Localstack can be used to test idem-aws on your local machine without needing legitimate aws credentials.
It can be used for running the idem-aws tests or for testing your states locally.

Install localstack with pip:

.. code:: bash

    pip install "localstack [full]"

Start the localstack infrastructure:

.. code:: bash

    localstack infra start



TESTING
=======
In order to run the tests you must have a profile called "test_development_idem_aws" in your `acct` provider
information. This can use localstack (recommended) or valid production aws credentials (at your own risk).

.. code:: sls

    aws:
      test_development_idem_aws:
        endpoint_url: http://localhost:4566
        use_ssl: False
        aws_access_key_id: localstack
        aws_secret_access_key: _
        region_name: us-west-1

It's recommended to run the tests using localstack (by specifying your localstack container address as your endpoint_url)

.. code:: bash

    pytest idem-aws/tests

EXECUTION MODULES
=================

Once everything has been set up properly, execution modules can be called directly by `idem`.
Execution modules mirror the namespacing of the boto3.client and boto3.resource modules and have the same parameters.

For example, this is how you could list Vpcs from the command line with idem:

.. code:: bash

    idem exec boto3.client.ec2.describe_vpcs

You can specify parameters as well.
In the case of boto3 resources, args will be passed to the resource constructor and kwargs will be passed to the operation like so:

.. code:: bash

    idem exec boto3.resource.ec2.Vpc.create_subnet vpc-71d00419 CidrBlock="10.0.0.0/24"

STATES
======
States are also accessed by their relative location in `idem-aws/idem_aws/states`.
For example, `idem-aws/idem_aws/states/aws/ec2/vpc.py` contains a function `absent()`.
In my state file I can create a state that uses the `absent` function like so.

my_state.sls:

.. code:: sls

    idem_aws_test_vpc:
      aws.ec2.vpc.absent:
        - name: "idem_aws_test_vpc"

I can execute this state with:

.. code:: bash

    idem state my_state.sls

`idem state` also has some flags that can significantly boost the scalability and performance of the run.
Let's use this new state which verifies that 100 vpcs are absent:

.. code:: sls

    {% for i in range(100) %}
    idem_aws_test_vpc_{{i}}:
      aws.ec2.vpc.absent:
        - name: "idem_aws_test_vpc_{{i}}"
    {% endfor -%}

I can execute this state with `--runtime parallel` to make full use of idem's async execution calls:

.. code:: bash

    idem state --runtime parallel my_state.sls

Current Supported Resources states
++++++++++++++++++++++++++++++++++

ec2
"""
* elastic_ip
* flow_log
* instance
* internet_gateway
* nat_gateway
* route_table
* spot_instance
* subnet
* transit_gateway
* transit_gateway_vpc_attachment
* vpc

iam
""""
* instance_profile
* policy
* role
* role_policy
* role_policy_attachment
* user

kms
""""
* key

organizations
""""""""""""""
* organization
* organization_unit

s3
"""
* bucket
