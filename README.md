prog
====

Maintains a list of programming projects, and their directories. prog open will move to that directory and open vim, resuming the session if a Session.vim is present.

    Usage:
        prog open [<name>]
        prog ls
        prog default [<name>]
        prog add [-d]
        prog add [-d] <name> <directory>
        prog rm <name>

If no directory and name is supplied to add, it will add the current directory.
