# Akinon Cloud Commerce CLI
Akinon CLI is an application designed to manage projects and applications 
in Akinon Cloud Commerce through a command line interface.

## Installation
After installing python 3.8+, run the following command. 
Then the Akinon CLI would be ready to be used.
```
$ pip install --user akinoncli
```

## Usage
Every cloud commerce user is registered to an `Account`. For a fresh user an `Account` would be 
created automatically. The authorized users who are registered to `Account` can create users
for the same `Account` using the CLI or UI. (Registration is not currently available on the CLI)

`-h` command argument can be used in order to know more about the command. 
(Command's required parameters, information about what it does, etc.)

Example:
```
akinoncli user -h
```
In order to start using Akinon CLI, the `base_url` should be set with the following command:
```
akinoncli base-url set {base_url}
```
## Commands

### Authentication
In order to use Akinon CLI, the user must authenticate first.

___
* `akinoncli login` 

Authentication is achieved by submitting e-mail and password.
___
* `akinoncli logout` 

By logging out the previous credentials can be deleted.
___
### Public Keys
In order to access the `ProjectApp`'s repositories, public keys are required.

___
* `akinoncli publickey create {key}`

Creates public key.


| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| key      | the text inside .ssh/id_rsa.pub | Yes |

**Example**

`akinoncli publickey create "ssh-rsa AAAAB..."`
___
*  `akinoncli publickey list`

Lists the public keys.
___

* `akinoncli publickey delete {ID}`

Deletes the public key.


| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| ID      | Public Key ID | Yes |


### Applications
Users can create their own application and publish it so other users
can set up for their project and use it.

The application which you'd like to publish needs to be managed by GIT version control system.
In order to have read/write access to application's repository, the application needed to be
created in the Akinon Cloud Commerce and a public key must be created.

For an application to be distributed and compiled by the Akinon Cloud Commerce, it needed to have 
a file named `akinon.json` in its home directory.


**TODO: add the link to documentation of akinon.json**
___
*  `akinoncli applicationtype list`

Lists the application types.

___
*  `akinoncli application create {name} {slug} {application_type_id}`

Creates an application.

| Parameter            | Description  | Required     |
| -------------------- | ------------ | ----------- |
| name                 | Application Name | Yes |
| slug                 | Application Slug (must be unique) | Yes |
| application_type_id  | Application Type ID (akinoncli applicationtype list) | Yes |

To see the git address you should run the `list` after creation of the application. 
It can be seen as `Clone URL` column.

___
*  `akinoncli application list`

Lists the applications.
___

In order to upload the source code of application run the following commands:
```
$ git remote add akinon {CLONE_URL}
$ git push akinon {branch_name}
```

In order to deploy an application for a project, it needs to be built by Akinon Cloud
Commerce. A stable version is required for such an action. One can create a tag 
using `git tag` commands. After that, the tag needs to be pushed to the 
remote repository in the Akinon Cloud Commerce system.

**Example**
```
$ git tag 1.0
$ git push akinon --tags
```

The building process can be started by CLI when the tag is pushed.
___

*  `akinoncli application build {app_id} {tag}`

Starts the building process for the given tag.

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| app_id      | Application ID | Yes |
| tag         | Tag | Yes |


**Example**
```
$ akinoncli application build 1 1.0
```

___
*  `akinoncli application versions {app_id}`

Lists the built versions of the application.

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| app_id      | Application ID | Yes |


The status of version being `completed` indicates that the version is ready for deployment.

___

### Projects

The projects are the ecosystem of applications working together and integrated. When a project is created
`Omnitron` application is automatically being added to project and starts running.

___
*  `akinoncli project list`
Lists the projects.
___

*  `akinoncli project create {name} {slug}`

Creates project.

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| name      | Project Name | Yes |
| slug      | Project Slug (Must be unique.) | Yes |

### Project Applications
The applications cannot be run without a project in the Akinon Cloud Commerce.
They should be related to a project and that relation can be assured with the
creation of a `ProjectApp`.

___
*  `akinoncli projectapp add {project_id} {app_id}`

Adds the application to project by creating `ProjectApp`.

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| project_id      | Project ID | Yes |
| app_id      | App ID | Yes |

*  `akinoncli projectapp list {project_id}`

Lists the applications of the relevant project.

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| project_id      | Project ID | Yes |

**Environment Parameters**

The applications are able to run with different configurations on the various projects.
The same application running with different default language on two different projects can be given as example.
For this kind of requirements, Environment Parameters can be used. 
These parameters could be seen in the `ENV Variables` column when listing the applications.

___
*  `akinoncli projectapp add-env {project_id} {project_app_id} {ENV_KEY}={ENV_VALUE} {ANOTHER_ENV_KEY}={ANOTHER_ENV_VALUE}`

Adds the environment parameter on the application.

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| project_id      | Project ID | Yes |
| project_app_id      | Application ID | Yes |
| ENV_KEY      | The key of relevant environment parameter | Yes |
| ENV_VALUE      | The value of relevant environment parameter | Yes |
| --deploy      | Redeploy the current version to activate environment variable changes. | No |

The same command can also be used for updating.

**Example**
```
$ akinoncli projectapp add-env 1 32 LANGUAGE_CODE=en-us
```

It's also possible to use complex (i.e. non-string) values by encoding them as JSON. The value must be quoted properly
to function correctly. 

```
$ akinoncli projectapp add-env 1 32 MIDDLEWARE='["my.custom.MiddlewareClass", "django.middleware.security.SecurityMiddleware", "whitenoise.middleware.WhiteNoiseMiddleware", "django.contrib.sessions.middleware.SessionMiddleware"]'
$ akinoncli projectapp add-env 1 32 THUMBNAIL_OPTIONS='{"product-list": {"width": 273, "height": 210}, "product-detail__slider_zoom": {"quality": 90}}'
```

For larger or dynamic payloads you can use `EOF` operator in `sh`-based terminals. This also allows string interpolation without having to escape 
double quotes.

```shell
img_quality=90
opts=$(cat <<EOF
{
  "product-list": {
    "width": 273, 
    "height": 210,
    "quality": $img_quality
  }, 
  "product-detail__slider_zoom": {
    "quality": $img_quality
  }
}
EOF
)

akinoncli projectapp add-env 1 32 THUMBNAIL_OPTIONS="$opts"
```

This environment variable can then be deserialized using `django-environ` package, or `json.loads`:

```python
from environ import Env

env = Env()

DEFAULT_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]
MIDDLEWARE = env.json('MIDDLEWARE', default=DEFAULT_MIDDLEWARE)  # omit `default` to throw an error if it's not set

THUMBNAIL_OPTIONS = env.json('THUMBNAIL_OPTIONS')  # throws error if THUMBNAIL_OPTIONS is not set

# print(MIDDLEWARE[0])  # prints "my.custom.MiddlewareClass"
# print(list(THUMBNAIL_OPTIONS))  # prints ["product-list", "product-detail__slider_zoom"]
```

Refer to [`django-environ` documentation](django-environ.readthedocs.io/) for further information.
___

___

*  `akinoncli projectapp remove-env {project_id} {app_id} {ENV_KEY} {ANOTHER_ENV_KEY}`

Deletes the environment parameter from the application.

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| project_id      | Project ID | Yes |
| project_app_id      | Application ID | Yes |
| ENV_KEY      | The key of relevant environment parameter | Yes |
| --deploy      | Redeploy the current version to activate environment variable changes. | No |

**Deploying the Application**

In order to deploy an application it needed to be built firstly. 
(Those steps are explained in Applications section.)

___
*  `akinoncli projectapp deploy {project_id} {project_app_id} {tag}`

Deploys the relevant tag to the relevant project application. (That process 
might take some time.)  


| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| project_id      | Project ID | Yes |
| project_app_id      | Application ID | Yes |
| tag      | Tag of the version | Yes |

*  `akinoncli projectapp deployments list {project_id} {app_id}`

Lists the deployments of the relevant application. 
The status of deployment can be seen in the `status` column.

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| project_id      | Project ID | Yes |
| project_app_id      | Application ID | Yes |

**Application Log**

The applications logs can be seen following commands.
Limit, offset, process type parameters are optional.
___
*  `akinoncli projectapp logs {project_id} {project_app_id}`

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| project_id      | Project ID | Yes |
| project_app_id      | Application ID | Yes |
| -o      | Offset (seconds) (10 by default)| No |
| -l      | Limit (seconds) (5 by default) | No |
| -p      | Process type (If that parameter is passed the relevant process typed logs would be returned) (By default returns logs with any process types ) | No |

**Example**
The following command returns the logs created from 10 seconds ago to 15 seconds ago by default.

*  `akinoncli projectapp logs 1 1`

The following command returns the logs created from 5 seconds ago to 25 seconds ago.
*  `akinoncli projectapp logs 1 1 -o 5 -l 20`

The following command returns the logs created from 15 seconds ago to 30 seconds ago.
*  `akinoncli projectapp logs 1 1 -o 15 -l 15 -p web`


**Exporting Application Logs**

The application logs can be exported with following commands.
___

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| project_id      | Project ID | Yes |
| app_id      | Application ID | Yes |
| -d      | Filters logs that were created on the specified dates. Dates must be separated by commas. Date format must be YYYY-MM-DD.  | No |
| -s      | Filters logs that were created after the given specified date. Date format must be YYYY-MM-DD. | No |
| -e      | Filters logs that were created before the given specified date. Date format must be YYYY-MM-DD. | No |
| -p      | Process type (If that parameter is passed the relevant process typed logs would be returned) (By default returns logs with any process types ) | No |

**Example**

The following command exports all the logs of the given application.
* `akinoncli projectapp export-logs 1 1`

The following command exports all the logs of the given application which were created in 2021-09-23 and 2021-09-24 dates.*  
`akinoncli projectapp export-logs 1 1 -d 2021-09-23,2021-09-24`

The following command exports all the logs of the given application which were created with web and beat process types.
*  `akinoncli projectapp export-logs 1 1 -p web,beat`

The following command exports all the logs of the given application which were created between 2021-09-23 and 2021-09-28 dates.
*  `akinoncli projectapp export-logs 1 1 -s 2021-09-23 -e 2021-09-28`

___
**Attaching certificate to Project Application**

In order to deploy an application with certain domain and ssl certificate, that command can be used.
One certificate can only be attached to one Project Application.

___
Attaches certificate to Project Application.

*  `akinoncli projectapp attach-certificate {project_id} {project_app_id} {certificate_id}`


| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| project_id      | Project ID | Yes |
| project_app_id      | Application ID | Yes |
| certificate_id      | Certificate ID | Yes |

**Example**
```
$ akinoncli projectapp attach-certificate 1 1 1
```
___
Detaches the certificate from Project Application.

*  `akinoncli projectapp detach-certificate {project_id} {project_app_id}`

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| project_id      | Project ID | Yes |
| project_app_id      | Application ID | Yes |


**Example**
```
$ akinoncli projectapp detach-certificate 1 1
```
___

### Domain and Certificate
Akinon Cloud Commerce sistemine bir uygulamayı dağıtıma çıkarırken uygulamanın ssl sertifikası ile belirli bir alan adı ile çalışmasını istediğimiz durumlarda alan adı ve sertifika oluşturarak oluşturulan sertifikayı proje uygulamasına bağlayabiliriz.

**Domain**
___
Lists the domains.
*  `akinoncli domain list`
___

Creates domain.
*  `akinoncli domain create {hostname} {is_managed}`

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| hostname        | Hostname | Yes |
| is_managed      | Alan adının akinon cloud tarafından yönetilmesini belirtir. (true, false değerlerinden biri olmalıdır) | Yes     |

**Example**
```
$ akinoncli domain create akinoncloud.net true
```

**Certificate**
___
Lists the certificates of the relevant domain.

*  `akinoncli certificate list {domain_id}`
___

Creates a certificate.

*  `akinoncli certificate create {domain_id} {fqdn}` 

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| domain_id      | Domain ID | Yes |
| fqdn           | Fully Qualified Domain Name | Yes |

**Example**
```
$ akinoncli certificate create 1 test.akinoncloud.net
```


### Addons
Addons are the third-party technologies such as Redis, Sentry, PostgreSQL etc.

___
Lists the addons.
*  `akinoncli addon list {project_id} {project_app_id}`
___

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| project_id        | Project ID | Yes |
| project_app_id      | Project Application ID | Yes |

**Example**
```
$ akinoncli addon list 1 1
```


### Kube Metric Monitor

CPU and memory metrics of the applications running in the relevant Kubernetes cluster and namespace
can be seen with the following command.

___
Lists the metrics.
*  `akinoncli addon list {project_id} {project_app_id}`
___

| Parameter      | Description | Required |
| ----------- | ----------- | ----------- |
| cluster        | Cluster Name | Yes |
| namespace      | Namespace | Yes |

**Example**
```
$ akinoncli metrics list cluster1 namespace1
```
