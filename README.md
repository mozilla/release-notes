# Mozilla Release Notes

Release notes and system requirements for Mozilla products in JSON format.

## Usage

To update the data in this repo you can run a simple script which will pull the data from an instance of [Nucleus][]
and populate the JSON files in the `releases` folder. After following one of the update procedures below you can commit
and push the changes to the JSON files if you need to manually update the release notes data on the website.

### Docker

This is the recommended way to do it since it requires no steps other than having [Docker][] installed. Simply run the following commands:

```bash
./update_docker.sh
```

This will build the docker image and run it to update the local JSON files.

### Local Python

You'll need Python 3.11 or above and [virtualenv][] to run the following steps.

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
./update_releases.py
```

[Nucleus]: https://nucleus.mozilla.org
[Docker]: https://www.docker.com/community-edition
[virtualenv]: https://virtualenv.pypa.io/en/stable/

## License

Mozilla Public License v2. See [LICENSE](LICENSE) file for details.
