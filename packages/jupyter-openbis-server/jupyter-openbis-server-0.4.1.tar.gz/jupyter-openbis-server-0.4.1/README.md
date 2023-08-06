# Jupyter openBIS Server

This server is an extension to the Jupyter notebook server and is part of the `jupyter-openbis-extension` and `jupyterlab-openbis` notebook extensions. It uses the `pyBIS` module internally to communicate with openBIS and ommunicates with the notebook extensions via the built-in tornado webserver.

This extension has been successfully tested with Safari 12.0.3, Chrome 72.0 and Firefox 66.0. There is a known incompatibility before Firefox 61.0b13 with Tornado > 6.x (the webserver used by Jupyter). If you encounter such incompatibilities, try to downgrade to Tornado 5.1.1. However, Tornado 5.1.1 will not work with Jupyter Lab 3.

## Install the server extension

The server extension will be automatically installed when you install the Jupyter Notebook Extension (the «classic» Jupyter Notebook):

```
$ pip install --upgrade jupyter-openbis-extension
```

If you need to install or upgrade the server extension alone, you can do so by:

```
$ pip install --upgrade jupyter-openbis-server
```

Make sure your extension is recognised by Jupyter and enabled (your output may vary, but ensure you see the line: `jupyter-openbis-server.main OK`)

```
$ jupyter serverextension list
config dir: /Users/your_username/.pyenv/versions/3.6.9/etc/jupyter
    jupyter-openbis-server.main  enabled 
    - Validating...
      jupyter-openbis-server.main  OK
```

## Create a connection configuration file

When the module is installed, you can create a connection configuration file.

```bash
$ jupyter-openbis-conn --help
Usage: jupyter-openbis [OPTIONS]

  Generate an openBIS connection file for use in Jupyter notebooks.

Options:
  -n, --name TEXT
  -h, --hostname TEXT
  --verfiy / --no-verify
  --https / --no-https
  -u, --username TEXT
  -p, --password TEXT
  -d, --destination [/Users/your_username/.jupyter|/Users/your_username/.pyenv/versions/3.6.9/etc/jupyter|/usr/local/etc/jupyter|/etc/your_username]
                                  [default: /Users/your_username/.jupyter]
  --help                          Show this message and exit.
```

You can start the utility as-is to get prompted for every parameter. Username and password are optional.

