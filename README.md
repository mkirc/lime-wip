# lime wip

## setup devcontainer

```bash
cd tools/devcontainer
docker compose build
```
builds an image 'lime-dev' for dependency isolation

## running lime

* directly:

`docker run -it -v ./lime-1.9.5:/lime -v [PATH TO MODEL]:/model lime-dev lime-run`

* use one of the test setups:

`bash outFilesTest.bash`

