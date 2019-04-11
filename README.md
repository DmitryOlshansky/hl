## HL - a simple flexible fuzzy host search/execute

HL (Host List) provides omni-box style query interface (inspired by next to any modern browser).
HL uses easy to understand weighted fuzzy-matching over hierarchical host lists. Things considered in full-text matching process are project name, env (prod, qa, dev, etc.), tags, ports and FQDN itself.

Note that what defines project name, or environment, etc. is your own arbitrary convention and they all work the same in HL.
In reality, HL accepts any hierarchical classification with each level considered as a tag. Upper classification tags have proportionally more weight then any other below, this property is used to disambiguate fuzzy string matches.

## Installation 

```sh
pip install --user hl
```

## Example

Imaginary config for simple project with API and DBs, having 2 environments - staging on AWS and production on bare metal in 2 DCs. Note that admins are funky and DB have their own unique and inconsistent names + different ports, that we want to classify properly our with tags.


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

Algorithm is simple (subject to change) - first we traverse the graph of host patterns and consider each tag as a token inversly weighted by depth (the deeper, the less weight). Then we apply sensible tokenization of hostname (split by '-', '_' and '.'), each token gets minimal weight. The result is then merged tags and hostname tokens.

Query is tokenized in the same way as hostnames. After that the two frequency dictionaries are multipled like sparse vectors, to minimize sharp effect of repeated words, weights in query is smoothed by sigmoid (this will likely change in the future).

Next step is to use trigramms or similar to fix typos in query and still find closest token to match.
