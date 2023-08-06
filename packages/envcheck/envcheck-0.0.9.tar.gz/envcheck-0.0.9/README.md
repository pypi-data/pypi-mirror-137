# envcheck
A small, simple command line utility to check for, compare and merge environment variables between environment files and their .example counterparts

## Install
```
python3 -m pip install envcheck
```

## Use

```
cd dir/to/check
envcheck
```

## What it does
* If you have a file of `env` or `environment` it will be found
* If there's a matching `env.example` or `environment.example` file it will compare the two and give you some help merging them
* Writes a new file, `env.new` or `environment.new`

This tool doesn't update your environment file
Please do for yourself: check the new file and update your existing environment file

## How it compares
* 🔑 👍 List and count the matching variables (matching both variable name and value)
* 🔑 🚨 List and count variables in the environment file but not found at all in the example (maybe stale or maybe the example is bad)
* 🔑 ✅ List and count new variables in the example
* If new variables are in the example you will be prompted to add them to the new environment file, with auto-fillable values from the example
