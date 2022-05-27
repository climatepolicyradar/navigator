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

# Blue/green deployments

We have two stacks: `ant` and `dev`. These will assume the roles of "ant is blue" and "dev is green" or vice versa, depending on which env is currently being pointed to by CNAME (i.e. the ones that our users see). 

To see our stacks:

```
pulumi stack ls
```

To see the current stack your local environment is pointing at:

``` 
pulumi stack | head -n1
Current stack is ...:
```

To point to another stack:

``` 
pulumi stack select <stack name>
```

## The deployment process

Sprint N:
CNAME is currently pointing to `dev`, so leave it alone.
Devops run `pulumi stack select ant`
Development and changes happen against `ant`.
Developers and internal stakeholders do UAT against `ant` (possibly via staging.api.climatepolicyradar.org or some other private domain name).
Everyone is happy with `ant`.
Change CNAME so that it points api.climatepolicyradar.org to `ant` (more specifically, the elastic beanstalk instance in this stack)
Check api.climatepolicyradar.org and if you're not happy, flip the CNAME back to `dev`.
But if you're happy:
Change CNAME so that it points staging.api.climatepolicyradar.org to `dev` (more specifically, the elastic beanstalk instance in this stack)
Development can bow resume against `dev`.

Sprint N+1:
CNAME is currently pointing to `ant`, so leave it alone.
Devops run `pulumi stack select dev`
Development and changes happen against `dev`.
Developers and internal stakeholders do UAT against `dev` (possibly via staging.api.climatepolicyradar.org or some other private domain name).
Everyone is happy with `dev`.
Change CNAME so that it points api.climatepolicyradar.org to `dev` (more specifically, the elastic beanstalk instance in this stack)
Check api.climatepolicyradar.org and if you're not happy, flip the CNAME back to `ant`.
But if you're happy:
Change CNAME so that it points staging.api.climatepolicyradar.org to `ant` (more specifically, the elastic beanstalk instance in this stack)
Development can bow resume against `ant`.

## The deployment status

Which environment is currently "prod" and used by our users, and we're not allowed to make changes to? 
Which environment is currently "dev", and we're allowed to make changes to it?

The file [blue-green-status.json](./blue-green-status.json) is the definitive source of truth to answer that question.

Whenever we decide to make the current "dev" environment "prod", we edit this file.
The Pulumi scripts will then also look at this file to decide how to configure certain variables.