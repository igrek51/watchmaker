# differ
**differ** monitors for a changes in any shell command output between the initial state and the current output.

# Usage
```bash
./differ.py <cmd>
```
The initial `<cmd>` output is stored at the beginning.
Then the command is run again periodically and the output is compared with the initial output.
If there are differences, they are shown in the standard diff format. The unchaged lines are not shown.

## Examples
Show how many packets have been sent since the script has been started:
```bash
$ ./differ.py ifconfig wlp2s0
-         RX packets 819320  bytes 171114372 (163.1 MiB)
?                     ---                ---      ^
+         RX packets 820098  bytes 171181884 (163.2 MiB)
?                       +++            + ++       ^
-         TX packets 2493955  bytes 3512746768 (3.2 GiB)
?                        ^^^           ^^^  ^^
+         TX packets 2496731  bytes 3516673094 (3.2 GiB)
?                       ++ ^           ^  ^^^^
```

Find new applications opening network ports (shows only changes between the initial state):
```bash
$ ./differ.py netstat -tulpn
# after opening new port:
+ tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      18655/python
```

Monitor a file for a changes:
```bash
$ ./differ.py cat /etc/resolv.conf
```

Difference between starting date and the current date:
```bash
$ ./differ.py date
- nie, 12 maj 2019, 13:41:51 CEST
?                       ^  ^
+ nie, 12 maj 2019, 13:42:52 CEST
?                       ^  ^
```
