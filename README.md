# basher
![Basher Logo](basher_logo.png)

An extensible collection of bash configuration utilities designed to synchronize your development environment across multiple devices.

Includes built-in support for secure handling of sensitive information.

A simple `git pull` on each device will sync your bash env across devices!

Setup below
```
cd /path/to/repo
git clone https://github.com/tmasthay/basher.git
cd basher
cd src
./setup.sh
```

That will setup the proper symbolic links to where you are used to seeing bash config files. 

## Starter Kit
You will find in `bash_{env, env_vars, functions, aliases}` some good starter kit functions for monotonous tasks. 
Some examples are below.

```bash
# "color echo", 0 <= X,Y,Z <= 5
cecho --color rgbX_Y_Z [what_you_would_normally_pass_to_echo]
```
```bash
# monitors GPU memory usage on multiple GPUs -- useful when nvtop not available
mgpu color1 color2 num_iterations sleep_time_between_iterations
#     color1 defaults to red
#     color2 defaults to green
#     num_iterations defaults to 1000
#     sleep_time_between_iterations defaults to 5 seconds
```

Here's a very brief description of what each function does.

1. `cecho`: Prints text with specified colors.
2. `see_fonts`: Lists available fonts.
3. `set_var`: Sets environment variable.
4. `prepend_env_var` and `revert_env_var`: Modifies environment variables.
5. `start_ssh` and `ssh_add_all`: Manages SSH agents.
6. `matlab`: Opens MATLAB.
7. `pfs`: Prints file content with optional regex filtering.
8. `grb`: Deletes Git-related temporary files.
9. `kkp`: Kills a process based on port number.
10. `vit`: Opens Vim with a vertical terminal.
11. `gpu_mem` and `mgpu`: Monitor GPU memory usage.
12. `jail_list, ban_ip, unban_ip, and unban_ip_regex`: Manage IPs with fail2ban.
13. `cdmr`: Change to most recently modified directory.
14. `ensure_ssh_agent`: Ensures an SSH agent is running.
15. `bpushm, bpush, bpull`: Git operations for a specific directory.
16. `dwre`: Specific function likely related to your development work.
17. `tyc`: Deletes files matching a regex.
18. `sfunc, salias, svars, senv, shelp`: Sources various bash configuration files.
19. `codeo`: Opens files in Visual Studio Code.
20. `gsg, gag, ge, gem, geg`: Git shortcuts.
21. `ufw_bak, ufw_bak2, ufw_restore`: Backup and restore UFW rules.

## Be a Basher!
Do not be afraid to `bash` things up! 

Edit files with impunity just like any other repo and revert if things break!

Your `~/.bashrc` file will be **instantly** synced since `setup.sh` sets up **soft symbolic links** to the repo.

Finally, your `~/.bashrc` is only **appended** to, but still **back up your bashrc** just in case...I cannot afford a lawyer.

## Handling Different Platforms
Since you might have multiple platforms, edit the `platform` directory after a simple

```bash
git branch {linux, osx, windows, ...}
git checkout {linux, osx, windows, ...}
```


Another way to use the `platform` is for specific workflows. 
For example, say you are working in two different directories and
    90% of your edits are in your current directory but 10% of the time you need to edit a small, helper repo. 
You might have a workflow like the following.

```bash
test() {
    PREV=$(pwd)
    cd $HELPER_REPO_PATH
    pip install --force-reinstall .
    cd unit_tests
    pytest run_only_this_one_unit_test_for_now.py
    cd $PREV
}
```

This will allow you to essentially dump temporary shorthands without mucking up your global bash environment setup.

## Handling Sensitive Information
The `MILD_SECRETS` directory does some simple accounting for you; as long as you know where it expects things to be, it should be able
to integrate sensitive info into your bashrc. It expects three things; if it doesn't find these, then it will attempt to integrate the
information but if it's not there, it will exit **quietly**.


1. `SUPER_SECRETS`
    1. Be vigilant that this directory **NEVER** gets pushed to a public repo.
    2. See note below regarding `.gitignore` file, but still be vigilant...I really can't afford a lawyer. 
2. `SUPER_SECRETS/super_secret_{env,env_vars,aliases,functions}`
    1. Can be defined as standalones or written to dynamically by a script named `SUPER_SECRETS/build_super_secrets.sh`.
    2. Should use that info to write to files described in (2).
3. `SUPER_SECRETS/build_super_secrets.sh` (OPTIONAL)
    1. This is a script that builds the environment variables, functions, etc. based on your sensitive info.
    2. Should use that info to write to files described in (2).
  
**NOTE**: Look at the `.gitignore` file. Any variable with snake, camel case, or ALL_CAPS of `super_secrets` will be ignored to make sure things do not get tracked. 
Make sure to only put sensitive info inside the `SUPER_SECRETS` directory! 
If you want to put those under private version control, either clone the repo there or use symbolic links! 

If you don't have sensitive info, omitting (1),(2), and (3) will not break anything.

If things your setup is static, you can just define (3) and omit (2).

An example of something you might want to do with build_super_secrets.sh is to define a "base_env_vars" file and then do some accounting
  of an ssh_config file for you that way you have all the devices you usually connect to under private version control and can simply
  port your environment rather than fussing with it every time you need to setup a new device.
