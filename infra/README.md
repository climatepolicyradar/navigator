# Infrastructure

Infrastructure as code, using Pulumi.

# Quick start

[Install Pulumi](https://www.pulumi.com/docs/get-started/install/), and then run

```
pulumi login
pulumi org set-default climatepolicyradar
pulumi stack select dev
```

And then `pulumi about` to verify.

# Python Environment

`venv` is created/used by Pulumi.

To install developer tooling (e.g. for IDE):

``` 
source venv/bin/activate
pip install -r requirements-dev.txt
```

# Troubleshooting

If, for any reason, you lose your `venv` folder, Pulumi will recreate it for you if you run any command.

E.g. `pulumi about`.

# Infrastructure code

The code is broken up into these conceptual parts:

- backend: everything needed for the API application, e.g. beanstalk
- storage: relational database, future: search index
- deployment_resources: single-use components that facilitate deployment, e.g. container registry, and the bucket which
  holds the beanstalk deployment manifest
- plumbing: all the invisible parts, like security groups, roles, VPCs, etc
- tasks: lambda tasks that need to run on occasion, like database migrations

# Visualise dependencies

``` 
pulumi stack graph --color always graph.dot
# sudo apt install -y graphviz
cat graph.dot|dot -Tpng > output.png
```

# Bastion server

`pulumi up` will export the bastion server's IP address, e.g. `1.2.3.4`, and then connect to it, presuming your key has been included:

``` 
ssh ec2-user@1.2.3.4
```