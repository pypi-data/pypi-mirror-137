# SimWrapper Python Tools

Official python library for working with SimWrapper.

[SimWrapper](https://simwrapper.github.io) is a data visualization tool for exploring large transport simulation results.

## About this library

This library contains the "simwrapper" command-line tool, which allows browsing of local files on your PC/laptop using the SimWrapper website.

We are at the very early stages of building this tool. The API will change, things will break, and there are certainly bugs.

- Our primary goal is to make it easy to get local simulation results viewable using the SimWrapper website.
- We have only tested this using Anaconda Python. Only Python 3.x is supported.

## Installation

Install once, using `pip install simwrapper`

## Usage

`simwrapper` knows two commands:

- `simwrapper serve` starts a local file server in the current directory. Run this command, then browse to either <https://vsp.berlin/simwrapper> or <https://activitysim.github.io/dashboard> to view your local folder outputs.

- `simwrapper open [vsp|asim]` opens a new web browser tab AND a local file server in the current directory. The site will only operate as long as you keep that local server running, so don't close the command window.
  - For the ActivitySim site, use `simwrapper open asim`
  - For the VSP MATSim site, use `simwrapper open vsp`

## Running as HTTPS - required for Safari

Safari blocks HTTPS websites (such as SimWrapper VSP and ASIM) which access localhost resources such as this local simwrapper file server. You can run simwrapper in HTTPS mode by following these extra instructions.

Both simwrapper commands accept `--key` and `--cert` options to specific the two pieces of a PEM certicate. You can create a PEM certificate for "localhost" and install it in your browser's certificate database with the following commands.

This requires Homebrew, which supplies the `brew` command.

```bash
brew install mkcert nss   # installs mkcert command
mkcert localhost          # Create PEM key/cert files for "localhost"
mkcert -install           # Installs certificates in browser
```

This creates two files: `localhost.pem` and `localhost-key.pem`. Move them somewhere where you cn find them.

Now you can run simwrapper as follows:

- `simwrapper serve --cert localhost.pem --key localhost-key.pem`
- `simwrapper open asim --cert localhost.pem --key localhost-key.pem`

That's it!
