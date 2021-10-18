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

> **Synko is still in development phase and is not tested throughly**

> **Work in progress for windows**

- Sync application settings and configuration files across multiple devices (linux and macos)
- Works with dropbox as of now (support for more soon)
- Freedom to sync specific set of files across specific set of devices. Here is an example:

![feature-1-2](https://github.com/souvikinator/synko/blob/master/assets/feature-1-2.png)

# 📑 How to use

### add

**Usage:**: `synko add [configname] [paths...]`

- add file to synko

```bash
synko add config1 ~/.config/random_app/test1.conf
```

![add command 1](https://github.com/souvikinator/synko/raw/master/assets/add-cmd-1.gif)


- adding multiple files under same config name

```bash
synko add config1 ~/.config/random_app/test1.conf ~/.config/random_app/test2.conf
```

![add command 2](https://github.com/souvikinator/synko/blob/master/assets/add-cmd-2.gif)

### index

```bash
synko index
```

### remove

```bash
synko remove [configname]
```

### info

- **displaying current synko settings**

```bash
synko info
```

![info](https://github.com/souvikinator/synko/raw/master/assets/info-cmd-1.gif)

- **updating storage path**

```bash
synko info -p path/to/storage/dir
```
in gif below synko is running in **[WSL (Windows Subsystem Linux)](https://docs.microsoft.com/en-us/windows/wsl/about)** and my dropbox folder is the Windows so I had to change the dropbox path to the one in windows for it to work properly.

![info](https://github.com/souvikinator/synko/raw/master/assets/info-path-update.gif)

# 🤔 FAQ

- faq

# ⚗️ Install

Install synko with pip

> **NOTE:** If on using `command not found: synko` or similar message shows up then try running the above command as root user (`sudo`)

```bash
  pip install synko
```

# 🛠️ Setup

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Run:**

After making changes make sure to run below command

```bash
sudo python3 setup.py install
```

now to run, directly use `synko` command.

# 👨🧑 Contribution

> **If you are interested in helping with project development, see [contribution guide](https://github.com/souvikinator/synko/blob/master/CONTRIBUTING.md) to find a set of tips.**
