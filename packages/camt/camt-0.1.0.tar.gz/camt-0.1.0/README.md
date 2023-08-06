# AMT Africa -  compression CLI tool

`camt` is a `CLI` tool built in python to help compress labeled images to exclude images that are not needed in the output.

## Requirements
* Python
* Virtual environment like `venv, virtualenv` 

## How to run

Start by creating the folder that will use as `[name]` in the command bellow
### Command 
```
$ python -m venv env
(env)$ python install -r requirements.tx
(env)$ python -m camt compress --dest-dir [name] --src-dir [path] --format [zip, tar]
```

# Future plans
* Add the ability to upload the zip file to a cloud provider `GCP`

# Contribution
You can contribute by opening an `Issue` or a `Pull request`.
