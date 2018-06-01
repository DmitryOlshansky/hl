## HL - a simple flexible fuzzy host search/execute

HL (Host List) uses omni-box style query (think Google or Altavista ;)) using easy to understand weighted fuzzy-matching
over hierarchical host lists. Things considered in match are project name, env (prod, qa, dev, etc.), tags, ports and FQDN itself.

Note that what is project name, or environment, etc. is arbitrary convention and they all work the same in HL.
In reality, HL accepts any hierarchical classification with each level considered as a tag. Upper classification tags have proportionally more weight then any other below, that is used to disambiguate fuzzy string matches.

## Example

Iamginary config for simple project with balancer, API and DB, having 2 environments - staging on AWS and production on bare metal in 2 DCs. Note that admins are funky and DB have their own unique and inconsistent names + different ports, that we want to classify properly our with tags.


```yml
# our-project.yml:
---
prod:
    api:
        us-east-dc:
            hosts: api-[0-4]-east-prod.our-company.cloud
            ports:
                http: 8080
        us-west-dc:
            hosts: api-[0-4]-west-prod.our-company.cloud
            ports:
                http: 8080
    db:
        us-east-dc:
            # list of host patterns is acceptable
            hosts:
                - ricky-the-great.our-company.cloud
                - mikky-the-malicious.our-company.cloud
            ports:
                postgres: 5432
         us-east-dc:
            # list of different host entries as well
            - hosts: east-mcgram-db.our-company.cloud
              ports:
                postgres: 5432
            - hosts: east-paul-db.our-company.cloud
              ports:
                postgres: 6432
qa:
    aws:
        api:
            hosts: api-[0-4]-aws-staging.ec2.cloud
            ports:
                http: 8080
        db:
            hosts: db-aws-staging.ec2.cloud
            ports:
                postgres: 5432

```

Enter `hl` tool:
```bash
hl aws

```

## Algorithm

TBD