````
$ jupyter-openbis-conn
```

## install Jupyter extension manually

In most cases, a simple `pip install --upgrade jupyter-openbis-server` will install the server extension. However, in some cases (e.g. when installing via `pip install -e .`) you need to issue the following command to register the extension:

**In the library path, e.g. etc/jupyter/ 
```
$ jupyter serverextension enable --py jupyter-openbis-server --sys-prefix
```

This will create a file `~/.jupyter/jupyter_notebook_config.json` with the following content:

```
{
  "NotebookApp": {
    "nbserver_extensions": {
      "jupyter-openbis-server.main": true
    }
  }
}
```

## Uninstall Jupyter openBIS Server

Unfortunately, `pip` doesn't automatically clean up the Jupyter configuration when uninstalling. You have to do it yourself:

```
$ jupyter serverextension disable --py jupyter-openbis-server
$ pip uninstall jupyter-openbis-server
```

## Server extension API documentation

### XSRF Token in `POST`, `PUT` and `DELETE` requests

XSRF (or CSRF) stands for Cross-Site-Request-Forgery.

For all **POST**, **PUT** and **DELETE** requests, the following **http headers** must be submitted as http headers:

```
"X-XSRFToken": xsrf_token,
"credentials": "same-origin"
```
The value of the `xsrf_token` is the value of the `_xsrf` cookie which is stored in the users' browser. Without this http header information, the request will fail. All **GET** requests can be established without a special header.

The underlying Tornado-Webserver which handles all requests to the Jupyter serverextension will throw an error if the X-XSRF Token is not present.

### Errors

Errors caused by a `POST`, `PUT` and `DELETE` request will result in a HTTP Status > 300 and an error message:

```
{
	"reason": "Incorrect username or password for openBIS instance"
}
```


### get openBIS connections

**GET `/openbis/conns`**

Returns an array of JSON objects:

```
{
  "status": 200,
  "connections": [
    {
      "name": "openBIS instance",
      "url": "https://openbis.instance.ch",
      "status": "connected",
      "username": "user_name",
      "password": "******",
      "isMounted": false,
      "mountpoint": ""
    }
  ],
  "notebook_dir": "/home/user_name/project_dir"
}
```
* the **`name`** is the name of the connection being used when downloading or uploading dataSets (see below)
* the **`url`** of the openBIS instance
* the values of `status` can be either **connected** or **not connected**
* the **`username`** being used in openBIS
* the **`password`** really only consists of a number of asteriks **\***. If they are passed as such to re-connect to openBIS, the server tries to use the internally saved password instead. The password only lives in memory of the singleuser notebook-server and is not saved persistently.
* **`isMounted`** is either **true** or **false**, depending whether there is a current FUSE/SSHFS mountpoint available which connects to the openBIS dataStore
* `mountpoint` is the path to the mounted openBIS dataStore. It defaults to `$HOME/<openbis hostname>`

### login to an openBIS connection

An openBIS connection that has to be established or has timed out: a new login has to take place.

**PUT `/openbis/conn`**

Body:

```
{
    "username": username,
    "password": password,
    "action": "login",
}
```
The `action` attribute defaults to `login`. Returns:

```
{
    "status": 200,
    "connection": {
        "name": "openBIS instance",
        "url": "https://openbis.instance.ch",
        "status": "connected",
        "username": "some_username",
        "password": "******",
        "isMounted": false,
        "mountpoint": ""
    }
}
```

### logout

Logs out from an openBIS instance, i.e. the token is invalidated. The mount might still persist, as it is a separate connection. The status changes from **connected** to **not connected**

**PUT `/openbis/conn`**

Body:

```
{
    "action": "logout",
}
```
Returns:

```
{
    "status": 200,
    "connection": {
        "name": "openBIS instance",
        "url": "https://openbis.instance.ch",
        "status": "not connected",
        "username": "some_username",
        "password": "******",
        "isMounted": true,
        "mountpoint": "/Users/some_username/openbis.instance.ch"
    }
}
```

### Mount to an openBIS dataStore

#### Prerequisites
On the Jupyter Server, FUSE/SSHFS must be installed beforehand (requires root privileges). For the actual mount to the openBIS dataStore, no special privileges are required.

For **Mac OS X**, follow the installation instructions on [https://osxfuse.github.io](https://osxfuse.github.io)

For **Unix Cent OS 7**, do the following:

```
$ sudo yum install epel-release
$ sudo yum --enablerepo=epel -y install fuse-sshfs
$ user="$(whoami)"
$ usermod -a -G fuse "$user"
```

**Windows** is currently not supported, sorry!

By default, the mountpoint is the same as the hostname of the instance and it is located inside the home of the user. FUSE/SSHFS needs an empty directory to do this, so it will automatically be created.

**PUT `/openbis/conn`**

Body:

```
{
    "username": username,
    "password": password,
    "action"  : "mount"
}
```
Returns:

```
{
    "status": 200,
    "connection": {
        "name": "openBIS instance",
        "url": "https://openbis.instance.ch",
        "status": "connected",
        "username": "some_username",
        "password": "******",
        "isMounted": true,
        "mountpoint": "/Users/some_username/openbis.instance.ch"
    }
}
```

### Unmount from openBIS dataStore

**PUT `/openbis/conn`**

Body:

```
{
    "action"  : "mount"
}
```
Returns:

```
{
    "status": 200,
    "connection": {
        "name": "openBIS instance",
        "url": "https://openbis.instance.ch",
        "status": "connected",
        "username": "some_username",
        "password": "******",
        "isMounted": false,
        "mountpoint": ""
    }
}
```

### Register a new openBIS connection

For the lifetime (runtime) of the Jupyter server, this will create a connection to openBIS.

**POST `/openbis/conns`**

Body:

```
{
    "name": connection_name,
    "url": connection_url,
    "username": username,
    "password": password
}
```

### Unregister/delete a new openBIS connection

For the lifetime (runtime) of the Jupyter server, this will drop an existing openBIS connection:

**DELETE `/openbis/conn/<connection name>`**


### Upload a dataSet

**POST `/openbis/dataset/<connection_name>/<permId>/<downloadPath>`**


### Download a dataSet

**GET `/openbis/dataset/<connection_name>/<permId>/<downloadPath>`**

* the `connection_name` is the name of the connection given in the connections dialog.
* the `permId` is the identifer of the dataSet that needs to be downloaded.
* the `downloadPath` is the absolute path on the host system where the dataSet files should be downloaded to. The `downloadPath` must be URL-encoded to not to be confused with the URL itself.

In case of a **successful download**, the API returns a JSON like this

```
{
    'url'       : conn.url,
    'permId'    : dataset.permId,
    'path'      : path,
    'dataStore' : dataset.dataStore,
    'location'  : dataset.physicalData.location,
    'size'      : dataset.physicalData.size,
    'files'     : dataset.file_list,
    'statusText': 'Data for DataSet {} was successfully downloaded to: {}'.format(dataset.permId, path)
}
```

In case of an **error**, the API returns one of these errors (HTTP Status > 200):

**general connection error**

```
HTTP-Status: 500
{
	"reason": 'connection to {} could not be established: {}'.format(conn.name, exc)
}
```

**dataSet not found error**

```
HTTP-Status: 404
{
	"reason": 'No such dataSet found: {}'.format(permId)
}
```

**dataSet download error**

```
HTTP-Status: 500
{
	"reason": 'Data for DataSet {} could not be downloaded: {}'.format(permId, exc)
}
```

### Save `requirements.txt` and `runtime.txt` file

Note: The requirements list and the runtime must be evaluated by executing actual Python or R code from wtihin a notebook cell. The Python used by the Jupyter server might differ from the Python used by the kernel. The usual `pip freeze` doesn't work, as we cannot access the pip CLI from within Python.

For the Python `requirements.txt` we use this script:

```
import pkg_resources
print(
	"\n".join(
		["{}=={}".format(i.key, i.version) for i in pkg_resources.working_set]
	)
)
```

For the Python `runtime.txt`:

```
import sys
print('python-' + str(sys.version_info[0]) + '.' + str(sys.version_info[1]))
```

Once submitted to the server, the server will join the relative `notebook_path` (from the UI) with the server-side `notebook_dir`. These files will be stored in the same location on the filesystem as the notebook itself.

**POST `/openbis/requirements`**

Body:

```
{
    "notebook_path": notebook_path,
    "requirements_list": state.requirements_list,
    "requirements_filename": state.requirements_filename,
    "runtime": state.runtime,
    "runtime_filename": state.runtime_filename
}
```
