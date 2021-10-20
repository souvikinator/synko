<h1 align="center">
  <br>
  <a href="https://github.com/souvikinator/synko"><img src="https://github.com/souvikinator/synko/blob/master/assets/logo.png" alt="synko" width="200"></a>
  <br>
</h1>

<h3 align="center">sync application configuration and settings across multiple multiplatform devices</h3>
<p align="center">
  <a href="https://opensource.org/licenses/">
    <img src="https://img.shields.io/badge/License-GPL%20v3-yellow.svg"
         alt="license">
  </a>
  <a href="https://github.com/souvikinator/synko/issues"><img src="https://img.shields.io/github/issues/souvikinator/synko"></a>
  <img src="https://img.shields.io/badge/made%20with-python-blue">
</p>

<p align="center">
  <a href="#-features">✨ Key Features</a> •
  <a href="#-how-to-use">📑 How To Use</a> •
  <a href="#%EF%B8%8F-install">⚗️ Installation</a> •
  <a href="#%EF%B8%8F-setup">🛠️ Setup</a> •
  <a href="#-contribution">👨🧑 Contribution</a> •
  <a href="#-faq">🤔 FAQ</a> 
</p>

# ✨ Features

> **Synko is still in development phase and is not tested throughly, so it is recommended to take backup of the config files before adding to synko. As any bug may lead to loss of data**

> **Work in progress for windows**

- Sync application settings and configuration files across multiple devices (linux and macos)
- Works with dropbox as of now (support for more soon)
- User gets the freedom to add path to the config and setting files.
- Freedom to sync specific set of files across specific set of devices. Here is an example:

![feature-1-2](https://github.com/souvikinator/synko/blob/master/assets/feature-1-2.png)

# 📑 How to use

> **Note**: on first usage of Synko it'll look for Dropbox directory and if not found, it will prompt to enter the path to dropbox. Also synko needs to register you device so it will prompt to enter device name which can be anything you want as long as it's not conflict with pre-registered devices. Here is how it looks:
>
> In gif below, synko is running in **[WSL (Windows Subsystem Linux)](https://docs.microsoft.com/en-us/windows/wsl/about)** and my dropbox folder is the Windows so I had to change the dropbox path to the one in windows for it to work properly.
>
> ![unregistered](https://github.com/souvikinator/synko/raw/master/assets/unregistered-device.gif)
>
> In case one want's to change/update the storage path then use `synko info -p path/to/storage`

## Add

**Usage:** `synko add [paths...] --config-name="configname"`

> ### **adding files to synko**
>
> `config-name` can be anything, synko will add provided paths under the config name
>
> ![add command 1](https://github.com/souvikinator/synko/raw/master/assets/add-cmd-2.gif)

> ### **add multiple files to synko**
>
> **Note:** if `--config-name / -c` option is not used then it prompts to enter the config name as seen in below gif
>
> ![add command 2](https://github.com/souvikinator/synko/raw/master/assets/add-cmd-1.gif)

> ### **adding files under same config name**
>
> one can also add files to existing config names like so:
>
> `synko add ~/.config/random_app/newfile -c existing_config_name`

> ### **syncing same file in different device**
>
> ![syncing across device](https://github.com/souvikinator/synko/raw/master/assets/add-different-device-empty.gif)
>
> ![syncing across device](https://github.com/souvikinator/synko/raw/master/assets/add-different-device-non-empty.gif)

## Index

**Usage:** `synko index`

> ### list all the added configurations
>
> `synko index`
>
> ![index](https://github.com/souvikinator/synko/raw/master/assets/index-cmd.gif)

## Remove

**Usage:** `synko remove [options]`

> ### **remove specific configuration/settings file added to synko**
>
> `synko remove --config-name configuration_name_here`
>
> it asks to select one or multiple files one wants to remove from synko, user **right arrow key to select** and **left arrow key to unselect** , **up and down arrow key** to navigate.
> ![remove](https://github.com/souvikinator/synko/raw/master/assets/remove-cmd-1.gif)

If you don't want to remove any then select nothing and press enter, the process will be aborted

> ### **remove all config files added to Synko on current device for syncing (this won't affect other devices)**
>
> `synko remove -a`
>
> ![remove all](https://github.com/souvikinator/synko/raw/master/assets/remove-all.gif)

## Info

**Usage**: `synko info [options]`

> ### **displaying current synko settings**
>
> `synko info`
>
> ![info](https://github.com/souvikinator/synko/raw/master/assets/info-cmd-1.gif)

> ### **updating storage path**
>
> `synko info -p path/to/storage/dir`
>
> ![info](https://github.com/souvikinator/synko/raw/master/assets/info-path-update.gif)
>
> in gif above synko is running in **[WSL (Windows Subsystem Linux)](https://docs.microsoft.com/en-us/windows/wsl/about)** and my dropbox folder is the Windows so I had to change the dropbox path to the one in windows for it to work properly.

## Reset

**Usage**: `synko reset`

> ### Reset synko completely, (fresh as new)
>
> This removes all the files added to synko on current device and also resets synko by unregistering you device and the storage path. So next time you run any synko command, you'll be prompted to register your device and if the default storage path is not found then you'll be prompted to enter storage path.
>
> ![reset](https://github.com/souvikinator/synko/raw/master/assets/reset-cmd.gif)
>
> In the gif above you can see that after reset command, the time when any other synko command is executed it prompts to register device.

# 🤔 FAQ

- faq

# ⚗️ Install

Install synko with pip

> **NOTE:** If on using `command not found: synko` or similar message shows up then try running the above command as root user (`sudo`)

```bash
  pip install synko
```

# 🛠️ Setup

## **Install dependencies**

> ### using pipenv
>
> `pipenv install`

> ### using pip
>
> `pip3 install -r requirements.txt`

## **Run:**

After making changes make sure to run below command

```bash
sudo python3 setup.py install
```

now to run, directly use `synko` command.

# 👨🧑 Contribution

> **If you are interested in helping with project development, see [contribution guide](https://github.com/souvikinator/synko/blob/master/CONTRIBUTING.md) to find a set of tips.**
