# pdf2text - extract the text from a set of pdf files in a directory

The pdf2text cli allows you to automatically extract the text from a set of pdf files in a directory. A dockerfile is provided which allows you to build a docker image which has pdfalto preinstalled.

## Using the docker image

### 1. Add ssh private key to agent
First, add your ssh private key to the ssh agent:

`ssh-add`

### 2. Building the docker image
When building the docker image, you must make sure that Docker is configured to use the new [BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/). This is to enable you to use [ssh to clone the pdfalto git repo](https://docs.docker.com/develop/develop-images/build_enhancements/#using-ssh-to-access-private-data-in-builds).


`DOCKER_BUILDKIT=1 docker build --ssh default -t navigator_pipeline .`

### 3. Running the cli
Use the following command to run the pdf2text cli:

```
docker run -v /path/to/pdf/files:/pdf-in -v /path/to/output/directory:/pdf-out \
navigator_pipeline python /app/pdf2text.py /pdf-in /pdf-out --json --text
```

where:

- `/path/to/pdf/files` - is the path to the directory containing the pdf files to process
- `/path/to/output/directory` - is the path to the directory where the output files should be stored

### Output files
Output files produced by the process will be placed in the output directory. 1-2 files per pdf file will be generated depending on the following arguments passed to the cli:

- `--json` - generates a .json file containing extracted text blocks and positional information
- `--text` - generates a .txt file containing extracted text

The name of each .json and .txt file generated will be set to the corresponding pdf filename.

e.g. `pdf-input-file.pdf` will produce the following 2 files in the output directory once processed:

- `pdf-input-file.json`
- `pdf-input-file.txt`