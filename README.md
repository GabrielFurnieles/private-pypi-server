# Private PyPI Server

This repository contains a private PyPI server that can be used to host and distribute Python packages.
The server is hosted in a docker container and can be started by running `docker compose up` (follow installation steps below).

In addition, the repository contains four packages built with both [Poetry](https://python-poetry.org/) `poetry/` and  [uv](https://docs.astral.sh/uv/) `uv/` for testing purposes of chained explicit dependencies (see [link-to-Medium](#)).

## Installation

### Prerequisites
- Docker - [Linux](https://www.docker.com/get-started), [Windows](https://docs.docker.com/desktop/setup/install/windows-install/), [MacOS](https://docs.docker.com/desktop/install/mac-install/)
- [Docker Compose](https://docs.docker.com/compose/install/)


### Running the PyPI Server
1. Generate username and password using `htpasswd` [^1]
    ```
    htpasswd -c auth/.htpasswd [username]
    ```

2. Start the PyPI server by running `docker compose up` (make sure no other containers are running on port 8080)

3. Check that the PyPI server is running by navigating to `http://localhost:8080` in your browser.


[^1]: If you don't want to generate credentials remove lines 7-9 (included) and 13 from `docker.compose.yaml`


> [!NOTE]
> To completely remove the PyPI server run `docker compose down -v` (-v flag removes volumes)


> [!TIP]
> To remove a package from the PyPI server run:
> ```
> curl --form ":action=remove_pkg" --form "name=[package-name]" --form "version=[package-version]" http://[username]:[password]@localhost:8080/
> ```


## Testing Poetry vs uv

> [!NOTE]
> The following commands are run using **Ubuntu 22.04** and might change in other systems.

### Prerequisites
- [Poetry](https://python-poetry.org/docs/#installation)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Setup

#### Add PyPI Server credentials to Poetry

```bash
poetry config repositories.[repo-name] http://localhost:8080
poetry config http-basic.[repo-name] [username] [password]
```

Where `[repo-name]` is the name of the repository you want to add (in the packages is added as `private-pypi` so if you want to use another name make sure to change it in the `pyproject.toml` file before continuing) and `[username]` and `[password]` are the credentials for the PyPI server.

#### Add PyPI Server credentials to uv

```bash
export UV_INDEX_[REPO_NAME]_USERNAME=[username]
export UV_INDEX_[REPO_NAME]_PASSWORD=[password]
```

In case you want to preserve these credentials between different console sessions, add these lines at the end of the file `~/.bashrc`.\
Again, make sure REPO_NAME matches the one defined in the `pyrpoject.toml` (currently set as `PRIVATE_PYPI`)

#### Runing Setup

Publishes package `p1` and `p2` to the PyPI server

```bash
bash setup.sh
```

#### Testing with Poetry

```bash
cd poetry/pkg_p3

poetry shell
poetry add p2 --source private-pypi
```

Raises error:

```
Because no versions of p2 match >0.1.0,<0.2.0
and p2 (0.1.0) depends on p1 (>=0.1.0,<0.2.0), p2 (>=0.1.0,<0.2.0) requires p1 (>=0.1.0,<0.2.0).
So, because no versions of p1 match >=0.1.0,<0.2.0
and p3 depends on p2 (^0.1.0), version solving failed.
```

#### Testing with uv

```bash
cd uv/pkg_uv3

uv add p2 --index private-pypi=http://localhost:8080
uv sync
```

No errors are raised. Test it running:

```bash
uv run uv3/module3.py
```

Expected output:

```
Hello, P1!
Hello, P1!
Hello, P2!
Hello, UV3!
```
