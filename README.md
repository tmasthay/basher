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
Ideally, you'd just run config.sh, but I got a weird scoping issue, which is why the eval is there.

## Sensitive Information
The `MILD_SECRETS` directory does some simple accounting for you; as long as you know where it expects things to be, it should be able
to integrate sensitive info into your bashrc. It expects three things; if it doesn't find these, then it will attempt to integrate the
information but if it's not there, it will exit **quietly**.

(1) SUPER_SECRETS directory
(2) SUPER_SECRETS/build_super_secrets.sh script that builds the environment variables, functions, etc. based on your sensitive info.
(3) SUPER_SECRETS/super_secret_{env,env_vars,aliases,functions} get written to by build_super_secrets.sh

If things are static, you can just define (3) and completely omit (2). 
An example of something you might want to do with build_super_secrets.sh is to define a "base_env_vars" file and then do some accounting
  of an ssh_config file for you that way you have all the devices you usually connect to under private version control and can simply
  port your environment rather than fussing with it every time you need to setup a new device.
