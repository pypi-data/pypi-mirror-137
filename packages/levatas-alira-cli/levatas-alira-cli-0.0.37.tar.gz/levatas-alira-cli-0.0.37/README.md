# Alira Command Line Interface

## Table of Contents

-   [Prerequisites](#prerequisites)
-   [Application configuration](#application-configuration)
-   [License structure](#license-structure)
-   Supported commands
    -   [`alr setup` — Installing the application](#alr-setup--installing-the-application)
    -   [`alr start` — Starting the application](#alr-start--starting-the-application)
    -   [`alr stop` — Stopping the application](#alr-stop--stopping-the-application)
    -   [`alr restart` — Restarting the application](#alr-restart--restarting-the-application)
    -   [`alr upgrade` — Upgrading the application](#alr-upgrade--upgrading-the-application)
    -   [`alr remove` — Removing the application](#alr-remove--removing-the-application)
    -   [`alr status` — Displaying the application status](#alr-status--displaying-the-application-status)
    -   [`alr save` — Saving the application packages](#alr-save--saving-the-application-packages)
    -   [`alr --version` — Displaying version information](#alr--version--displaying-version-information)
    -   [`alr help` — Displaying help information](#alr-help--displaying-help-information)
-   [What's New](WHATSNEW.md)

## Prerequisites

The following is the list of prerequisites that you need on the host computer:

-   Python 3.8
-   Docker

## Installation

Create a virtual environment and install the library:

```shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install --user levatas-alira-cli
```

You can then run the CLI to make sure everything is working:

```shell
$ alr
```

## Application configuration

To run the command line interface, we need to specify the location of the folder in the host computer that stores the configuration of the application. This folder will contain the following structure:

-   `license.pem` A valid application's license.
-   `public.pem` The public key that will be used to decrypt the license certificate.
-   A folder for each one of the packages that will be installed as part of the application.

The command line interface assumes that the local folder from where it runs is the configuration folder. If you want to tun the command line interface from a different location, use the `--volume` parameter to specify the location of the folder. For example:

```shell
$ alr --volume /home/spot/levatas status
```

The above command will display the status of the installation using the `/home/spot/levatas` as the folder hosting the configuration.

### Using an environment variable

You can also configure the location of the configuration folder using an environment variable. For example, if you want to use the `/home/spot/levatas` folder as the configuration folder, you can set the `ALIRA_VOLUME` environment variable to `/home/spot/levatas`:

```shell
$ export ALIRA_VOLUME=/home/spot/levatas
$ alr status
```

## License structure

The license contains a metadata section with the following structure:

```json
{
    "GITHUB_REPOSITORY_ACCESS_USER": "username",
    "GITHUB_REPOSITORY_ACCESS_TOKEN": "access-token",

    "PACKAGES": [
        {
            "name": "model-container-1",
            "image": "ghcr.io/vinsa-ai/model-container-1:latest",
            "model": "people-detection",
            "binding": true
        },
        {
            "name": "model-container-2",
            "image": "ghcr.io/vinsa-ai/model-container-2:latest",
            "model": "clip",
            "volumes": "$volume:/opt/ml/volume, $model:/opt/ml/model",
            "binding": true
        },
        {
            "name": "redis",
            "image": "redis:6.2.6",
            "binding": false
        }
    ]
}
```

-   `GITHUB_REPOSITORY_ACCESS_USER`: A valid GitHub username with access to download containers published as packages.
-   `GITHUB_REPOSITORY_ACCESS_TOKEN`: The access token related to GitHub username.

### Packages

The license specifies the list of containers that will be installed under the `PACKAGES` section. Here are the attributes supported:

-   `name`: This is the name of the container. This will be the name that will be used to identify the container from the command line interface.
-   `image`: This is the Docker image that will be downloaded to run the container.
-   `model`: This is the identifier of the model. Models will use this identifier to refer to its model-specific configuration folder. This attribute should only be specified for those containers that are bound to a model.
-   `volumes`: A comma-separated list of volumes to mount. If this attribute is not present, the installer will automatically mount the configuration folder to the `/opt/ml/model` path in the container. If this attribute is present, the configuration folder will not be automatically mounted. To reference the configuration folder, you can use the `$volume` variable. To reference the model-specific configuration folder, you can use the `$model` variable. For example: `$volume:/opt/ml/volume, $model:/opt/ml/model`.
-   `binding`: This is a boolean value that specifies whether we want to do a port binding with an auto-generated port (21000, 21001, etc.) If not present, the installer will try to map the exposed port numbers to the same ports on the host.

## Supported commands

### `alr setup` — Installing the application

You can install the solution using the `setup` command. The installation process uses the list of authorized packages in the license file.

This command will only download and install the packages that are not already installed. To upgrade a package that's already installed, use the `upgrade` command.

#### Usage

```shell
$ alr setup
```

#### Options

| Name, shorthand  | Default | Description                                                             |
| :--------------- | :------ | :---------------------------------------------------------------------- |
| `--folder`, `-f` |         | Specify the folder containing the docker images that will be installed. |

#### Offline installation

By default, the installation process downloads the required containers before installing them. To install the containers without an Internet connection, you can use the `--folder` argument to specify the location of the corresponding docker images:

```shell
$ alr --volume /home/spot/levatas setup --folder /home/spot/docker-images
```

The file name of each image in this folder should match the name of the container specified in the license file. For example, if the license file specifies the `model-container-1` container, the corresponding image should be named `model-container-1.tar`.

### `alr start` — Starting the application

To run the application, you can use the `start` command. This starts all of the components of the application.

#### Usage

```shell
$ alr start
```

#### Options

| Name, shorthand  | Default | Description                                                                                  |
| :--------------- | :------ | :------------------------------------------------------------------------------------------- |
| `--port`, `-p`   | `21000` | Specify the starting port number to automatically map all exposed ports.                     |
| `--local`        |         | Specify whether cloud synchronization will be disabled.                                      |
| `--docker`, `-d` |         | Specify a set of arguments that will be used with `docker run` to run individual containers. |

#### Port mapping

Each component exposes a list of port numbers that should be mapped with the host. By default, the application maps each port to a consecutive number starting with port `21000`.

You can use the `--port` argument to change the initial port that will be mapped.

For example, assume there are two components installed by the application. Here is the list of port numbers exposed by each one of them:

-   Component1: `5000`, `8080`, `8081`
-   Component2: `80`, `1234`

When starting the solution, each port will mapped the following way:

-   Component1: `21000:5000`, `21001:8080`, `21002:8081`
-   Component2: `21003:80`, `21004:1234`

To change the initial port number that will be used for the mapping, you can use the `--port` argument:

```shell
$ alr start --port 9000
```

In this case, these will be the resulting mappings:

-   Component1: `9000:5000`, `9001:8080`, `9002:8081`
-   Component2: `9003:80`, `9004:1234`

For the automatic port mapping to work, each component has to expose all of their port numbers using the docker [`EXPOSE`](https://docs.docker.com/engine/reference/builder/#expose) instruction. You can inspect an individual container to make sure all of the necessary ports are properly exposed using the following command:

```shell
$ docker inspect --format='{{.Config.ExposedPorts}}' container:latest
```

#### Cloud synchronization

The application includes a `Redis` server to synchronize the communication with remote endpoints.

You can run the solution without cloud integration using the `--local` argument. This will disable the `Redis` server and the synchronization process to avoid them using any processing bandwith.

```shell
$ alr start --local
```

#### Arbitrary arguments

When running the application, we might find cases where we need to run a specific component in a different way as it was designed. For example, we might need to map a host device with the container to test something specific. These cases should be rare, but they could happen.

You can use the `--docker` argument to pass arbitrary arguments to the `docker run` command used to start each component.

Here is an example on how to start the solution by specifying an additional volume mapping for the `component1` container:

```shell
$ alr start --docker "component1 -v /home/spot/folder:/opt/alira/folder"
```

You can specify arbitrary arguments for more than one container by using the `--docker` argument multiple times:

```shell
$ alr start \
    --docker "component1 -v /home/spot/folder:/opt/alira/folder" \
    --docker "component3 --expose 5001"
```

### `alr stop` — Stopping the application

To stop the application, you can use the `stop` command. This stops all the running components of the application.

#### Usage

```shell
$ alr stop
```

### `alr restart` — Restarting the application

To restart the application, you can use the `restart` command. This stops all the running components of the application and then starts them.

#### Usage

```shell
$ alr restart
```

#### Options

For the list of supported options, check [`alr start`](#alr-start--starting-the-application).

### `alr upgrade` — Upgrading the application

To upgrade the application, you can use the `upgrade` command. This process will attempt to download the newest version of all the packages and reinstall them.

You can also upgrade a specific package by specifying its name.

#### Usage

```shell
$ alr upgrade [package-name]
```

#### Options

| Name, shorthand  | Default | Description                                                             |
| :--------------- | :------ | :---------------------------------------------------------------------- |
| `--folder`, `-f` |         | Specify the folder containing the docker images that will be installed. |

#### Offline installation

Just like with the `setup` command, you can use the `--folder` argument to specify the location of the corresponding docker images to perform the installation without access to Internet.

```shell
$ alr upgrade --folder /home/spot/docker-images
```

### `alr remove` — Removing the application

To remove the application, you can use the `remove` command. This uninstalls all the components of the application after the user confirms the operation.

If any of the components of the application is running, the remove process will first stop the component before uninstalling it.

#### Usage

```shell
$ alr remove
```

#### Options

| Name, shorthand  | Default | Description                                                             |
| :--------------- | :------ | :---------------------------------------------------------------------- |
| `--folder`, `-f` |         | Specify the folder containing the docker images that will be installed. |

### `alr status` — Displaying the application status

You can use the `status` command to display the status of every installed package and the expiration date of the license.

#### Usage

```shell
$ alr status
```

### `alr save` — Saving the application packages

You can use the `save` command to save every image specified in the license file as a tar file.

#### Usage

```shell
$ alr save --folder /home/spot/docker-images
```

#### Options

| Name, shorthand  | Default | Description                                                                                                      |
| :--------------- | :------ | :--------------------------------------------------------------------------------------------------------------- |
| `--folder`, `-f` |         | Specify the folder where the images will be saved. If not specified, images will be saved in the current folder. |


### `alr --version` — Displaying version information

You can use the `--version` command to display the current version of the application.

#### Usage

```shell
$ alr --version
```

### `alr help` — Displaying help information

You can use the `help` command to display a quick reference about all the supported commands.

#### Usage

```shell
$ alr help
```

#### Specific help information

You can display help information about a specific command the following way:

```shell
$ alr help start
```
