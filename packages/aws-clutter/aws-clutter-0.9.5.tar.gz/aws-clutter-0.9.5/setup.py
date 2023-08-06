# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_clutter', 'aws_clutter.clutter']

package_data = \
{'': ['*'], 'aws_clutter': ['data/*']}

install_requires = \
['boto3>=1.19.4,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'importlib-metadata>=4.8.1,<5.0.0',
 'importlib-resources>=5.3.0,<6.0.0',
 'pendulum>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['awsclutter = aws_clutter.cli:cli']}

setup_kwargs = {
    'name': 'aws-clutter',
    'version': '0.9.5',
    'description': 'monitor the cost of unused AWS resources',
    'long_description': '# AWS Clutter\n\nPython package that reports on "AWS clutter" and how much they cost. Can report via CloudWatch custom metrics.\n\n## Features\n* Cost-Aware. Where relevant, `awsclutter` calculates how much the clutter is costing you.\n* Cross-Region. A common challenge for AWS users is the lack of *cross-region* visibility (for many types of resources). `awsclutter` scans across every region that\'s accessible to your AWS account so that it can uncover clutter in regions that are rarely visited.\n* Fast.  `awsclutter` uses asynchronous programming to run queries concurrently. This makes it very fast/efficient in retrieving the underlying data from AWS.\n\n## Getting Started\nTo install:\n```\npip install aws-clutter\n```\nThis installs a command line tool, `awsclutter`. You can use this to generate a report on "AWS clutter". \n\nSample Commands:\n```\n# summary list of all the clutter resources:\nawsclutter list --summary\n\n# detailed list of debs (detached EBS):\nawsclutter list debs \n\n# for any resource type, to get its description (replace `debs` below with the resource type in question):\nawsclutter list debs | jq \'.debs.description`\n\n# using jq to identify the properties of \'debs\' resource type:\nawsclutter list debs | jq \'.debs.resources."us-east-1"[0] | keys\'\n\n# to push cloudwatch metrics:\nawsclutter watch\n\n# to see what the cloudwatch metrics look like (without actually pushing them):\nawsclutter watch --dry-run\n\n# to see what the cloudwatch custom metric names and their dimensions look like:\nawsclutter watch --dry-run | jq -r \'.[] | .MetricName + "[" + ( [.Dimensions[].Name] | join(",")) + "]"\' | sort\n```\n\n## Installing as Lambda\nIf you\'re familiar with Terraform, see the [README](https://github.com/cloudkeep-io/aws-clutter/blob/main/terraform/README.md) under `terraform` directory. This is a Terraform module that installs this Python code as a Lambda function that will get triggered on a schedule (by default every 10 minutes.) Once deployed, look under the namespace CloudKeep in CloudWatch for the various custom metrics. More details on these metrics below.\n\n\n## Clutter Type debs - Detached (Orphaned) EBS Volumes\n\nDetached EBS (Elastic Block Storage) volumes constitue one of the most common sources of AWS cost that creeps up over time. When an EC2 instance is instantiated and extra storage is desired, it is easy to add an EBS volume. At the time of instantiation, there is an option to "Delete on Termination" (of the EC2 instance). The default is "No".\n\nThus, it\'s common that these detached volumes exist in a given AWS environment. The problem is two-fold:\n* Not all organizations have a process in place where AWS users (who can create EC2 instances) will actually delete these volumes when they no longer need it.\n* These detached volumes do not stand out in the AWS console where an admin might do something about them.\n\n`awsclutter` allows an AWS admin to keep track of these detached EBS volumes by creating the following CloudWatch custom metrics:\n* `DetachedEBSCount` - number of detached EBS volumes\n* `DetachedEBSMonthlyCost` - monthly cost of detached EBS volumes\n\nThese custom metrics are created under the name space of `CloudKeep` and can have the following dimensions:\n* `Currency` (only for `DetachedEBSMonthlyCost`) - required - currency for the EBS cost, as per the AWS pricing metric. Currently, this is \'CNY\' for China regions and \'USD\' for everywhere else.\n* `RZCode` - Region/Zone Code. E.g., `us-east-1`.\n* `VolumeType` - Volume Type. E.g., `gp3`.\n* `VolumeId` - Volume ID. Note the dimensions `RZCode` and `VolumeType` are always added to the metric with `VolumeId` in it.\n\nA metric without a certain dimension represents a summation over the missing dimension. For example, `DetachedEBSCount` without any dimensions is the total number of all the Detached EBS Volumes (across all the regions and volume types). `DetachedEBSCount[RZCode]` represents the total number of detached EBS volumes in the specified `RZCode`.\n\nBy default, custom metrics with the dimension of `RZCode` is added. You can specify additional dimensions to be surfaced via an environment variable `DEBS_DIMS`, by setting it to a list of dimensions, separated by a comma. E.g., `"RZCode,VolumeType"`.\n\n## Clutter Type ulbs - Unused Load Balancers\n\nUnused load balancers can come about when the actual servers and/or Lambda functions that backend the load balancer are removed. Even if a load balancer is not being used at all, it incurs a charge, and so we collect their info here.\n\nThe custom metrics created are:\n* `UnusedLBCount` - number of unused Load Balancers\n* `UnusedLBMonthlyCost` - monthly cost of unused Load Balancers\n\nAnd these metrics can have the following dimensions\n* `Currency` (only for `UnusedLBMonthlyCost`) - required - currency for the LB cost, as per the AWS pricing metric. For ELBs, these are all \'USD\'.\n* `RZCode` - Region/Zone Code. E.g., `us-east-1`.\n* `LBType` - Load Balancer Type. (\'application\', \'network\', \'gateway\') - Note "Classic" is not supported.\n\n',
    'author': 'Shinichi Urano',
    'author_email': 's@urano.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.10,<4',
}


setup(**setup_kwargs)
