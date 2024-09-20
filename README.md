# Dotfiles unpacker

Simple python library for syncing windows config files across devices, inspired by GNU Stow.

## File structure
Each app gets its own directory, which __must__ contain a `_paths.yaml`-file with the following structure:

```yaml
paths:
    <file description>:
        src: file1.json # Path of file inside app dir, relative to the app dir
        dst: C:\path\to\target\location.json # Path where file should be copied/symlinked
        is_dir: false # Optional, default is false. Set to true if the file is a directory
```

`~`s in paths are automatically expanded to the users home directory.

For example, to handle VS Code configs, create a directory called `vscode`, add a user settings json file called `user_settings.json` (the name can be anything), and create the following `_paths.yaml`-file inside the `vscode` directory:

```yaml
paths:
    user config:
        src: user_settings.json
        dst: ~\AppData\Roaming\Code\User\settings.json
```

If you want to add other related files, e.g. keybindings, simply add the config file in the `vscode`-directory and update `_paths.yaml` accordingly:

```yaml
paths:
    user config:
        src: user_settings.json
        dst: ~\AppData\Roaming\Code\User\settings.json
    keybindings:
        src: keybindings.json
        dst: ~\AppData\Roaming\Code\User\keybindings.json
```

## Commands

The command for running the library has the following format:

```bash
python -m unpack <action> <appdir> [dry-run]
```

* `appdir` is the name of the directory where the apps config files and `_paths.yaml` file is located
* `dry-run` only outputs to stdout, without modifying any files
* `action` controls the behaviour of the library, and can be one of the following (case insensitive):
    * `symlink` creates symlinks in the target location pointing to the source files
    * `powershell` outputs a powershell script to stdout, which when run will perform the same operation as `symlink`
    * `copy_in` copies files from the target location to the source. This is useful for initial setup, and keeping files up to date if you can't use symlinks.
    * `copy_out` copies files from the source to the target location. This is useful if you're unable to use symlinks.
