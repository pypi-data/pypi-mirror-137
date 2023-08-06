# ML & data helper code!
Jakub Langr (c) 2021

This is a CLI utility for speeding up basic Data Engineering/Data Science tasks

## Installation

```
$ pip install data-toolkit
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run dt cli application

$ dt --help


### run pytest / coverage

$ make test
```


## TODO: Central Data Repository

As a PM, I want to be able to quickly look at all the data we have on S3 with sample images.

    * Needs a DB
    * Needs a way of sampling