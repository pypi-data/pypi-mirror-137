# RelyComply Python Client and CLI

**BETA RELEASE**

This package contains the python client and CLI for the RelyComply platform:

> RelyComply is an end-to-end Anti-Money Laundering (AML) Platform, managing detection, risk management and automation of your AML compliance requirements

The CLI makes configuration of the system substantially simpler and allows for a full configuration-as-devops experience. 

The python client exposes both a lower level GraphQL client which makes it easy to interact with the GraphQL APi in a pythonic manner. As well as a higher-level integration client that provides useful routines for common integration tasks.

## Credentials

Credentials for the various clients can be loaded in multiple ways. In the following order of precedence:

* Constructor Arguments
* Environment Variables
* AWS Secrets
* Configuration Files (.rely.toml)
* Defaults

Credentials can stack, so you can define certain credentials in a cofig file for example, and override it with an environment variable.

The following credentials can be set:

* token: The API token of the user
* url: The url of the RelyComply application (default: `https://app.relycomply.com`)
* impersonate: If user impersonation is available for your user this allows you to make a command on behalf of another user. This should be in format `<organisation_name>:<user_email>`, for example `relycomply:james@relycomply.com`.

**Constructor Arguments**

You can pass credentials when constructing a client as keyword arguments, e.g.

```python
client = RelyComplyGQLClient(token="<token>")
```

**Environment Variables**

The client will look if there are matching environment variables of the format `RELYCOMPLY_<CREDENTIAL>`, for example: `RELYCOMPLY_TOKEN=<token>`.

**AWS Secrets**

The client can integrate with the AWS Secrets Manager. This is done by setting appropriate environment variables with the naming convention `RELYCOMPLY_<CREDENTIAL>_AWS_SECRET` and the value being the secrets path, for example:

```
RELYCOMPLY_TOKEN_AWS_SECRET=path/to/my/secret
```

For more information please consult the [AWS Secrets Manager documentation](https://docs.aws.amazon.com/secretsmanager/).

**Config Files**

Credentials can be set in a `.rely.toml` file. The client will search the current working directory, and all parent directories in order, with the most local directory taking precedence. The `.rely.toml` file is a TOML file with the credentials as keys, e.g.

```toml
token="<token>"
url="https://relycomply.customer.com"
```

**Default Credentials**

The following credentials have default values:

```toml
url="https://app.relycomply.com"
```

## RelyComplyGQLClient

A flexible and intelligent GraphQL client for RelyComply. This client will create methods that match the mutation sand queries of the RelyComply API, and expose them with familiar calling conventions. It also handles paging as well as simplifying the returned structures.

It can be constructed as below:

```python
from relycomply_client import RelyComplyGQLClient

client = RelyComplyGQLClient()

# Or with specific credentials
client = RelyComplyGQLClient(token="<token>")
```

Queries can be called with their lowerCase field name and any filter arguments as kwargs, e.g.:

```python
client.products(nameContain="ZA") # Will return a list of products
client.products(nameContain="ZA", _iter=True) # Will return a lazy generator
client.products(name="retailZA", _only=True) # Will return only the first object or None
```

The client will automatically collapse edge lists into plain lists of objects to make the output easier to work with.

Mutations can be called in a similar way, but arguments will be lifted into the $input variable

```python
client.createProduct(name="retailZA", label="South African Retail") # Returns the created product
```

The interface is automatically generated from the GQL schema as well as the CLI support templates. Thus it should always be in sync with the latest features on the platform.

The client also exposes a raw GraphQl call when you need to make a more complex query. No post processing will be done on the results. For example to query the first 10 products.

```python
client.graphql(
    """
    products(first:$first) {
        edges {
            node {
                id
                name
            }
        }
    }
    """, 
    variables=dict(first=10)
)
```

## RelyComplyClient

The RelyComplyCLient contains higher level methods that make common integration tasks simpler. It provides simple integration with various cloud services and common data tools like pandas.

```python
from relycomply_client import RelyComplyGQLClient
rc = RelyComplyClient()

# Or for quick usage for a standard client
from relycomply_client.rc import rc
```

A quick overview of a common data integration with the transaction monitoring is shown below:

```python
# Load a file with pandas
raw_df = pd.read_csv(file_path)

# Perform some cleaning
df = clean_raw_df(raw_df)

# Pull in a datafile from a known source. 
# This will automatically creat a signed URL if an S3 path is passed
raw_data_file = rc.pull_to_datafile(
    file_path, "raw/" + file_name, wait_for_ready=True
)

# Upload a dataframe as parquet datafile
processed_data_file = rc.put_to_datafile(df, "processed/" + file_name)

# Ingest the given files

# Note that the responses from previous calls can be passed as is for the call
# arguments. Their id's will be automatically extracted.
data_source_version = rc.ingest_datasource(
    data_source, data_file=processed_data_file, raw_data_files=[raw_data_file]
)

# Run a monitor
rc.run_monitor(monitor_name, source_versions=[data_source_version])
```

The underlying `RelyComplyGQLClient` can be accessed with `.gql` property.

```python
rc.gql.createProduct(name="bank_account", label="My Bank Account)
```

## Command Line Interface (CLI)

The command line interface is an important part of our developer first mentality. It acts as a layer on top of the GraphQL API and makes it substantially easier to for power-users to explore and manipulate RelyComply.

GraphQL is excellent as an API for integration, but can be a lot extra overhead to quickly just see what is happening in the system. Primarily this is because the user has to define the output format they want. This greatly improves the flexibility but certainly is not as easy as just using curl on a rest endpoint. The rely CLI makes it easy to perform the standard queries and mutations on the GraphQL API, without extra effort by the user.

The CLI can be accessed with the `rely` command. The basic format is to call it with a `type` and an `action`. This will automatically be coerced into the appropriate GraphQL calls. 

Arguments can be passed as keyword arguments of the form `--key=value` additionally a configuration file name can be passed as the final argument. The value can be a json string, which will be parsed correctly for complex arguments. Arguments are merged with the command line arguments taking precedence.

Queries can be performed with the `list` and `retrieve` actions, `retrieve` will return a single item, and `list` will display a table of items.

```bash
rely product list # Will list all the products
rely product list --nameContains="za" # Will list all the products with za in their name
rely product retrieve --id=123 # Will return just the specified product 
```

Mutations can called by their name, with the action being prepended to the type. The system is intelligent enough that the case of the action and type do not matter.

```bash
# Will call createProduct
rely product create --name="bank_account" --label="Bank Account" 

# Will update the given product (updateProduct) based on the given ID and the config file (pr_my_product.toml)
rely product update --id=10 pr_my_product.toml
```

Certain aliases are provided for convenience, e.g. 

```bash
# This will call addCaseNote
rely case addNote --case=123 --note="This is my note"
```

The format of the output can be controlled with the `--json`, `--yaml` and `--toml` (default) flags.
