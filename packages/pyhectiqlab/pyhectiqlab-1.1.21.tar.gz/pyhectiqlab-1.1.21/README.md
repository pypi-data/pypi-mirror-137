# Contents 

<!-- MarkdownTOC -->

- [Tutorials](#tutorials)
	- [Quickstart](#quickstart)
	- [Metrics](#metrics)
	- [Save artifacts](#save-artifacts)
		- [Classical run artifacts](#classical-run-artifacts)
		- [Step artifacts](#step-artifacts)
		- [Shared artifacts](#shared-artifacts)
		- [Special artifacts](#special-artifacts)
	- [MLModel and Datasets](#mlmodel-and-datasets)
		- [Upload](#upload)
		- [Download](#download)
	- [Config](#config)
		- [Push a config](#push-a-config)
	- [Package versions](#package-versions)
	- [External git repos](#external-git-repos)
	- [States](#states)
	- [Logs](#logs)
	- [Others](#others)
	- [Tags](#tags)
- [Shell](#shell)
	- [Login/Add a profile](#loginadd-a-profile)
	- [List the projects](#list-the-projects)
	- [Download shared artifacts](#download-shared-artifacts)
	- [Push a shared artifacts](#push-a-shared-artifacts)
	- [Custom env variables](#custom-env-variables)
- [FAQ](#faq)
	- [Is it fast?](#is-it-fast)
	- [Will I be alerted if the lab is unavailable?](#will-i-be-alerted-if-the-lab-is-unavailable)
	- [What is the dry mode?](#what-is-the-dry-mode)

<!-- /MarkdownTOC -->

# Tutorials

## Quickstart
Login with your username and password
```
hectiqlab add-profile
```
A secret API key will be generated and stored in `~/.hectiqlab/credentials`. If you have multiple profiles, you can switch profiles with the env var `HECTIQLAB_PROFILE`.

In a python script or jupyter notebook, create a run:
```python
from pyhectiqlab.run import Run

run = Run(name="dev-run")
```
If the name doesn't already exist, it will be created. If a run already exists, the data will be pushed in the existing run. However, if you attach to an existing run that you are not the original author, the run will be in read-only mode.

## Metrics
The metrics of a run are pushed async (no latency). We have included an internal aggregator so that you don't overflow the server with metrics. You can setup the parameters of the metrics cache using `run.set_metrics_cache_settings`.

```python
# Push a metrics
run.add_metrics(key='train/loss', value=0.982, step=10)
```

## Save artifacts
You can save files using three approaches.

### Classical run artifacts

A run artifact is a file attached to a run. It can be any type of file. Please do not use this to store large datasets (>1Gb).

```python
# Run artifact. Overwrite if a file with the same name exists
run.add_artifact(path_to_artifact)
```

The artifact is now available in the web app in the artifact tab of the run. The web app let you download the artifact, and copy a code snippet to download the artifact with the python client. Also, images (extension .png, .jpg, .jpeg) can be visualized in the web app.

> The upload does not yet support streaming mode. Hence, there is no progress bar to see how the upload goes.

### Step artifacts
A step artifact is a method to group similar artifacts that are generated at certain steps during a process. 

```python
step = 5 # example is an integer
# Overwrite if an artifact with this name at this step exists
run.add_artifact(path_to_artifact, step=step) 
```
The name of the group of the basename of the path to the artifacts. For instance, `(./data/test.png, step=0)` and `(./data2/test.png, step=1)`  will be grouped under `test.png`. 

### Shared artifacts
A shared artifact is a file that is attached to the project, instead of the run. 

```python
# Overwrite if a file with the same name exists
run.add_shared_artifact(path_to_artifact)
```

### Special artifacts
You have access to certain helpers for saving complex files

```python
# Compress a directory into zip and save it as an artifact
run.add_directory_as_zip_artifact(dirpath) # You can add the step argument for step artifacts

# Add a tensor flow model. It will run save_weights
run.add_tf_model_as_artifact(model, filename) # You can add the step argument for step artifacts

# Add your notebook if the code is run from a notebook
run.add_current_notebook()
```
## MLModel and Datasets

### Upload
You can push project models and datasets
```python
run.add_mlmodel('./path/to/model/', 
	name='test-model', 
	version='1.0.0', 
	short_description='A VGG11 trained on ImageNet.')

run.add_dataset('./path/to/dataset/', 
	name='train-imagenet', 
	version='1.0.0', 
	short_description='The train images of ImageNet')
```

### Download
There is multiple methods to download mlmodels and datasets (shell, etc.), check the web app to get snippets for a specific mlmodel/dataset.

```python
run.download_mlmodel(name='test-model', 
	version='1.0.0', 
	save_path="./")

run.download_dataset(name='train-imagenet', 
	version='1.0.0', 
	save_path="./")
```

## Config
To store the config parameters, use the Config object. You may use it just like a dictionary and it can be nested.

```python
from pyhectiqlab import Config
nested_config = Config(path='./here', b=1)
config = Config(hello='world', a= nested_config)

# Use the nested values
config.a.path # './here'

# Use as a dict
model(**config.a)
```

### Push a config
Configs should be pushed using the designated method. If you already pushed a config for this run, the server will update the config file. Hence, it will add the unseen elements. 
```python
run.add_config(config)
```

## Package versions
You can store the versions of all the packages loaded in the kernel. It will also save the machine setup and the git commit if your script is part of a repo.

```python
import torch
import numpy as np
run.add_package_versions(globals())
```

## External git repos
If you code use a package part of a git repo (context-segments for instance), you can ask the lab to store the state of the repo.

```python
run.add_package_repo_state('voxnet')

# It will check if voxnet.__path__ is in a git repo. If so, the commit/branch/source is stored.
```

## States

```python
run.completed()
run.failed()
run.completed()
run.pending()
run.running()
run.training()
```

## Logs

```python
logger = run.start_recording_logs()
logger.info('test')
logger.stop_recording_logs()
logger.critical('This will not be logged.')
run.start_recording_logs()
logger.info('This will be logged.')

# Check a specify channel. It will log everything that goes through torch.
logger = run.start_recording_logs('torch')

# To log: "Progress ----------"
logger.info("Progress \r")
for i in range(10):
    logger.info("-\r")
```
Finish your log with `\r` to cancel the line break.

## Others

```python
run.set_note('This is a short description that will be featured on the tab General of the run.')
run.add_meta(key='hello', value='world')
```

## Tags
Usually, we add tags using the web client but you can do it with the python client as well.

```python
# You can specify the colour (hex)
# If a tag with this name exists, it will simply attach it to the run 
run.add_tag(name='Train', description=None, color=None)
```

# Shell

## Login/Add a profile
```
hectiqlab add-profile
```

## List the projects
List the projects name and ids.
```
hectiqlab projects
```

## Download shared artifacts
Download a shared artifact.
```
hectiqlab artifacts [project_Id]
```

## Push a shared artifacts
Push a file into a shared artifacts of a project.
```
hectiqlab post_artifact [project_Id] [filename]
```

## Custom env variables

`HECTIQLAB_CREDENTIALS`: Path to the credentials file
`HECTIQLAB_PROFILE`: Name of the profile to connect with

# FAQ
## Is it fast?

Yes, the python client is fully async so it won't slow down your runs. Every call to the lab is made on a separate thread. Hence, you won't always be alerted if something doesn't reach the server.

The metrics and the logs are managed by buffer objects. The buffer is cleared (by sending the information to the lab) when its limit is reached or after a time interval, and at deletion.

## Will I be alerted if the lab is unavailable?

The run initialization (`run = Run(...)`) waits for the server confirmation. If the server is down, an error will be printed and you'll be switched to a dry mode. All the other calls (`add_metrics`, etc.) are fully async and don't wait for the server's response. For example, if the `add_metrics` fails, you will not be alerted. This is because we don't want your run to stop because the hectiqlab is broken.

## What is the dry mode?

The dry mode consists is a layer that prevents your code to crash if the hectiqlab is down. Hence, if the dry mode (or read only mode) is activated, you can call all run methods (`run.add_metrics`) without errors but the data won't be pushed.
