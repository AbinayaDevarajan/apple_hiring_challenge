# apple_hiring_challenge
This repository will contain solution to the apple hiring challenge
The input will contain a sequence of commands (as described below), each on a separate line
containing no more than eighty characters. Item names are case sensitive, and each is no
longer than ten characters. The command names (DEPEND, INSTALL, REMOVE and LIST)
always appear in uppercase starting in column one, and item names are separated from the
command name and each other by one or more spaces. All appropriate DEPEND commandswill appear before the occurrence of any INSTALL command that uses them. There will be no
circular dependencies. The end of the input is marked by a line containing only the word END.

Command Interpretation
DEPEND item1 item2 [item3 ...] item1 depends on item2 (and item3 ...)
INSTALL item1 install item1 and those on which it depends
REMOVE item1 remove item1, and those on which it depends, if
possible.
LIST list the names of all currently installed components.



Output
Echo each line of input. Follow each echoed INSTALL or REMOVE line with the actions taken
in response, making certain that the actions are given in the proper order. Also identify
exceptional conditions (see Sample Output, below, for examples of all cases). For the LIST
command, display the names of the currently installed components in the installation order.
No output, except the echo, is produced for a DEPEND command or the line containing END.
There will be at most one dependency list per item.
Sample Input
_______________________________________________________________________

```
DEPEND TELNET TCPIP NETCARD
DEPEND TCPIP NETCARD
DEPEND DNS TCPIP NETCARD
DEPEND BROWSER TCPIP HTML
INSTALL NETCARD
INSTALL TELNET
INSTALL foo
REMOVE NETCARD
INSTALL BROWSER
INSTALL DNS
LIST
REMOVE TELNET
REMOVE NETCARD
REMOVE DNS
REMOVE NETCARD
INSTALL NETCARD
REMOVE TCPIP
REMOVE BROWSER
REMOVE TCPIP
END
```

Sample Output
_____________________________________________________________________

```
DEPEND TELNET TCPIP NETCARD
DEPEND TCPIP NETCARD
DEPEND DNS TCPIP NETCARDDEPEND BROWSER TCPIP HTML
INSTALL NETCARD
Installing NETCARD
INSTALL TELNET
Installing TCPIP
Installing TELNET
INSTALL foo
Installing foo
REMOVE NETCARD
NETCARD is still needed.
INSTALL BROWSER
Installing HTML
Installing BROWSER
INSTALL DNS
Installing DNS
LIST
NETCARD
TCPIP
TELNET
foo
HTML
BROWSER
DNS
REMOVE TELNET
Removing TELNET
REMOVE NETCARD
NETCARD is still needed.
REMOVE DNS
Removing DNS
REMOVE NETCARD
NETCARD is still needed.
INSTALL NETCARD
NETCARD is already installed.
REMOVE TCPIP
TCPIP is still needed.
REMOVE BROWSER
Removing BROWSER
Removing HTML
Removing TCPIP
REMOVE TCPIP
TCPIP is not installed.
END
```
__________________________________________________________________________________

This solution uses python for running the program on Linux, Mac, Windows you have to have python installed

-- the problem is a graph problem
The nodes denote the software components and the vertices will point to the other nodes having the 
dependencies

"""
The idea is to create a dependency -- adjacency matrix and resolve the dependencies in the given order 
"""
