# basher
Customizable bash config helpers that provide unified repo across devices. 
A simple `git pull` on each device will sync your bash env across devices!

![Basher Logo](basher_logo.png)

Setup below
```
cd /path/to/repo
cd src
eval $(cat config.sh)
```

That will setup the proper symbolic links to where you are used to seeing bash config files. 
Ideally, you'd just run config.sh, but I got a weird scoping issue, which is why the eval is there.
