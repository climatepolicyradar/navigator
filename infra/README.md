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

### Python Environment

A virtualenv `venv` is created/used by Pulumi.

### Infrastructure code

The code is broken up into these conceptual parts:

- backend: everything needed for the API application, e.g. beanstalk
- storage: relational database, future: search index
- deployment_resources: single-use components that facilitate deployment, e.g. container registry, and the bucket which
  holds the beanstalk deployment manifest
- plumbing: all the invisible parts, like security groups, roles, VPCs, etc
- tasks: lambda tasks that need to run on occasion, like database migrations

### Bastion server

The bastion server's instance ID will be exported as `bastion.id` via Pulumi.

To connect to it, ensure you have the [Session Manager plugin installed](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html):

```shell
aws ssm start-session --target <instance-id>
```

Then run migrations via psql. The RDS URL will be exported as `rds.address` via Pulumi:

```shell
psql -h rds-instance<random>.<random>.eu-west-2.rds.amazonaws.com -U navigator_db_user navigator
```

When prompted for the password, use the one from

```shell
pulumi config get infra:db_password
```

## Deployment

TODO: revisit instruction

### Deployment stacks

We have two stacks: `ant` and `dev`, which due to a quirk of fate have the following mapping (these names will be updated in the future):

- ant => dev.app.climatepolicyradar.org
- dev => app.climatepolicyradar.org

To see the available stacks:

```shell
pulumi stack ls
```

To see the current stack your local environment is pointing at:

```shell
pulumi stack | head -n1
Current stack is ...:
```

To point to another stack:

```shell
pulumi stack select <stack name>
```

### The deployment process

#### Deploy to dev.app.climatepolicyradar.org for UAT

Select the stack for the development environment

```shell
pulumi stack select ant
```

Deploy the stack (make sure to inspect the console output to confirm that you are deploying to the expected environment).

```shell
pulumi up
```

(pulumi up will often fail after building the required docker images, when this happens simply run `pulumi up` again).

Caches must now be invalidated in the CloudFront distribution for the dev environment, or older cached javascript may
be served, rather than the updated code. The distribution can be located at "https://us-east-1.console.aws.amazon.com/cloudfront"

Developers & stakeholders can now perform UAT against the deployed dev environment.

#### Deploy to app.climatepolicyradar.org

When the testing is complete & everyone is happy, a deploy can be main against the production environment:

TODO: instructions for 2 main scenarios (those with/without downtime).

```shell
pulumi stack select dev
pulumi up
```

### The deployment status

TODO: revisit this file name & content

The file [blue-green-status.json](./blue-green-status.json) contains a mapping from stack name to environment (currently "dev" or "prod").

The Pulumi scripts look at this file to decide how to configure certain variables.

## Troubleshooting

### Installing developer dependencies to the virtualenv for debugging

To install developer tooling (e.g. for IDE):

```shell
source venv/bin/activate
pip install -r requirements-dev.txt
```

If, for any reason, you lose your `venv` folder, Pulumi will recreate it for you if you run any command.

E.g. `pulumi about`.

### Visualise dependencies

```shell
pulumi stack graph --color always graph.dot
# sudo apt install -y graphviz
cat graph.dot|dot -Tpng > output.png
```
