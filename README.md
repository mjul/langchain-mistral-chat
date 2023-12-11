# langchain-mistral-chat

This is a LangChain application that uses the [Mistral] 7B model running locally.


## Prerequisites
We are using Python 3.11 and Poetry to manage environments, make sure you have both installed.

Make sure you have `poetry.exe` in your path, and use `poetry shell` to open a shell with the environment.

Install dependencies with `poetry install` from the root folder.

## Project Structure

The project was created with `langchain app new .` in the root folder.

## Notes on PyTorch on Windows

Now, if you try to install the PyTorch "wheels" you may note that 
the `triton` dependency is not available for Windows. Apparently that library 
does not have the proper tagging so Poetry does not pick it up 
(you can install it from `pip`). 

There is a workaround for this in the `pyproject.toml` file,
pointing to a specific wheel file for a specific Windows, using a specific wheels package:

```toml
torch = {url = "https://download.pytorch.org/whl/cu118/torch-2.1.1%2Bcu118-cp311-cp311-win_amd64.whl" }
```


Normally you would just use the PyTorch cuda wheels for your specific platform, e.g. pulling
them from the [PyTorch website](https://pytorch.org/get-started/locally/).

```toml
torch = {version = "^2.1.1", source = "pytorch"}
```

Use `poetry show --tree torch` to see the dependency tree.


## Installation

Install the LangChain CLI if you haven't yet

```bash
pip install -U langchain-cli
```

## Adding packages

```bash
# adding packages from 
# https://github.com/langchain-ai/langchain/tree/master/templates
langchain app add $PROJECT_NAME

# adding custom GitHub repo packages
langchain app add --repo $OWNER/$REPO
# or with whole git string (supports other git providers):
# langchain app add git+https://github.com/hwchase17/chain-of-verification

# with a custom api mount point (defaults to `/{package_name}`)
langchain app add $PROJECT_NAME --api_path=/my/custom/path/rag
```

Note: you remove packages by their api path

```bash
langchain app remove my/custom/path/rag
```

## Setup LangSmith (Optional)
LangSmith will help us trace, monitor and debug LangChain applications. 
LangSmith is currently in private beta, you can sign up [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

## Launch LangServe

```bash
langchain serve
```

## Running in Docker

This project folder includes a Dockerfile that allows you to easily build and host your LangServe app.

### Building the Image

To build the image, you simply:

```shell
docker build . -t my-langserve-app
```

If you tag your image with something other than `my-langserve-app`,
note it for use in the next step.

### Running the Image Locally

To run the image, you'll need to include any environment variables
necessary for your application.

In the below example, we inject the `OPENAI_API_KEY` environment
variable with the value set in my local environment
(`$OPENAI_API_KEY`)

We also expose port 8080 with the `-p 8080:8080` option.

```shell
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8080:8080 my-langserve-app
```
