# basher
An extensible collection of Bash configuration utilities designed to synchronize your development environment across multiple devices.
Includes built-in support for secure handling of sensitive information.
A simple `git pull` on each device will sync your bash env across devices!

![Basher Logo](basher_logo.png)

Setup below
```
cd /path/to/repo
cd src
./setup.sh
```

That will setup the proper symbolic links to where you are used to seeing bash config files. 

## Starter Kit
You will find in `bash_{env, env_vars, functions, aliases}` some good starter kit functions for monotonous tasks. 
`cecho` is probably the most universally useful to let you print in color easily.

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

1. SUPER_SECRETS directory
2. SUPER_SECRETS/build_super_secrets.sh script that builds the environment variables, functions, etc. based on your sensitive info.
3. SUPER_SECRETS/super_secret_{env,env_vars,aliases,functions} get written to by build_super_secrets.sh

If you don't have sensitive info, omitting (1),(2), and (3) will not break anything.

If things your setup is static, you can just define (3) and omit (2).

An example of something you might want to do with build_super_secrets.sh is to define a "base_env_vars" file and then do some accounting
  of an ssh_config file for you that way you have all the devices you usually connect to under private version control and can simply
  port your environment rather than fussing with it every time you need to setup a new device.
