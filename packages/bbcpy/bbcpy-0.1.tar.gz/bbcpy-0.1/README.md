# BBCpy Readme

## Development

This project defines specific requirement versions. To minimize version conflicts with already installed libraries you should either set up a virtual environment or use a docker container for development.

In case your installed `python --version` differs from the required 3.8 the docker approach may be appropriate.

### Virtual Environment

Python 3 supports virtual environments natively with the [venv module](https://docs.python.org/3/tutorial/venv.html).

The following commands create the virtual environment `.venv` and install all dependencies defined in `requirements.txt`. The virtual environment needs to be active in the terminal you work with. Use `source .venv/bin/activate` to activate it in the bash shell or `.venv\Scripts\activate.bat` on windows. More information can be found [here](https://docs.python.org/3/tutorial/venv.html).

*Note: `python` may refer to version 2 on your system, in that case use `python3` in the commands instead.*

Example for Linux with bash shell:
```sh
# create virtual environment "venv"
python -m venv .venv
# activate environment
source .venv/bin/activate
# install dependencies
pip install -r requirements.txt
```

In case you use an IDE (like PyCharm) you might need to configure it to use the virtual environment as-well.

### Docker

The docker container contains python 3.8 and all dependencies from the `requirements.txt` at the time of building and is based on a modern ubuntu image.  
To download from or publish to the container registry you need to log in first with your tu gitlab account. In case you have 2FA enabled you need to use a [personal access token](https://git.tu-berlin.de/help/user/profile/personal_access_tokens.md) instead of your password. The scopes `read_registry` and `write_registry` should suffice.

The following command creates and starts the container named `bci-dev` and mounts the current directory inside.

```sh
# login if you have not already
docker login git.tu-berlin.de:5000
# run container and access it's terminal
docker run -it --name bci-dev -v "$(pwd)":/home git.tu-berlin.de:5000/roydick1.0/bcifntd2020ws:dev
```

You can work and edit files normally and may test and execute from the command line within the container.  
The python executable is `python3`.

If you need other dependencies you can simply use `apt` or `pip` to install them inside the container or edit the `requirements.txt` and build your own image with the `Dockerfile`.
