

# smily - SageMaker Inspection Library

`smily` is a python-library to quickly inspect SageMaker resoruces:

    $ smily logs head -n 10 <training-job-arn>
    ...


## Account Discovery

To ease its use, `smily` can automatically discover AWS profiles for a given resource.

For example, given the arn  `arn:aws:sagemaker:us-west-2:123456789012:training-job/my-training-job` the tool extracts the account-id `123456789012` and searches the aws config file for possible matches:

```
[profile my-profile]
account = 123456789012
```
