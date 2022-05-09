# Infrastructure

Infrastructure as code, using Pulumi.

## Quick start

[Install Pulumi](https://www.pulumi.com/docs/get-started/install/), and then run

```shell
pulumi login
pulumi org set-default climatepolicyradar
pulumi stack select dev
```

And then `pulumi about` to verify.

## Python Environment

`venv` is created/used by Pulumi.

To install developer tooling (e.g. for IDE):

```shell
source venv/bin/activate
pip install -r requirements-dev.txt
```

## Troubleshooting

If, for any reason, you lose your `venv` folder, Pulumi will recreate it for you if you run any command.

E.g. `pulumi about`.

## Infrastructure code

The code is broken up into these conceptual parts:

- backend: everything needed for the API application, e.g. beanstalk
- storage: relational database, future: search index
- deployment_resources: single-use components that facilitate deployment, e.g. container registry, and the bucket which
  holds the beanstalk deployment manifest
- plumbing: all the invisible parts, like security groups, roles, VPCs, etc
- tasks: lambda tasks that need to run on occasion, like database migrations

## Visualise dependencies

```shell
pulumi stack graph --color always graph.dot
# sudo apt install -y graphviz
cat graph.dot|dot -Tpng > output.png
```

## Bastion server

`pulumi up` will export the bastion server's IP address, or you can find it via [the AWS console](https://eu-west-2.console.aws.amazon.com/ec2/v2/home?region=eu-west-2#NIC:securityGroup=bastion*) in the `Public IPv4 address` column.

Then connect to it (provided your SSH public key is provisioned for):

```shell
ssh ec2-user@<the-ip>
```

Then run migrations via psql:

```shell
psql -h rds-instance<random>.<random>.eu-west-2.rds.amazonaws.com -U navigator_db_user navigator
```

When prompted for the password, use the one from

```shell
pulumi config get infra:db_password
```
