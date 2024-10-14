#!/usr/bin/python3
#
# ToC
# 1. DOCUMENTATION
# 2. IMPORT & INITIALIZATION
# 3. OPTION HANDLING
# 4. ARGUMENT PROCESSING
# 5. SIGNATURE CREATION AND CHECKING

#############################################################################
#                                                                           #
#               DOCUMENTATION                                               #
#                                                                           #
#############################################################################
#
# The full manual can be printed as:
# - HTML: Replace '[[[' by < and ']]]' by >, protect original <, > brackets in text
# - plain text long: Remove everything between '[[[' and ']]]'
# - plain text short: as long, but remove text between [[[LONG]]] and [[[/LONG]]]
# - makefile: Print only the text between [[[pre make=<label>]]] and [[[/pre]]], 
#             remove '\\\n' and replace '^\$' by "\t". Add label and grouped labels
#             and a 'clean' action to complete functional makefile
#
manual = """
[[[!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"]]][[[html]]][[[header]]][[[title]]]Signature-du-Terroir[[[/title]]][[[/header]]][[[body]]][[[h1]]]Signature-du-Terroir[[[/h1]]][[[p]]]
Construct a signature of the installed software state or check the integrity of the installation
using a previously made signature.
[[[/p]]][[[p]]]
Usage: signduterre.py [options] FILE1 FILE2 ...
[[[/p]]][[[p]]]
Options:[[[/p]]][[[pre]]]
  -h, --help            show this help message and exit
  -s HEX, --salt=HEX    Enter salt in cleartext. If not given, a hexadecimal
                        salt will be suggested. The SUGGESTED[=N] keyword will
                        cause the selection of the suggested string. N is the
                        number of salts generated (default N=1). If N>1, all
                        will be printed and a random one will be used to
                        generate the signature (selection printed to STDERR).
  -a, --all-salts-pattern
                        Use all salts in sequence, randomly replace salts with
                        incorrect ones in the output to create a pattern of
                        failing hashes indicated by a corresponding integer
                        number. Depends on '--salt SUGGESTED=N'. Implies
                        --total-only.
  -p TEXT, --passphrase=TEXT
                        Enter passphrase in cleartext, the keyword
                        SUGGESTED[=N] will cause the suggested passphrase to
                        be used. If N>1, N passphrases will be printed to
                        STDERR and a random one will be used (selection
                        printed to STDERR). Entering the name of an existing
                        file (or '-' for STDIN) will cause it to be read and a
                        random passphrase found in the file will be used
                        (creating a signature), or they will all be used in
                        sequence (--check-file).
  -c FILE, --check-file=FILE
                        Check contents with the output of a previous run from
                        file or STDIN ('-'). Except when the --quiet option is
                        given, the previous output will contain all
                        information needed for the program, but not the
                        passphrase and the --execute option.
  -i FILE, --input-file=FILE
                        Use names from FILE or STDIN ('-'), use one filename
                        per line.
  -o FILE, --output-file=FILE
                        Print to FILE instead of STDOUT.
  --file-source=PATH    Read all files from PATH. The PATH-string is prepended
                        to every plain file-path that is read for a signature.
                        Remote files can be checked with
                        'ssh://<user>@<host>[/path]'. A shell command that
                        prints out the file can be entered as '$(<cmd>)'. The
                        filepath will be substituted for any '{}' string in
                        the command, or appended tot the command (without
                        white-space). The option overrules any File source
                        specification in the --check-file.
  -P FILE, --Private-file=FILE
                        Print private information (passwords etc.) to FILE
                        instead of STDERR.
  -u USER, --user=USER  Execute $(cmd) as USER, default 'nobody' (root/sudo
                        only)
  -S, --Status          For each file, add a line with unvarying file status
                        information: st_mode, st_ino, st_dev, st_uid, st_gid,
                        and st_size (like the '?' prefix, default False)
  --Status-values=MODE  Status values to print for --Status, default MODE is
                        'fmidugs' (file, mode, inode, device, uid, gid, size).
                        Also available (n)l(inks) a(time), (m)t(ime), and
                        c(time).
  -t, --total-only      Only print the total hash, unsets --detailed-view
                        (default True)
  -d, --detailed-view   Print hashes of individual files, is unset by --total-
                        only (default False)
  -e, --execute         Interpret $(cmd) (default False)
  --execute-args=ARGS   Arguments for the $(cmd) commands ($1 ....)
  -n, --no-execute      Explicitely do NOT Interpret $(cmd)
  --import=FILE         Import python modules (comma separated list without extension)
  --print-textdump      Print printable character+hexadecimal dump of input
                        bytes to STDERR for debugging purposes
  --message=TEXT        Add a comment message about the test
  -m, --manual          Print a short version of the manual and exit
  --manual-long         Print the long version of the manual and exit
  --manual-html         Print the manual in HTML format and exit
  --manual-make         Print the examples in the manual as a makefile and
                        exit
  -r, --release-notes   Print the release notes and exit
  -l, --license         Print license text and exit
  -v, --verbose         Print more information on output
  -q, --quiet           Print minimal information (hide filenames). If the
                        output is used with --check-file, the command line
                        options and arguments must be repeated.
[[[/pre]]][[[p]]]
FILE1 FILE2 ...
Names and paths of one or more files to be checked. All file arguments in SdT accept '-' as the STDIN file
(ie, piped data). Can use ssh://<user>@<host>/path pseudo-URLs for checking files at remote sites. Arguments
of any type can take an appended range parameter '[<start>:<end>:<offset>]' or '[<start>:+<length>:<offset>]'. 
<offset>+<start> bytes are skipped and only <length>=<end>-<start> bytes are written. Leaving out the second 
argument, ie, '[<start>:]', means all bytes after <start> to the end of the file or stream are used. The 
':<offset>' argument is optional. All <start>, <end>, <length>, and <offset> arguments are eval(uat)ed by
the Python interpreter as expressions. This means ranges can be can be entered in decimal (default), 
hexadecimal (0x0000..), octal (0o0000..), and binary (0B0000..) representations. 
[[[/p]]][[[p]]]
Single expression byte rangess can each be enclosed in ()-brackets, and this is obligatory if a ':' character 
is used in an expression. It is allowed to use balanced []-brackets in expressions inside the byte range 
slices. Python evaluation takes place INSIDE the current Python environment. This means there is access to 
all imported modules including those imported with the --import option.[[[br /]]]
THIS COULD BE A SECURITY CONCERN AND THE '--execute' OPTION IS REQUIRED TO CALL ANY FUNCTION IN BYTE RANGE
SLICE EXPRESSIONS
[[[/p]]][[[p]]]
Any name starting with a '$', eg, $PATH, will be interpreted as an environmental variable or a command 
according to the bash conventions: '$ENV' and '${ENV}' as variables, '$(cmd;cmd...)' as system commands 
(bash --restricted -c 'cmd;cmd...' PID). Where PID the current Process ID is (available as positional 
parameter $0). Other parameters can be entered with the --execute-args option ($1 etc). Do not forget to 
enclose the arguments in single ''-quotes! The commands are scanned for unwanted characters and these 
are removed (eg, ' and \\, however, escaping $ is allowed, eg, '\\$1'). The use of '$(cmd;cmd...)' 
requires explicit use of the -e or --execute option. 
[[[/p]]][[[p]]]
Note that byte range slices '$(cmd)[<start>:<end>]' do work, but only [[[em]]]after[[[/em]]] the command 
has completed. So, the file version, '/dev/kmem[0xc04838a0:+88]', will simply use 88 bytes as in 
'$(dd if=/dev/kmem bs=1 skip=3225958560 count=88)'. However, '$(dd if=/dev/kmem bs=1)[0xc04838a0:+88]' will 
[[[em]]]first[[[/em]]] read all of /dev/kmem, and only then extract the 88 bytes. In general, this is not 
the desired procedure (/dev/kmem contains all of the physical RAM). Note that the remote 
'--file-soource=ssh://...' option preserves the file slice behavior as the file reads are changed into the 
equivalent 'dd skip=<start> count=<length>' commands. 
[[[/p]]][[[p]]]
Any string '@(python code)' will be evaluated as python 3 code. The '--execute' option is obligatory. 
Note that the outer ()-brackets are removed. You can extend the program by importing modules with the 
'--import <module>,<module>,....' option. The python code will be interpreted as a function body, 
complete with obligatory return statement(s), and wrapped in a function definition. This function will 
be executed in a separate namespace and the 'return'ed value will be exported and hashed. The current PID
is available as 'argv[0]' and the --execute-args argument values are available as list elements 'argv[1]', 
'argv[2]', etc. @() statements are executed inside the running signduterre program and cannot be used to 
querry a remote system with ssh:// pseudo-URL constructs.
[[[/p]]][[[p]]]
If executed as root or sudo, $(cmd;cmd...) will be executed as 'sudo -H -u <user>' which defaults to
--user nobody ('--user root' is at your own risk). This will obviously not work when invoked as non-root/sudo.
--user root is necessary when you need to check privileged information, eg, you want to check the MBR with 
'$(dd if=/dev/hda bs=512 count=1 | od -X)'
However, as you might use --check-file with files you did not create yourself, it is important to
be warned if commands are to be executed.
[[[/p]]][[[p]]]
Interpretation of $() ONLY works if the -e or --execute options are entered. signduterre.py can easily 
be adapted to automatically use the setting in the check-file. However, this is deemed insecure and 
commented out in the distribution version.
[[[/p]]][[[p]]]
The -n or --no-execute option explicitely supress the interpretation of $(cmd) arguments.
[[[/p]]][[[p]]]
Meta information from stat() on files is signed when the filename is preceded by a '?'. '?./signduterre.py' will 
extract (st_mode, st_ino, st_dev, st_nlinks, st_uid, st_gid, st_size) and hash a line of these data (visible 
with --verbose). The --Status option will automatically add such a line in front of every file. Note that '?' 
is implied for directories. Both '/' and '?/' produce a hash of, eg,: 
[[[/p]]][[[pre]]]
stat(/) = [st_mode=041775, st_ino=2, st_dev=234881026, st_uid=0, st_gid=80, st_size=1360]
[[[/pre]]][[[p]]]
The --Status-values=<mode> option selects which status values will be used: f(ile), m(ode), i(node), 
d(evice), u(id), g(id), s(ize), (n)l(inks), a(time), (m)t(ime), and c(time). Default is 
--Status-values='fmidugs'. Note that nlinks of a directory include every file in the directory, so this 
option can check whether files have been added to a directory.
[[[/p]]][[[p]]]
Arguments enclosed in []-brackets will be hidden in the output. That is, '[/proc/self/exe]' will show up as
'[1]' in the output (or '[n]' with n the number of the hidden argument), equivalent to the use of the 
--quiet option. This means the hidden arguments must be entered again when using the --check-file (-c) 
option.
[[[/p]]][[[h1 align="CENTER"]]]
Signature-du-Terroir
[[[/h1]]][[[p]]]
A very simple tool to generate a signature that can be used to test the integrity of files and "states" in 
a running installation. signduterre.py constructs a signature of the current system state and checks 
installation state with a previously made signature. The files are hashed with a passphrase to allow detection 
of compromised systems while running on the same system. The signature checking can be subverted, but the 
flexibillity of signduterre.py and the fact that the output of any command can be tested should hamper 
automated root-kit attacks.
[[[/p]]][[[p]]]
signduterre.py writes a total SHA-256 hash to STDOUT of all the files and commands entered as arguments. It 
can also write a hash for each individual file (insecure). The output of a signature can be send to a file and 
later used to check with --check-file. Hashes are calculated with a hashed salt + passphrase sequence 
pre-pended to create unpredictable hashes. This procedure ensures that an attacker does not know whether or 
not the correct passphrase has been entered. An attacker can only know when to supply the requested hash 
values if she knows the passphrase or has copies available of all the tested files and output of commands to 
calculate the hashes on the fly.
[[[/p]]][[[LONG]]][[[h2]]]
The Problem
[[[/h2]]][[[p]]]
The problem SdT tries to solve is how to test whether your system has been compromised when you can only use 
the potentially compromised system? The solution is to store a password encrypted signature (or fingerprint) 
of your system when you are sure it is in a good state. Then you check whether the system can still 
distinguish between correct and incorrect passwords when it regenerates the signature. The trick is to use 
the right data (ie, questions) to generate the signature.
[[[/p]]][[[p]]]
The underlying idea is that some bits have to be changed to compromise a system. That is, program
files have been altered, settings and accounts changed, new processes are running or existing processes 
altered. The most common situation is that some system programs have been changed to hide the traces of
the attack. For instance, the [[[i]]]ls[[[/i]]], [[[i]]]find[[[/i]]], and [[[i]]]stat[[[/i]]] commands are altered to hide the existence of new files
and programs, and the [[[i]]]netstat[[[/i]]] and [[[i]]]ps[[[/i]]] commands or the [[[i]]]/proc[[[/i]]] pseudo file system are changed to hide the 
malicious processes that are running. Such wholescale adaptations of running systems can be executed 
using standard, off-the-shelf application suits, so called rootkits. There are applications that can 
detect common (known) rootkits and other malicious programs, eg, [[[i]]]chkrootkit[[[/i]]] ([[[a 
href="http://www.chkrootkit.org/"]]]www.chkrootkit.org[[[/a]]]) and 
[[[i]]]rootkit hunter[[[/i]]] ([[[a 
href="http://www.rootkit.nl"]]]www.rootkit.nl[[[/a]]]). However, these rootkit detectors also use existing commands on the 
potentially compromised system, so a rootkit can hide from them too.
[[[/p]]][[[p]]]
There are two obvious directions to guard against rootkits. One is to continuously run a process that
looks for attempts to install a rootkit and other malicious activities. The other is to take a snapshot 
of the system in a known good state, and then flag changes in relevant areas, eg, like [[[i]]]Tripwire[[[/i]]] 
([[[a href="http://sourceforge.net/projects/tripwire/"
]]]http://sourceforge.net/projects/tripwire/[[[/a]]]) and [[[i]]]Radmind[[[/i]]] ([[[a 
href="http://rsug.itd.umich.edu/software/radmind/"
]]]http://rsug.itd.umich.edu/software/radmind/[[[/a]]]).
Signature-du-Terroir takes the second route, it creates a signature of a set of relevant files and 
command output, and checks later whether these have not been changed. However, when running such a test 
on a compromised system, the attacker can theoretically "fool" any (automated) test. In practise, time 
and other precious resources will limit what an attacker can accomplish. The idea is to raise the bar 
for rootkits high enough to make them not worthwhile. SdT tries to make using signatures easy (cheap)
and subverting it difficult (expensive).
[[[/p]]][[[p]]]
As an illustration of the problem SdT treis to solve, take the [[[i]]]sha256sum[[[/i]]] command which generates file 
hashes (signatures) using the SHA256 algorithm. Hashes can be generated and checked with this command:
[[[/p]]][[[pre]]]
# Use of sha256sum to check integrity of ps and ls commands
$ sha256sum /bin/ps /bin/ls > ps-ls.sh256
$ sha256sum -c ps-ls.sh256
[[[/pre]]][[[p]]]
A compromised file will show up as FAILED. This is ok for unintentional changes to the files. However, a 
malicious attacker could easily replace [[[i]]]/usr/bin/sha256sum[[[/i]]] with a program that would replace the hash of 
malicious replacements of these files with the hash sums of the original files. There are three easy ways 
of doing that. Either simply say 'ok' when checking the file, print out the stored old hash value whenever 
an altered file is requested by name, or look for the hash of the new, malicious replacement and print out 
the old hash sum instead. The former two are easy to circumvent, the last one is somewhat less easy.
[[[/p]]][[[p]]]
The first solution to these avoidance strategies is to generate the signatures with a passphrase and random
string (salt). As long as the attacker does not know the passphrase, the only way to subvert SdT is to store
the original bits in the files and calculate the signature the moment SdT is called. As the attacker does 
not know when the correct password or salt is entered, it is not possible to simply answer OK or repeat the
stored earlier results instead of calculating them de-novo.
[[[/p]]][[[p]]]
To be able to serve up the original bits, instead of the bits used on the compromised system, when asked
for the hashes, the attacker must divert attempts to read the files by SdT, but not at other moments. 
There are many ways to do this, eg, running python in a chroot-jail, changing python itself, changing other
programs. To accommodate these diversion strategies, SdT allows to read data from each and every command
that can supply it. So, a binary file can be entered by name, with eg, cat, dd, perl, python, ruby, or read 
from the [[[i]]]/proc[[[/i]]] system (if it is a running process), or from STDIN or shell subprocesses. For instance, 
to protect against running in a chroot-jail, the inode number and device of the root directory can be read 
from [[[i]]]/proc/self/root[[[/i]]], or [[[i]]]/proc/<PID>/root[[[/i]]], or simply from [[[i]]]/[[[/i]]].
[[[/p]]][[[/LONG]]][[[h2]]]
Signature creation: Passphrases, salts, and hashes
[[[/h2]]][[[p]]]
Good passphrases are difficult to remember, so their plaintext form should be protected. To protect the 
passphrase against rainbow and brute force attacks, the passphrase is concatenated to a salt phrase and 
hashed before use (SHA-256). 
[[[/p]]][[[p]]]
The salt phrase is requested when constructing a signature. In interactive use, an 8 byte hexadecimal 
(= 16 character) salt from [[[i]]]/dev/urandom[[[/i]]] is suggested. If '--salt SUGGESTED' is entered on the command line
as the salt, the suggested value will be used. The salt is printed in plaintext to the output. The salt will 
make it more difficult to determine whether the same passphrase has been used to create different signatures.
[[[/p]]][[[p]]]
At the bottom, a 'TOTAL HASH' line will be printed that hashes all the lines printed for the files. This 
includes the file names as printed on the hash lines. It is not inconceivable that existing signature files 
could have been compromised in ways that might be missed when checking the signature. The total hash will 
point out such changes.
[[[/p]]][[[h3]]]
SECURITY
[[[/h3]]][[[LONG]]][[[p]]]
When run on a compromised system, signduterre.py can be subverted if the attacker keeps a copy of all the 
files and command outputs, and reroutes the open() and stat() functions, or simply delegating signduterre.py 
to a chroot jail with the original system. In principle, signduterre.py only checks whether the computer 
responds identically to when the signature file was made. There is no theoretic barrier against a compromised 
computer perfectly simulating the original system when tested, but behaving adversely at other times. Except 
for running from clean boot media (USB?), I know of no theoretical sound solution to this problem.
[[[/p]]][[[p]]]
However, this scenario assumes the use of unlimited resources and time. Inside a limited, real computer system, 
the attacker must make compromises on what can and what cannot be simulated with the available time and 
hardware. The idea behind signduterre.py is to "ask difficult questions" that increase the cost of simulating 
the original system high enough to make detection of successful attacks likely.signduterre.py simply intends 
to raise the bar high enoug. One point is to store the times needed to create the original hashes. This timing 
can later be used to see whether the new timings are reasonable. If the same hardware takes considerably 
longer to perform the same calculations, or needs a much longer delay before it starts, the tester might want 
to see where this time is spent.
[[[/p]]][[[/LONG]]][[[p]]]
Signature-du-Terroir works on the assumption that any attacker in control of a compromised system cannot
predict whether the passphrase entered is correct or not. An attacker can always intercept the in- and output 
of signduterre. When running with --check-file, this means the program can be made to print out OK 
irrespective of the tests. A safe use of signduterre.py is to start with a random number of incorrect 
passphrases and see whether they fail. Alternatively, and easier, is to add a number of unused salts
to the check-file and let the attacker guess which one is correct.
[[[/p]]][[[p]]]
THE CORRECT USE OF signduterre.py IS TO ENTER A RANDOM NUMBER OF INCORRECT PASSPHRASES OR SALTS FOR EACH 
TEST AND SEE WHETHER IT FAILS AT THE CORRECT INSTANCES!
[[[/p]]][[[p]]]
On a compromised system, signduterre.py's detailed file testing (--detailed-view) is easily subverted. With a 
matched file hash, the attacker will know that the correct passphrase has been entered and can print out the 
stored hashes or 'ok's  for the rest of the checks. So if the attacker keeps any entry in the signature file 
uncompromised, she can intercept the output, test the password on the unchanged entry and substitute the 
requested hashes for the output if the hash of that entry matches. 
[[[/p]]][[[LONG]]][[[p]]]
When checking for root-kits and other malware, it is safest to compare the signature files from a different, 
clean, system. But then you would not need signduterre.py anyway. If you have to work on the system itself, 
only use the -t or --total-only options to create signatures with a total hash and without individual file 
hashes. Such a signature can be used to check whether the system is unchanged. Another signature file WITH A 
DIFFERENT PASSPHRASE can then be used to identify the individual files that have changed. If a detailed 
signature file has the same passphrase, an attacker could use that other file to read the individual file 
hashes to check whether the correct passphrase was entered.
[[[/p]]][[[/LONG]]][[[p]]]
Using the --check-file option in itself is UNsafe. An attacker simply has to print out 'OK' to defeat the 
check. This attack can be foiled by making it unpredictable when signduterre.py should return 'OK'. This can 
be done by using a list of salts or passphrases where only one of them (or none!) is correct. Any attacker 
will have to guess when to return 'OK'.
[[[/p]]][[[LONG]]][[[p]]]
As generating and entering wrong passphrases and salts is tedious, users have to be supported in correct use 
of SdT. To assist users, the '--salt SUGGESTED=<N>' option will generate a number N of salts. When 
checking, each of these salts is tried in turn. An attacker that is unable to simulate the uncompromised 
system will have to guess which one of the salts is the correct one, and whether or not the passphrase 
is correct. This increases the chances of detecting compromised systems. If this is not enough guess
work, the '-a', '--all-salts-pattern' option will use all salts in sequence to generate total hashes,
but random salts will be changed in the output. This generates a pattern of failed salt tests. This pattern
is translated into a bit pattern and printed as an integer ([Fail, Fail, OK, Fail, OK, OK, Fail, OK]
= 00101101 (least significant first) = 10110100 (unsigned bin) = 180). On creation of a signature, this 
number is printed to STDERR, on checking (--check-file) it is printed to STDOUT (note that the number
will never become 0 or all Fail). So for '--salt SUGGESTED=<N> --all-salts-pattern' the probability of 
guessing the correct output goes from 1/N to 1/(2^N - 1). Note that '--all-salts-pattern' will work, 
but is pointless, without '--salt SUGGESTED=<N>' with N>1.
[[[/p]]][[[p]]]
The '--passphrase SUGGESTED=N' option will generate and print N passphrases. One of these is chosen at 
random for the signature. The number of the chosen passphrase is printed on STDERR with the passwords. 
When checking a file, the stored passphrases can be read in again, either by entering the passphrase 
file after the --passphrase option ('--passphrase <passphrase file>'), or directly from the --check-file. 
signduterre.py will print out the result for each of the passphrases. 
[[[/p]]][[[p]]]
Note, that storing passphrases in a file and feeding it to signduterre.py is MUCH less secure than just 
typing them in. Moreover, it might completely defeat the purpose of signduterre.py. If future experiences 
cast any more doubt on the security of this option, it will be removed. 
[[[/p]]][[[p]]]
For those who want to know more about what an "ideal attacker" can do, see:[[[br]]]
Ken Thompson "Reflections on Trusting Trust"[[[br]]]
[[[a href="http://cm.bell-labs.com/who/ken/trust.html"]]]http://cm.bell-labs.com/who/ken/trust.html[[[/a]]][[[br]]]
[[[a href="http://www.ece.cmu.edu/~ganger/712.fall02/papers/p761-thompson.pdf"]]]http://www.ece.cmu.edu/~ganger/712.fall02/papers/p761-thompson.pdf[[[/a]]]
[[[/p]]][[[p]]]
David A Wheeler "Countering Trusting Trust through Diverse Double-Compiling"[[[br]]]
[[[a href="http://www.acsa-admin.org/2005/abstracts/47.html"]]]http://www.acsa-admin.org/2005/abstracts/47.html[[[/a]]]
[[[/p]]][[[p]]]
and the discussion of these at Bruce Schneier's 'Countering "Trusting Trust"'[[[br]]]
[[[a href="http://www.schneier.com/blog/archives/2006/01/countering_trus.html"]]]http://www.schneier.com/blog/archives/2006/01/countering_trus.html[[[/a]]]
[[[/p]]][[[/LONG]]][[[h2]]]
Manual
[[[/h2]]][[[p]]]
The intent of signduterre.py is to ensure that the signature cannot be subverted even if the system has been 
compromised by an attacker that has obtained root control over the computer and any existing signature files.
[[[/p]]][[[p]]]
signduterre.py asks for a passphrase which is PRE-pended to every file before the hash is constructed (unless 
the passphrase is entered with an option). As long as the passphrase is not compromised, the hashes cannot 
be reconstructed. A randomly generated, unpadded base-64 encoded 16 Byte password (ie, ~22 characters) is 
suggested in interactive use. If '--passphrase SUGGESTED' is entered on the command line or no passphrase is
entered when asked, the suggested value will be used. This value is printed to STDERR (the screen or 2) for 
safe keeping. Please, make sure you store the printed passphrase. For instance:
[[[/p]]][[[pre make=example1]]]
# make: example1
# Simple system sanity test using the 'which' command to establish the paths
$ python3 signduterre.py --passphrase SUGGESTED --salt SUGGESTED --detailed-view \\
`which python3 bash ps ls find stat` 2> test-20090630_11-14-03.pwd > test-20090630_11-14-03.sdt
$ python3 signduterre.py --passphrase test-20090630_11-14-03.pwd --check-file test-20090630_11-14-03.sdt
[[[/pre]]][[[p]]]
The first command will store the passphrase (and all error messages) in a file 'Signature_20090630_11-14-03.pwd'
and the check-file in 'Signature_20090630_11-14-03.sdt'. The second line will test the signature.
The signature will be made of the files used for the commands python3, bash, ps, ls, find, and stat.
These files are found using the 'which' command.
[[[/p]]][[[h2]]]
Working with remote systems
[[[/h2]]][[[p]]]
It is not secure to store files with the passphrase on the system you want to check. However, you could
pipe STDERR to some safe site.
[[[/p]]][[[pre]]]
# Send passphrase over ssh tunnel to safe site
$ python3 signduterre.py --passphrase SUGGESTED --salt SUGGESTED `which bash python3` \\
-o test-safe-store.sdt 2>&1 | ssh user@safe.host.site 'dd of=/home/user/safe/test-safe-store.pwd'
[[[/pre]]][[[p]]]
As the security of the passphrases is important and off-site storrage of files is often prudent or convenient, 
this tunneling construct has been automated in all in- and output as a pseudo-URL: 'ssh://<user>@<host></path>', 
eg, 'ssh://user@safe.host.site/home/user/safe/test-safe-store.pwd'. It is not possible to enter a 
password in such a pseudo-URL, so the automatical login into the host system must be configured in SSH.[[[br /]]]
[[[em]]]Note: There are severe security risks involved when using SSH to login into another system if the
originating system is compromised[[[/em]]].
[[[/p]]][[[p]]]
The pseudo-url can be used with the  [[[i]]]--output-file, --Private-file, --input-file, --check-file, --passphrase[[[/i]]] 
options as well as for the actual file, ${ENV}, and $(cmd) arguments used to determine the signatures. The latter 
allows to check files on remote systems, or to repeat a check from a remote system using the [[[i]]]--file-source[[[/i]]]
option (only works with plain files, ${ENV}, and $(cmd), not for @(python code), directories, or --Status arguments). 
For instance:
[[[/p]]][[[pre]]]
# Use ssh:// pseudo-url to send passphrase to safe.host.site
$ python3 signduterre.py --passphrase SUGGESTED --salt SUGGESTED `which bash python3` \\
-o ssh://user@safe.host.site/home/user/safe/test-safe-store.sdt \\
-P ssh://user@safe.host.site/home/user/safe/test-safe-store.pwd
# Check files on remote compromised.host.site while running test program on safe.host.site
$ python3 signduterre.py --passphrase test-safe-store.pwd --check-file test-safe-store.sdt \\
--file-source ssh://user@compromised.host.site
[[[/pre]]][[[p]]]
To execute a remote $(cmd) argument, write $(ssh://<user>@<host>/cmd). Be aware that nested "-quotes might cause
problems. ${ENV} can be written as ${ssh://<user>@<host>/ENV}. When using a --file-source argument that starts 
with 'ssh://', the $(cmd) and ${ENV} commands are internally rewritten into the above form. In both forms,
as well as the arguments entered with --execute-args, any '$' and '"' symbols are protected by '\$' and '\"' to 
be evaluated at the host system, as they would be evaluated locally by the ssh command line. This might not 
always work out as planned, so take care when using these pseudo-URLS. Note that no <path> argument will be used.
[[[/p]]][[[p]]]
The next example uses the ssh:// pseudo-URL to read the data in an alternative way on [[[i]]]localhost[[[/i]]]. Obviously, storing the
plain text passphrase on the same system makes it a rather pointless excersize. The example only works if your have
(open)SSH server and clients installed and appended the '~/.ssh/id_dsa.pub' or '~/.ssh/id_rsa.pub' file to '~/.ssh/authorized_keys', 
and you used ssh-add or another application to open the key.
[[[/p]]][[[pre make=ssh1]]]
# make: ssh1
# Use ssh:// pseudo-url to read data in an alternative way
$ python3 signduterre.py --passphrase SUGGESTED --salt SUGGESTED -v -d -e `which dd` '$(cat `which dd`)' \\
-o test-safe-store.sdt \\
-P ssh://`whoami`@localhost${PWD}/test-safe-store.pwd
# check files the standard way
$ python3 signduterre.py -e --passphrase ssh://`whoami`@localhost${PWD}/test-safe-store.pwd --check-file test-safe-store.sdt
# Check files using ssh on localhost
$ python3 signduterre.py -e --passphrase ssh://`whoami`@localhost${PWD}/test-safe-store.pwd --check-file test-safe-store.sdt \\
--file-source ssh://`whoami`@localhost
[[[/pre]]][[[h2]]]
Examples:[[[/h2]]][[[pre make=example2]]]
# make: example2
# Self test of root directory, python, and signduterre.py using the 'which' command to establish the paths
$ python3 signduterre.py --detailed-view --salt 436a73e3 --passphrase liauwefa3251EWC -o test-self.sdt \\
 / `which python3 signduterre.py`
$ python3 signduterre.py --passphrase liauwefa3251EWC -c test-self.sdt
[[[/pre]]][[[LONG]]][[[p]]]
Write a signature to the file test-self.sdt and test it with the --check-file option. The signature contains 
the SHA-256 hashes of the files, [[[i]]]/usr/bin/python3[[[/i]]], [[[i]]]signduterre.py[[[/i]]], and the status information on the root 
directory. The salt '436a73e3' and passphrase 'liauwefa3251EWC' are used.
[[[/p]]][[[/LONG]]][[[pre make=procfs1]]]
# make: procfs1
# Self test of root directory, python, and signduterre.py using the the /proc file system
$ python3 signduterre.py --detailed-view --salt SUGGESTED --passphrase liauwefa3251EWC -o test-self_proc.sdt \\
 /proc/self/root /proc/self/exe `which signduterre.py`
$ python3 signduterre.py --passphrase liauwefa3251EWC --check-file test-self_proc.sdt
[[[/pre]]][[[LONG]]][[[p]]]
Write a signature to the file test-self_proc.sdt and test it with the --check-file option. The signature 
contains the SHA-256 hashes of the same files as above, [[[i]]]/usr/bin/python3[[[/i]]], [[[i]]]signduterre.py[[[/i]]], and the status 
information on the root directory. However, the python executable and the root directory are now accessed
through the [[[i]]]/proc[[[/i]]] file system. The suggested salt is used (written to test-self_proc.sdt) and the passphrase 
is (again) 'liauwefa3251EWC'.
[[[/p]]][[[/LONG]]][[[pre make=example3]]]
# make: example3
# Test of supporting commands for chkrootkit
$ python3 signduterre.py --execute --total-only --salt SUGGESTED=8 --passphrase SUGGESTED --Status \\
  --output-file=test-chkrootkit.sdt --Private-file=test-chkrootkit.pwd \\
  signduterre.py `which bash awk cut egrep find head id ls netstat ps strings sed uname`
$ python3 signduterre.py --execute --passphrase test-chkrootkit.pwd --check-file test-chkrootkit.sdt
[[[/pre]]][[[LONG]]][[[p]]]
Writes a signature of the requested files to test-chkrootkit.sdt (signature) and private information to 
test-chkrootkit.pwd (password and selected salt) and checks it in the next line. The files are those of 
commands required by the [[[i]]]chkrootkit[[[/i]]] program (http://www.chkrootkit.org/), with bash added. The 'which' 
command will give the paths for the commands. Eight salts are generated, of which only 1 is actually 
used. When checking, the correct salt should match. This prevents a compromised program from simply 
printing out OK tot he check. A more comprehensive evation of guessing the correct salt can be obtained
by using the '--all-salts-pattern' option.
[[[/p]]][[[/LONG]]][[[pre make=procfs2]]]
# make: procfs2
# Simply lump all "system" files, the PATH environment variable and the first 2 columns of the output of lsmod
$ python3 signduterre.py --execute --detail --salt SUGGESTED --passphrase liauwefa3251EWC --Status --total-only \\
  signduterre.py /sbin/* /bin/* /usr/bin/find /usr/bin/stat /usr/bin/python3 '${PATH}' \\
  '$(lsmod | awk "{print \$1, \$2}")' > test-20090625_14-31-54.sdt
# 
# Failing check due to missing --execute option
$ python3 signduterre.py --passphrase liauwefa3251EWC -c test-20090625_14-31-54.sdt
$ python3 signduterre.py --passphrase liauwefa3251EWC -c test-20090625_14-31-54.sdt --no-execute
# 
# Successful check
$ python3 signduterre.py --execute --passphrase liauwefa3251EWC --check-file test-20090625_14-31-54.sdt
[[[/pre]]][[[LONG]]][[[p]]]
Prints a signature to the system test-20090625_14-31-54.sdt and the automatically generated password to 
test-20090625_14-31-54.pwd. The salt will be automatically determined. The signature contains the SHA-256 
hashes of the file status and file contents of [[[i]]]signduterre.py, /sbin/*, /bin/*,  /usr/bin/find, 
/usr/bin/file, /usr/bin/python*[[[/i]]] on separate lines, and a hash of the PATH environment variable. Do not 
display the hash of every single file, which could be insecure, but only the total hash.
The first two checks will both fail if test-20090625_14-31-54.sdt contains a $(cmd) entry. 
The --no-execute option is default and prevents the execute option (if reading the execute option from the 
signature file has been activated). The last check will succeed (if the files have not been changed).
[[[/p]]][[[/LONG]]][[[pre make=example4]]]
# make: example4
# Use a list of generated passphrases
$ python3 signduterre.py --salt SUGGESTED --passphrase SUGGESTED=20 signduterre.py \\
2> test-20090630_16-44-34.pwd > test-20090630_16-44-34.sdt
$ python3 signduterre.py -p test-20090630_16-44-34.pwd -c test-20090630_16-44-34.sdt
[[[/pre]]][[[LONG]]][[[p]]]
Will generate and print 20 passphrases and print a signature using one randomly chosen passphrase from these 
20. Everything is written to the files 'test-20090630_16-44-34.pwd' and 'test-20090630_16-44-34.sdt'.
Such file names can easily be generated with 'test-`date "+%Y%m%d_%H-%M-%S"`.sdt'.
The next command will check all 20 passphrases generated before from the Signature file and print the results.
[[[/p]]][[[/LONG]]][[[pre make=example5]]]
# make: example5
# Use a list of generated salts with a pattern of correct salts
$ python3 signduterre.py --salt SUGGESTED=16 --passphrase SUGGESTED --all-salts-pattern \\
-P test-salt-pattern.pwd -o test-salt-pattern.sdt `which bash stat find ls ps id uname awk gawk perl` 
$ python3 signduterre.py -p test-salt-pattern.pwd -c test-salt-pattern.sdt
# Compare to salt pattern number to the one from the check-file
$ cat test-salt-pattern.pwd
[[[/pre]]][[[LONG]]][[[p]]]
As the previous, but with a pattern of random correct and incorrect salts. The salt pattern number
indicates which salts were and were not correct.
[[[/p]]][[[/LONG]]][[[pre make=sudo1]]]
# make: sudo1
# Check MBR and current root directory (sudo and root user)
$ sudo python3 signduterre.py -u root -s SUGGESTED -p SUGGESTED --Status-values='i' -v -e -t \\
--output-file test-boot-sector.sdt --Private-file test-boot-sector.pwd --execute-args=sda \\
'?/proc/self/root' `which dd` '$(dd if=/dev/$1 bs=512 count=1 | od -X)'
$ sudo python3 signduterre.py -u root -e -p test-boot-sector.pwd -c test-boot-sector.sdt
[[[/pre]]][[[LONG]]][[[p]]]
Will hash the inode numbers of the effective root directory (eg, chroot) and the executable (python) 
together with the contents of the MBR (Master Boot Record) on [[[i]]]/dev/sda[[[/i]]] in Hex. It uses suggested salt and 
passphrase. Accessing [[[i]]]/dev/sda[[[/i]]] is only possible when [[[i]]]root[[[/i]]], so the command is entered with [[[i]]]sudo[[[/i]]] and 
'--user root'. Use the '--print-execute' option if you want to check the output of the [[[i]]]dd[[[/i]]] command.
[[[/p]]][[[p]]]
The main problem with intrusion detection by comparing file contents is the ability of an attacker 
to redirect attempts to read a compromised file to a stored copy of the original. So, [[[i]]]sha256sum[[[/i]]] or 
python could be changed to read [[[i]]]'/home/attacker/old/ps'[[[/i]]] when the argument was [[[i]]]'/bin/ps'[[[/i]]]. This would 
foil any scheme that depends on entering file names in programs. An answer to this threat is to 
read the bytes in files in as many ways as possible. Therefor, forcing an attacker to change many 
files which itself would increase the probability of detection of the attack. The following command 
will read the same (test) file, and generate identical hashes, in many different ways.
[[[/p]]][[[/LONG]]][[[pre make=example6]]]
# make: example6
# Example generating identical signatures of the same text file in different ways
$ dd if=signduterre.py 2>/dev/null | \\
python3 signduterre.py -v -d -s 1234567890abcdef -p poiuytrewq \\
--execute --execute-args='signduterre.py' \\
signduterre.py - \\
'$(cat $1)' \\
'$(grep "" $1)' \\
'$(awk "{print}" $1)' \\
'$(cut -f 1-100 $1)' \\
'$(perl -ane "{print \$_}" $1)' \\
'$(python3 -c "import sys;f=open(sys.argv[1]);sys.stdout.buffer.write(f.buffer.read())" $1;)' \\
'$(ruby -e "f=open(ARGV[0]);print f.read();" $1;)'
[[[/pre]]][[[LONG]]][[[p]]]
These "commands" do not always return the same bytes (awk), or any bytes at all (grep), from a text 
file as when used with a binary file. However, if the commands can print the bytes unaltered, the 
signatures will be identical. That is, the following arguments will work on a binary file:
[[[/p]]][[[/LONG]]][[[pre make=example6]]]
# make: example6
# Example generating identical signatures of the same file in different ways, now for binary files
$ dd if=/bin/bash 2>/dev/null | \\
python3 signduterre.py -v -d -s 1234567890abcdef -p poiuytrewq \\
--execute --execute-args='/bin/bash' \\
/bin/bash - \\
'$(cat $1)' \\
'$(perl -ane "{print \$_}" $1)' \\
'$(python3 -c "import sys;f=open(sys.argv[1]);sys.stdout.buffer.write(f.buffer.read())" $1;)' \\
'$(ruby -e "f=open(ARGV[0]);print f.read();" $1;)'
[[[/pre]]][[[LONG]]][[[p]]]
Will generate the same identical signatures for [[[i]]]/bin/bash[[[/i]]], [[[i]]]STDIN[[[/i]]], [[[i]]]'$(cat /bin/bash)'[[[/i]]] etc.
There are obviously many more ways to read out the bytes from the disk or memory. The main point
being that it should be difficult to predict for an attacker which commands must be compromised
to hide changes in the system.
[[[/p]]][[[/long]]][[[p]]]
In case of a real compromised system, it is conceivable that the signatures will need to be checked using known
good statically linked programs, eg, cat or dd from a cyptographically secured container like ecryptfs or an 
encrypted loopback device. An existing signature can be tested against such statically linked programs using 
the "--file-source '$(<cmd>)'" option. In this option, the plain file path will be substituted for every 
occurence of the string '{}' in the command. If no '{}' is present in the command, the file will simply be 
appended to the command. So, '$(/bin/dd if=)' is equivalent to '$(/bin/dd if={})' and '$(/bin/cat )' is 
equivalent to '$(/bin/cat {})'. Note the trailing space in '$(/bin/cat )'.
[[[/p]]][[[pre make=example7]]]
# make: example7
# Create standard signature
$ python3 signduterre.py --passphrase SUGGESTED --salt SUGGESTED --detailed-view --verbose \\
`which python3 bash ps ls find stat lsof` 2> test-20090825_14_48-23.pwd > test-20090825_14_48-23.sdt
# Standard check
$ python3 signduterre.py --passphrase test-20090825_14_48-23.pwd --check-file test-20090825_14_48-23.sdt -v
# Example generating identical signatures checking with --file-source $(dd if=)
$ python3 signduterre.py --passphrase test-20090825_14_48-23.pwd --check-file test-20090825_14_48-23.sdt -v \\
--execute --file-source '$(dd if=)'
# Example generating identical signatures checking with --file-source $(cat ) (note the space between 'cat' and ')')
$ python3 signduterre.py --passphrase test-20090825_14_48-23.pwd --check-file test-20090825_14_48-23.sdt -v \\
--execute --file-source '$(cat )'
# Example generating identical signatures checking with --file-source $(perl -e "{open(F, \"<{}\");print <F>;};)
$ python3 signduterre.py --passphrase test-20090825_14_48-23.pwd --check-file test-20090825_14_48-23.sdt -v \\
--execute --file-source '$(perl -e "{open(F, \\"<{}\\");print <F>;};")'
[[[/pre]]][[[p]]]
The integrity of a running 'cat' command can be checked with module proc_PID that will create a signature of all 
files loaded with the 'cat' command from the information in the /proc/<pid>/maps file using the inode numbers 
(sudo only). Debugfs will read the blocks directly from the medium using the inode tables without using the filenames.
[[[/p]]][[[pre make=sudo2]]]
# make: sudo2
# Use module proc_PID to check the integrety of 'cat' and all libraries loaded with it
# Check out the workings of proc_PID.py with '$ python3 proc_PID.py'
# The actual output of the module used in the signature can be inspected with --print-textdump
$ sudo python3 signduterre.py -p poiuytrewq --salt SUGGESTED --detailed-view \\
 --verbose --execute -u root -o test-proc_PID.sdt --import proc_PID \\
'@(return proc_PID.paths("cat","inode"))' '@(return proc_PID.fileSHA("cat", mainprefix))' \\
'@(return proc_PID.inodeSHA("cat", "", mainprefix))' '@(return proc_PID.mapsSHA("cat", mainprefix))'
# Check the results
$ sudo python3 signduterre.py -p poiuytrewq  --detailed-view --verbose --execute -u root \\
 --check-file test-proc_PID.sdt --import proc_PID
[[[/pre]]][[[p]]]
Check only the Table of Contents of this file using a byte range slice
[[[/p]]][[[pre make=example8]]]
# make: example8
# Create standard signature
$ python3 signduterre.py --passphrase kdfuhgcriu --salt SUGGESTED --detailed-view --verbose \\
'signduterre.py[0o7:+136:0xf]' -o test-slices.sdt -P test-slices.pwd --print-textdump
# Standard check
$ python3 signduterre.py --passphrase kdfuhgcriu --detailed-view --verbose \\
-c test-slices.sdt  --print-textdump
[[[/pre]]][[[p]]]
The examples can be run as a makefile using make. Use one of the following commands:
[[[/p]]][[[pre]]]
# General examples, use them all
python3 signduterre.py --manual-make |make -f - example
# Linux specific examples using the second procfs example
python3 signduterre.py --manual-make |make -f - procfs2
# Examples requiring sudo, using first
python3 signduterre.py --manual-make | sudo make -f - sudo1
[[[/pre]]][[[h2]]]
Known Bugs:
[[[/h2]]][[[p]]]
- Reading files from STDIN (-) does not work if ssh:// has been used before as input for, 
  eg, file arguments, --check-file or --passphrase
[[[/p]]][[[pre make=sshbug1]]]
# make: sshbug1
# '-' stdin before ssh:// is fine
$ dd if=/bin/ps 2>/dev/null | python3.0 signduterre.py -edv -p SUGGESTED -s SUGGESTED \
/bin/ps - ssh://`whoami`@localhost/bin/ps 
# '-' stdin after ssh:// FAILs
$ dd if=/bin/ps 2>/dev/null | python3.0 signduterre.py -edv -p SUGGESTED -s SUGGESTED \
/bin/ps ssh://`whoami`@localhost/bin/ps -
[[[/pre]]][[[p]]]
- Reading URLs as file arguments should work when Python treats URLs identical 
to file descriptors. For the technically inclined: 
when:[[[br /]]]
[[[tt]]]with urllib.request.urlopen(url) as f:[[[/tt]]][[[br /]]]
works, URLs can be entered where ever file paths can be entered.. 
[[[/p]]][[[/body]]][[[/html]]]
"""
# 
license = """
Signature-du-Terroir
Construct a signature of the installed software state or check a previously made signature.

copyright 2009, R.J.J.H. van Son

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
""";
#
# Note that only release notes are put here
# See git repository for detailed change comments:
# git clone git://repo.or.cz/signduterre.git
# http://repo.or.cz/w/signduterre.git
releasenotes = """
20090926 - Opened work on v0.6a
20090926 - Added expressions to byte range slices
20090922 - Release v0.6
20090922 - Regression testing
20090916 - Completed work on import of modules and documentation thereof
20090829 - Added optional offset to [<start>:<end>:<offset>] byte slices
20090826 - Added [<start>:<end>] byte slices for every argument
20090825 - Added --source-file $(cmd) as substitute file readers 
20090820 - Release v0.6RC
20090820 - Added extensibility, or plugins, with functional @(python code) execution
20090817 - Replaced --print-hexdump by --print-textdump
20090817 - Implemented ssh:// with ${ENV}
20090814 - Release v0.5RC
20090811 - Implemented ssh tunnel for commands
20090810 - Added --file-source=PATH option
20090810 - Added ssh tunnel for all file i/o (ssh://...)
20090807 - DIFFERENT became FAIL in --check-file
20090730 - Release v0.4
20090724 - Added '--all-salts-pattern' and HTML formatting in manual
20090723 - Added URL support for all files. Does not yet work due to bug in Python 3.0
20090723 - Added '-' for STDIN
20090717 - Added --execute-args
20090716 - Release v0.3
20090713 - Added --quiet option
20090712 - moved from /dev/random to /dev/urandom
20090702 - Replaced -g with -p SUGGESTED[=N]
20090702 - Generating and testing lists of random salts
20090701 - Release v0.2
20090630 - Generating and testing random passphrases
20090630 - --execute works on $(cmd) only, nlinks in ?path and ? implied for directories
20090630 - Ported to Python 3.0

20090628 - Release v0.1b
20090628 - Added release-notes

20090626 - Release v0.1a
20090626 - Initial commit to Git
""";

#############################################################################
#                                                                           #
#               IMPORT & INITIALIZATION                                     #
#                                                                           #
#############################################################################

import sys;
import os;
import subprocess;
import stat;
import subprocess;
# if sys.stdout.isatty(): import readline;
import binascii;
import hashlib;
import re;
import time;
from optparse import OptionParser;
import base64;
import random;
import struct;
import urllib.request;
import urllib.error;

# Limit the characters that can be used in $(cmd) commands
# Only allow the escape of '$'
not_allowed_chars = re.compile('([^\w\ \.\/\"\|\;\:\,\-\$\[\]\{\}\(\)\@\`\!\*\=\\\\\<\>]|([\\\\]+([^\$\"\\\\]|$)))');

programname = "Signature-du-Terroir";
version = "0.6a";


# Open files or pipes for in/output, use mode = 'b' if binary is needed
def open_infile(filename, mode):
	if filename == '-':
		return sys.stdin;
	elif filename.lower().find('ssh://') > -1:
		match = re.search('(?i)ssh://([^/]+)/(.*)$', filename);
		tunnel_command = 'ssh '+match.group(1)+' "dd if=/'+match.group(2)+' "';
		if 'b' in mode:
		   pipe = subprocess.Popen(tunnel_command, shell=True, stdout=subprocess.PIPE);
		else:
		   pipe = subprocess.Popen(tunnel_command, shell=True, stdout=subprocess.PIPE, universal_newlines=True);
		return pipe.stdout;
	elif filename.find('://') > -1:
		print("URL:", filename, file=current_private);
		return urllib.request.urlopen(filename);
	else:
		if not os.path.isfile(filename):
			print(filename, "does not exist", file=sys.stderr)
			quit();
		return open(filename, mode);

def open_outfile(filename, mode):
	if filename == '-':
		return sys.stdout;
	elif filename.lower().find('ssh://') > -1:
		match = re.search('(?i)ssh://([^/]+)/(.*)$', filename);
		tunnel_command = 'ssh '+match.group(1)+' "dd of=/'+match.group(2)+' "';
		if 'b' in mode:
		   pipe = subprocess.Popen(tunnel_command, shell=True, stdin=subprocess.PIPE);
		else:
		   pipe = subprocess.Popen(tunnel_command, shell=True, stdin=subprocess.PIPE, universal_newlines=True);
		return pipe.stdin;
	elif filename.find('://') > -1:
		print("URL:", filename, file=current_private);
		return urllib.request.urlopen(filename);
	else :
		return open(filename, mode);

current_outfile = sys.stdout;
current_private = sys.stderr;

# Determine which kind of argument you have
def arg_is_shell_command (argument):
	return_value = False;
	if argument.startswith('$(') and argument.endswith(')'):
		return_value = argument[2:-1];
	return return_value;
	
def arg_is_env (argument): # -> Env/False
	return_value = False;
	if arg_is_shell_command(argument): return return_value;
	match = re.match(r'\$\{?([^\}]+)\}?$', argument);
	if match != None:
		return_value =  match.group(1);
	return return_value;

def arg_is_python_script (argument): # -> Script/False
	return_value = False;
	if argument.startswith('@(') and argument.endswith(')'):
		return_value = argument[2:-1];
	return return_value;
	
def arg_is_hidden (argument): # -> Exposed arg/False
	return_value = False;
	if argument.startswith('[') and argument.endswith(']'):
		return_value = argument[1:-1];
	return return_value;
	
def arg_is_tunnel (argument): # -> True/False
	return argument.find('ssh://') > -1;
	
def arg_is_stat (argument): # -> Path/False
	return_value = False;
	if argument.startswith('?'):
		return_value = argument[1:];
	return return_value;
	
def arg_is_stdin (argument): # -> True/False
	return argument == '-';
	
def arg_is_URL (argument): # -> True/False
	return re.search(r'\://', argument) and not arg_is_tunnel(argument);

def arg_is_dir (argument): # -> True/False
	return os.path.isdir(argument);

# Plain files are defined as NOT something else
def arg_is_plain_file (argument): # -> True/False
	not_file = False;
	not_file = not_file or arg_is_env(argument)
	not_file = not_file or arg_is_shell_command (argument);
	not_file = not_file or arg_is_python_script (argument);
	not_file = not_file or arg_is_tunnel (argument);
	not_file = not_file or arg_is_stdin (argument);
	# not_file = not_file or arg_is_URL (argument);
	not_file = not_file or arg_is_dir (argument);
	not_file = not_file or arg_is_stat (argument);
	
	return not not_file;

# Supportive functions
# Convert Hexadecimal, 0XFFFF, Octal, 0o7777, Binary, 0B111, and decimal, 9999, strings to int
def convertString2Int (number):
	result = 0;
	# If this is a number
	if number > ' ' and re.search(r'(?i)[^oxb0-9A-F]', number) == None:
		# Is it hexadecimal?
		if number.upper().startswith('0X') or re.search(r'(?i)[A-F]', number) != None:
			result=int(number, 16);
		# Is it octal
		elif number.upper().startswith('0O'):
			result=int(number, 8);
		# Is it binary?
		elif number.upper().startswith('0B'):
			result=int(number, 2);
		# Then it must be decimal
		else:
			result = int(number);
	return result;

#############################################################################
#                                                                           #
#               OPTION HANDLING                                             #
#                                                                           #
#############################################################################

parser = OptionParser()
parser.add_option("-s", "--salt", metavar="HEX", 
				  dest="salt", default=False,
                  help="Enter salt in cleartext. If not given, a hexadecimal salt will be suggested. The SUGGESTED[=N] keyword will cause the selection of the suggested string. N is the number of salts generated (default N=1). If N>1, all will be printed and a random one will be used to generate the signature (selection printed to STDERR).")
parser.add_option("-a", "--all-salts-pattern",
                  dest="allsalts", default=False, action="store_true", 
                  help="Use all salts in sequence, randomly replace salts with incorrect ones in the output to create a pattern of failing hashes indicated by a corresponding integer number. Depends on '--salt SUGGESTED=N'. Implies --total-only.")
parser.add_option("-p", "--passphrase", metavar="TEXT",
                  dest="passphrase", default=False,
                  help="Enter passphrase in cleartext, the keyword SUGGESTED[=N] will cause the suggested passphrase to be used. If N>1, N passphrases will be printed to STDERR and a random one will be used (selection printed to STDERR). Entering the name of an existing file (or '-' for STDIN) will cause it to be read and a random passphrase found in the file will be used (creating a signature), or they will all be used in sequence (--check-file).")
parser.add_option("-c", "--check-file",
                  dest="check", default=False, metavar="FILE", 
                  help="Check contents with the output of a previous run from file or STDIN ('-'). Except when the --quiet option is given, the previous output will contain all information needed for the program, but not the passphrase and the --execute option.")
parser.add_option("-i", "--input-file",
                  dest="input", default=False, metavar="FILE", 
                  help="Use names from FILE or STDIN ('-'), use one filename per line.")
parser.add_option("-o", "--output-file",
                  dest="output", default=False, metavar="FILE", 
                  help="Print to FILE instead of STDOUT.")
parser.add_option("--file-source",
                  dest="filesource", default=False, metavar="PATH", 
                  help="Read all files from PATH. The PATH-string is prepended to every plain file-path that is read for a signature. Remote files can be checked with 'ssh://<user>@<host>[/path]'. "
				  + "A shell command that prints out the file can be entered as '$(<cmd>)'. The filepath will be substituted for any '{}' string in the command, or appended tot the command (without white-space). "
				  + "The option overrules any File source specification in the --check-file.")
parser.add_option("-P", "--Private-file",
                  dest="private", default=False, metavar="FILE", 
                  help="Print private information (passwords etc.) to FILE instead of STDERR.")
parser.add_option("-u", "--user",
                  dest="user", default="nobody", metavar="USER", 
                  help="Execute $(cmd) as USER, default 'nobody' (root/sudo only)")
parser.add_option("-S", "--Status",
                  dest="status", default=False, action="store_true", 
                  help="For each file, add a line with unvarying file status information: st_mode, st_ino, st_dev, st_uid, st_gid, and st_size (like the '?' prefix, default False)")
parser.add_option("--Status-values",
                  dest="statusvalues", default="fmidugs", metavar="MODE", 
                  help="Status values to print for --Status, default MODE is 'fmidugs' (file, mode, inode, device, uid, gid, size). Also available (n)l(inks) a(time), (m)t(ime), and c(time).")
parser.add_option("-t", "--total-only",
                  dest="total", default=False, action="store_true", 
                  help="Only print the total hash, unsets --detailed-view (default True)")
parser.add_option("-d", "--detailed-view",
                  dest="detail", default=False, action="store_true", 
                  help="Print hashes of individual files, is unset by --total-only (default False)")
parser.add_option("-e", "--execute",
                  dest="execute", default=False, action="store_true", 
                  help="Interpret $(cmd) (default False)")
parser.add_option("--execute-args",
                  dest="executeargs", default='', metavar="ARGS", 
                  help="Arguments for the $(cmd) commands ($1 ....)")
parser.add_option("-n", "--no-execute",
                  dest="noexecute", default=False, action="store_true", 
                  help="Explicitely do NOT Interpret $(cmd)")
parser.add_option("--import",
                  dest="importfile", default='', metavar="FILE", 
                  help="Import python modules (comma separated list)")
parser.add_option("--print-textdump",
                  dest="printtextdump", default=False, action="store_true", 
                  help="Print printable character+hexadecimal dump of input bytes to STDERR for debugging purposes")
parser.add_option("--message",
                  dest="message", default='', metavar="TEXT", 
                  help="Add a comment message about the test")
parser.add_option("-m", "--manual",
                  dest="manual", default=False, action="store_true", 
                  help="Print a short version of the manual and exit")
parser.add_option("--manual-long",
                  dest="manuallong", default=False, action="store_true", 
                  help="Print the long version of the manual and exit")
parser.add_option("--manual-html",
                  dest="manualhtml", default=False, action="store_true", 
                  help="Print the manual in HTML format and exit")
parser.add_option("--manual-make",
                  dest="manualmake", default=False, action="store_true", 
                  help="Print the examples in the manual as a makefile and exit")
parser.add_option("-r", "--release-notes",
                  dest="releasenotes", default=False, action="store_true", 
                  help="Print the release notes and exit")
parser.add_option("-l", "--license",
                  dest="license", default=False, action="store_true", 
                  help="Print license text and exit")
parser.add_option("-v", "--verbose",
                  dest="verbose", default=False, action="store_true", 
                  help="Print more information on output")
parser.add_option("-q", "--quiet",
                  dest="quiet", default=False, action="store_true", 
                  help="Print minimal information (hide filenames). If the output is used with --check-file, the command line options and arguments must be repeated.")

(options, check_filenames) = parser.parse_args();


# Start with opening any non-default output files
my_output = False;
if options.output:
	current_outfile = open_outfile(options.output, 'w');
	my_output = options.output;
	
my_private = False;
if options.private:
	current_private = open_outfile(options.private, 'w');
	my_private = options.private;
	
print("# Program: "+programname + " version " + version, file=current_outfile);
print("#", time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()), "("+time.tzname[0]+")\n", file=current_outfile);

# Print license
if options.license:
	print (license, file=sys.stderr);
	exit(0);
# Print manual
if options.manual or options.manuallong:
	cleartext_manual = re.sub(r"(?i)\[\[\[\s*(/?)\s*LONG\s*\]\]\]", r'[[[\1LONG]]]', manual);
	if not options.manuallong:
		currentstart = cleartext_manual.find('[[[LONG]]]');
		while currentstart > -1:
			currentend = cleartext_manual.find('[[[/LONG]]]', currentstart)+len('[[[/LONG]]]');
			(firstpart, secondpart) = cleartext_manual.split(cleartext_manual[currentstart:currentend]);
			cleartext_manual = firstpart+secondpart;
			currentstart = cleartext_manual.find('[[[LONG]]]'); 
	htmltags = re.compile('\[\[\[[^\]]*\]\]\]');
	cleartext_manual = htmltags.sub('', cleartext_manual);
	print (cleartext_manual, file=sys.stdout);
	exit(0);
# Print HTML manual
if options.manualhtml:
	protleftanglesbracks = re.compile('\<');
	protrightanglesbracks = re.compile('\>');
	leftanglesbracks = re.compile('\[\[\[');
	rightanglesbracks = re.compile('\]\]\]');
	html_manual = re.sub(r"(?i)\[\[\[\s*(/?)\s*LONG\s*\]\]\]", '', manual);
	html_manual = protleftanglesbracks.sub('&lt;', html_manual);
	html_manual = protrightanglesbracks.sub('&gt;', html_manual);
	html_manual = leftanglesbracks.sub('<', html_manual);
	html_manual = rightanglesbracks.sub('>', html_manual);
	print (html_manual, file=sys.stdout);
	exit(0);
# Print manual examples as makefile
if options.manualmake:
	make_manual = re.sub("\$ ", "\t", manual);
	make_manual = re.sub("\#", "\t#", make_manual);
	make_manual = re.sub(r"\\\s*\n", '', make_manual);
	make_manual = re.sub(r"\$", r'$$', make_manual);
	# Protect "single" [ brackets
	make_manual = re.sub(r"(^|[^\[])\[([^\[]|$)", r"\1&#91;\2", make_manual);
	extrexamples = re.compile(r"\[\[\[pre\s+make\=?([a-zA-Z]*)([0-9]*)\s*\]\]\]\n([^\[]*)\n\[\[\[/pre\s*\]\]\]", re.IGNORECASE|re.MULTILINE|re.DOTALL);
	exampleiter = extrexamples.finditer(make_manual);
	makefile_list = [];
	group_list={};
	group_list['all'] = "all: ";
	for match in exampleiter:
		# We had to convert any '[' in the command. Now convert them back.
		command_text = re.sub(r"\&\#91\;", '[', match.group(3));
		makefile_list.append(match.group(1)+match.group(2)+":\n"+command_text);
		if len(match.group(2)) > 0:
			if not match.group(1) in group_list.keys(): 
				group_list[match.group(1)] = match.group(1)+": ";
				group_list['all'] += match.group(1)+" ";
			group_list[match.group(1)] += match.group(1)+match.group(2)+" ";
		else:
			group_list['all'] += match.group(1)+" ";
	print("help: \n\t@echo 'Use \"make -f - "+re.sub(':', '', group_list['all'])+"\"'", file=sys.stdout);
	for group in group_list:
		print(group_list[group]+"\n", file=sys.stdout);
	makefile_list.sort()
	previous_cat = 'NOT A VALUE';
	for line in makefile_list:
		(category, commands) = line.split(':\n');
		if category != previous_cat:
			previous_cat = category;
			print("\n"+previous_cat+":", file=sys.stdout);
		print(commands, file=sys.stdout);
	# Clean option
	print("\nclean:\n\trm test-*.sdt test-*.pwd", file=sys.stdout);
	exit(0);
# Print release notes
if options.releasenotes:
	print ("Version: "+version, file=sys.stderr);
	print (releasenotes, file=sys.stderr);
	exit(0);

my_salt = options.salt;
my_allsalts = options.allsalts;
my_passphrase = options.passphrase;
my_check = options.check;
my_status = options.status;
my_statusvalues = options.statusvalues;
my_verbose = options.verbose and not options.quiet;
my_quiet = options.quiet;
execute = options.execute;
execute_args = options.executeargs;
if options.noexecute: execute = False;
input_file = options.input;
my_filesource = options.filesource;
if my_filesource: print("File source: '"+my_filesource+"'\n", file=current_outfile);
my_message = options.message;
my_importfiles = options.importfile;
if my_importfiles:
	for module_name in my_importfiles.split(','):
		var_module = __import__(module_name);
	print("Import: '"+my_importfiles+"'\n", file=current_outfile);


# Set total-only with the correct default
total_only = True;
total_only = not options.detail;
if options.total: total_only = options.total;
if my_allsalts: total_only = my_allsalts; # All alts pattern only sensible with total-only
if my_check: total_only = False;

my_user = options.user;
# Things might be executed as another user
user_change = '';
if os.getuid() == 0:
	user_change = 'sudo -H -u '+my_user+' ';
	if not my_quiet: print("User: "+my_user, file=current_outfile);

# Execute option
if execute:
	text_execute = "True";
else:
	text_execute = "False";

if execute and not my_quiet: 
	print("Execute system commands: "+text_execute+"\n", file=current_outfile);
	if execute_args != '': print("Execute arguments: '"+execute_args+"'\n", file=current_outfile);

# --quiet option
if my_quiet: print("Quiet: True\n", file=current_outfile);

# --Status-values option
if my_statusvalues != 'fmidugs': print("Status-values: '"+my_statusvalues+"'\n", file=current_outfile);

# --message option
if len(my_message) > 0: print("Message: '''"+my_message+"'''\n", file=current_outfile);

#############################################################################
#                                                                           #
#               ARGUMENT PROCESSING                                         #
#                                                                           #
#############################################################################

# Measure time intervals
start_time = time.time();

dev_random = open("/dev/urandom", 'rb');

# Read the check file
passphrase_list = [];
salt_list = [];
check_hashes = {};
total_hash_list = [];
if my_check:
	highest_arg_used = 0;
	print("# Checking: "+my_check+"\n", file=current_outfile);
	arg_list = check_filenames;
	check_filenames = [];
	with open_infile(my_check, 'r') as c:
		for line in c:
			match = re.search(r"Execute system commands:\s+(True|False)", line);
			if match != None:
				# Uncomment the next line if you want automatic --execute from the check-file (DANGEROUS)
				# execute = match.group(1).upper() == 'TRUE';
				continue;
				
			match = re.search(r"Execute arguments:\s+\'([\w\$\s\-\+\/]*)\'", line);
			if match != None:
				execute_args = match.group(1);
				continue;
				
			match = re.search(r"Quiet:\s+(True|False)", line);
			if match != None:
				my_quiet = match.group(1).upper() == 'TRUE';
				if my_quiet: my_verbose = False;
				continue;
			
			match = re.search(r"File source:\s+\'([\w\ \-\+\`\"\[\]\{\}\@\$\=\:\/\(\)\<\>\.\,\;\?\*\&\^\%\\]+)\'", line);
			if not my_filesource and match != None:
				my_filesource = match.group(1);
				continue;
				
			match = re.search(r"Salt\s*\+\s*TOTAL HASH\s*\:\s+\'([\w]*)\'\s+\'([\w]*)\'", line);
			if match != None:
				salt_list.append(match.group(1));
				total_hash_list.append(match.group(2));
				my_allsalts = True; # Salt+TOTAL HASH imples all-salts-pattern
				continue;
				
			match = re.search(r"Salt\:\s+\'([\w]*)\'", line);
			if match != None:
				salt_list.append(match.group(1));
				continue;
				
			match = re.search("Salt\s*\+\s*TOTAL HASH\s*\:\s+\'([\w]+)\'\s+\'([a-f0-9]+)\'", line);
			if match != None:
				salt_list.append(match.group(1));
				total_hash_list.append(match.group(2));
				continue;
				
			match = re.search("User\:\s+\'([\w]*)\'", line);
			if match != None:
				# Uncomment the next line if you want automatic --user from the check-file (DANGEROUS)
				# my_user = match.group(1);
				continue;
				
			match = re.search("Passphrase\:\s+\'([^\']*)\'", line);
			if match != None:
				passphrase_list.append(match.group(1));
				continue;
				
			match = re.search("Status-values\:\s+\'([\w]*)\'", line);
			if match != None:
				my_statusvalues = match.group(1);
				continue;
				
			match = re.search(r"Import\:\s+\'([^\']*)\'", line);
			if match != None:
				my_importfiles = match.group(1);
				continue;
				
			match = re.search("Message\:\s+\'\'\'(.*)$", line);
			if match != None:
				my_message = match.group(1);
				my_message = my_message[0:my_message.find("'''")];
				print("Message: '''"+my_message+"'''\n", file=current_outfile);
				continue;
				
			match = re.search("^\s*([a-f0-9]+)\s+\*(TOTAL HASH)\s*$", line)
			if match != None:
				total_hash_list.append(match.group(1));
				continue;
				
			match = re.search("^\s*([a-f0-9\-]+)\s+\*\[([0-9]+)\]\s*$", line)
			if match != None:
				filenumber = int(match.group(2));
				if filenumber > highest_arg_used: highest_arg_used = filenumber;
				# Watch out, arguments count from 0
				check_filenames.append(arg_list[filenumber - 1]);
				check_hashes['['+match.group(2)+']'] = match.group(1);
				continue;

			match = re.search("^\s*([a-f0-9\-]+)\s+\*(.*)\s*$", line)
			if match != None:
				check_filenames.append(match.group(2));
				# Catch --execute error as early as possible
				if match.group(2).startswith('$(') and not execute: 
					error_message = "Executable argument \'"+match.group(2)+"\' only allowed with the --execute flag";
					print (error_message, file=sys.stderr);
					if not sys.stdout.isatty(): print(error_message, file=current_outfile);
					exit(0);
				check_hashes[match.group(2)] = match.group(1);
				continue;
	for i in range(highest_arg_used, len(arg_list)):
	    check_filenames.append(arg_list[i]);
	    check_hashes['['+str(i+1)+']'] = (64*'-');

# Read input-file
if input_file:
	with open_infile(input_file, 'r') as i:
		for line in i:
			# Clean up filename
			current_filename = line.lstrip(' \n').rstrip(' \n');
			check_filenames.append(current_filename);
			if my_check: check_hashes['['+str(i+1)+']'] = (64*'-');

stat_list = [];
for x in check_filenames:
	if os.path.isdir(x):
		x = '?'+x;
	if my_status and not x.startswith(('?', '$')):
		stat_list.append('?'+x);
	stat_list.append(x);
check_filenames = stat_list;

# Seed Pseudo Random Number Generator
seed = dev_random.read(16);
random.seed(seed);

# Read suggested salts from /dev/(u)random if needed
if my_salt:
	if my_salt.startswith('SUGGESTED'):
		N=1;
		match = re.search("([0-9][0-9]*)$", my_salt);
		if match != None:
			N = int(match.group(1));
		for i in range(0,N):
			salt = dev_random.read(8);
			salt_list.append(str(binascii.hexlify(salt), 'ascii'));
	else:
		salt_list.append(my_salt);
elif len(salt_list) == 0:
	salt = dev_random.read(8);
	sys.stderr.write("Enter salt (suggest \'"+str(binascii.hexlify(salt), 'ascii')+"\'): ");
	new_salt = input();
	if not new_salt: new_salt = str(binascii.hexlify(salt), 'ascii');
	salt_list.append(new_salt);

# If not combining salts with TOTAL HASH, print salts now
if not my_allsalts:
	for my_salt in salt_list:
		print("Salt: \'"+my_salt+"\'", file=current_outfile);

# Get passphrase
if my_passphrase and(my_passphrase == '-' or my_passphrase.find("://") > -1 or os.path.isfile(my_passphrase)):
    with open_infile(my_passphrase, 'r') as file:
        for line in file:
	        match = re.search("Passphrase\:\s+\'([^\']*)\'", line);
	        if match != None:
		        passphrase_list.append(match.group(1));
elif not my_passphrase and len(passphrase_list) == 0:
	suggest_passphrase = dev_random.read(16);
	suggest_string = "";
	if not my_check:
	   suggest_string =  "(suggest \'"+str(base64.b64encode(suggest_passphrase), 'ascii').rstrip('=')+"\')";
	sys.stderr.write("Enter passphrase"+suggest_string+": ");
	# How kan we make this unreadable on input?
	current_passphrase = input();
	if not current_passphrase:
	    current_passphrase = str(base64.b64encode(suggest_passphrase), 'ascii').rstrip('=');
	    print("Passphrase: \'"+current_passphrase+"\'", file=current_private);
	passphrase_list.append(current_passphrase);
elif my_passphrase.startswith('SUGGESTED'):
    N = 1;
    match = re.search("([0-9][0-9]*)$", my_passphrase);
    if match != None:
        N = int(match.group(1));
    j = int(random.random()*N);
    for i in range(0, N):
	    suggest_passphrase = dev_random.read(16);
	    current_passphrase = str(base64.b64encode(suggest_passphrase), 'ascii').rstrip('=');
	    print("Passphrase: \'"+current_passphrase+"\'", file=current_private);
	    passphrase_list.append(current_passphrase);
else:
    passphrase_list.append(my_passphrase);

selected_salt = 1;
fail_fraction = 0.5;
if not my_check:
	if len(passphrase_list) > 1:
		j = int(random.random()*len(passphrase_list));
		passphrase_list = [passphrase_list[j]];
		print("# Selected passphrase:", j+1, file=current_private);
	if len(salt_list) > 1:
		j = int(random.random()*len(salt_list));
		# Make sure at least 1 salt will match and print the selection if only one is used
		selected_salt = j+1;
		if not my_allsalts:
			salt_list = [salt_list[selected_salt-1]];
			print("# Selected salt:", selected_salt, file=current_private);
		else:
			salt_N = len(salt_list);
			fail_fraction = (salt_N/2.0)/(salt_N - 1);
	else:
		fail_fraction = 0;

# Close /dev/(u)random
dev_random.close;

#############################################################################
#                                                                           #
#               SIGNATURE CREATION AND CHECKING                             #
#                                                                           #
#############################################################################

end_time = time.time();
print("# Preparation time:", end_time - start_time, "seconds\n", file=current_outfile);

pnum = 1;
snum = 1;
corrpnum = 0;
corrsnum = 0;
matched_salt_pattern = -1;
salt_pattern_number = -1;

for my_passphrase in passphrase_list:
	snum = 1;
	# Initialize salt pattern
	if my_allsalts: 
		salt_pattern_number = 0;
		current_salt_power = 1;

	for my_salt in salt_list:
		print("# Start signature: ", end='', file=current_outfile);
		if len(passphrase_list) > 1: print("passphrase -", pnum, end='', file=current_outfile);
		if len(salt_list) > 1: print(" salt -", snum, end='', file=current_outfile);
		print("", file=current_outfile);
		
		# Should everything be printed?
		print_verbose = my_verbose and not (my_allsalts and snum > 1);
		
		file_argnum = 0;
		start_time = time.time();
		# Construct the passphrase hash
		passphrase = hashlib.sha256();
		
		passphrase.update(bytes(my_salt, encoding='ascii'));
		passphrase.update(bytes(my_passphrase, encoding='ascii'));
		
		# Create prefix which is a hash of the salt+passphrase
		prefix = passphrase.hexdigest();
      
		##########################################
		#                                        #
		# Create signature and write output      #
		#                                        #
		##########################################
		
		totalhash = hashlib.sha256();
		totalhash.update(bytes(prefix, encoding='ascii'));
		for org_filename in check_filenames:
			# Create file hash object
			filehash = hashlib.sha256();
			filehash.update(bytes(prefix, encoding='ascii'));
			# Remove []
			filename = org_filename;
			if org_filename.startswith('[') and org_filename.endswith(']'):
				filename = filename[1:len(filename)-1];
			# Select input bytes to use for signature
			input_start = 0;
			input_length = 0;
			if filename.endswith(']'):
				input_offset = 0;
				# Find the matching open bracket
				finalCloseBracket = filename.rfind(']', 0, len(filename));
				closeBracket = finalCloseBracket;
				openBracket = filename.rfind('[', 0, closeBracket);
				while filename.rfind(']', openBracket, closeBracket) > -1:
					openBracket = filename.rfind('[', 0, openBracket);
					closeBracket = filename.rfind(']', openBracket, closeBracket);
				interval = filename[openBracket+1:finalCloseBracket];
				filename = filename[0:openBracket];
				(new_start, new_end, new_offset) = ('', '', '');
				# split interval
				intervalList = [];
				interval = interval.lstrip(' ').rstrip(' ')
				while len(interval) > 0:
					if interval.endswith(')'):
						closeBracket = len(interval) - 1;
						openBracket = interval.rfind('(', 0, closeBracket);
						while interval.rfind(')', openBracket, closeBracket) > -1:
							openBracket = interval.rfind('(', 0, openBracket);
							closeBracket = interval.rfind(')', openBracket, closeBracket);
						while openBracket > 0 and interval[openBracket-1:openBracket] != ':':
							openBracket -= 1;
						intervalList.append(interval[openBracket:len(interval)]);
						interval = interval[0:openBracket-1];
					elif interval.rfind(':') > -1:
						colonPoint = interval.rfind(':');
						intervalList.append(interval[colonPoint+1:len(interval)]);
						interval = interval[0:colonPoint];
					else:
						intervalList.append(interval);
						interval = "";
				# Add missing offset
				intervalList.reverse();
				if len(intervalList) < 3: intervalList.append('0');
				(new_start, new_end, new_offset) = intervalList;
				if new_end.lstrip(' ').startswith('+'): new_end = new_start+new_end;
				if len(new_start) > 0 and len(new_end) > 0:
					# Execute priviledges or not even builtins
					if execute:
						input_start = eval(new_start);
						input_end = eval(new_end);
						input_offset = eval(new_offset);
					else:	# not even builtins
						input_start = eval(new_start, {"__builtins__":None}, {});
						input_end = eval(new_end, {"__builtins__":None}, {});
						input_offset = eval(new_offset, {"__builtins__":None}, {});
					input_length = input_end - input_start;
					if input_start >=0 and input_offset > 0 : input_start += input_offset;
			
			# Preprocessing filename to include "external" file sources
			if my_filesource:
				# Insert different file reader as a shell command
				if arg_is_shell_command(my_filesource) and arg_is_plain_file(filename):
					current_source_command = arg_is_shell_command(my_filesource);
					if current_source_command.find('{}') > -1:
						current_source_command = re.sub(r'\{\}', filename, current_source_command);
					else:
						current_source_command += filename;
					filename = "$("+current_source_command+")";
				# Insert remote ssh:// if necessary and not allready a tunnel
				elif arg_is_tunnel(my_filesource) and not arg_is_tunnel(filename):
					if arg_is_env(filename) :
						match = re.search(r"(?i)ssh://([^/]+)", my_filesource);
						if match != None: filename = "${ssh://"+match.group(1)+"/"+arg_is_env(filename)+"}";
					elif arg_is_shell_command(filename):
						match = re.search(r"(?i)ssh://([^/]+)", my_filesource);
						if match != None: filename = "$(ssh://"+match.group(1)+"/"+arg_is_shell_command(filename)+")";
					elif arg_is_plain_file(filename):
						filename = my_filesource+filename;
			# Handle file tunnels: convert 'ssh://<user>@<host>/<path>' to 
			# $(ssh://<user>@<host>/dd if=/<path>)
			if arg_is_tunnel(filename) and filename.startswith("ssh://"):
				match = re.search(r"(?i)ssh://([^/]+)/(.*)$", filename);
				if match != None:
					host = match.group(1);
					path = match.group(2);
					if arg_is_stat(path):
						print("Error: status not possible in tunnels - "+filename);					
					else:
						if input_start > 0 or input_length > 0:
							filename = '$(ssh://'+host+'/dd if=/'+path+' bs=1 skip='+str(input_start)+' count='+str(input_length)+')';
							# The start and end have been dealt with, remove them
							input_start = 0;
							input_length = 0;
						else:
							filename = '$(ssh://'+host+'/dd if=/'+path+')';
				print(filename);
			# Use python @() constructs
			orig_command_filename = filename;
			if arg_is_python_script(filename):
				if not execute: 
					error_message = "Executable argument \'"+filename+"\' only allowed with the --execute flag";
					print (error_message, file=sys.stderr);
					exit(1);
				# Check for dangerous constructs
				if re.search(r'\bimport\b', filename):
				   print("Error: Import statement not allowed, please use --import option", file=sys.stderr);
				   exit(1);
				# Construct a code wrapper around the user supplied code
				script_input = arg_is_python_script(filename);
				statement_string = "";
				if my_importfiles: statement_string += "import "+re.sub(',', ', ', my_importfiles)+';\nglobal mainprefix;\n';
				statement_string += "def sdt_exec_code():\n\t"+re.sub(r'\\n', "\n\t", re.sub(r'\\t', '\t', script_input));
				# Compile and execute code in a limited namespace
				user_code = compile(statement_string+"\nsdt_export_result = sdt_exec_code()\n", '<user code>', 'exec');
				userdict = {'sdt_export_result' : None};
				userdict['mainprefix'] = prefix;
				argvlist = [];
				argvlist.append(os.getpid());
				for value in execute_args.split():
				   argvlist.append(value);
				userdict['argv'] = argvlist;
				# Execute code
				exec(user_code, userdict);
				# Use result
				b = None;
				if userdict['sdt_export_result']:
				   b = userdict['sdt_export_result'];
				else:
				   b = None;
				   print("Error: '"+filename+"' did not deliver any result", file=sys.stderr);
				   exit(1);
				if input_start > 0:
					b = b[input_start:];
				if input_length > 0:
					b = b[0:input_length];
				filehash.update(bytes(b, encoding='utf8'));
				if options.printtextdump: # For debugging commands
				   print(str(b));
			# Use system variables and commands
			# ${ENV} environment variables
			if arg_is_env(filename):
				current_var = not_allowed_chars.sub(" ", arg_is_env(filename));
				if print_verbose:
					print("# echo $"+ current_var, file=current_outfile);
				# Redirect env query to other system
				if current_var.startswith("ssh://"):
					match = re.search(r"(?i)(ssh://[^/]+/)(.*)$", current_var);
					if match != None:
						current_ssh = match.group(1);
						current_command = r"echo -n ${"+match.group(2)+"}";
						filename = '$('+current_ssh+current_command+')';
				# Current system
				else:
				   b = os.environ[current_var];
				   if input_start > 0:
				   	b = b[input_start:];
				   if input_length > 0:
				   	b = b[0:input_length];
				   filehash.update(bytes(b, encoding='utf8'));
				   if options.printtextdump: # For debugging commands
				   	print(str(b));
			# Commands $(command)
			if arg_is_shell_command(filename):
				if not execute : 
					error_message = "Executable argument \'"+filename+"\' only allowed with the --execute flag";
					print (error_message, file=sys.stderr);
					exit(0);
				# Clean up command
				current_command = not_allowed_chars.sub(" ", arg_is_shell_command(filename));
				# Expand remote ssh://
				current_host = None;
				current_executable = None;
				current_args = execute_args;
				if current_command.startswith("ssh://"):
					match = re.search(r"(?i)ssh://([^/]+)/(.*)$", current_command);
					if match != None:
						current_host = match.group(1);
						current_command = match.group(2);
						# Protect $, ",  and backslashes
						current_command = re.sub(r'\\', r'\\', current_command);
						current_command = re.sub(r'\$', r'\$', current_command);
						current_executable = "/usr/bin/ssh";
						current_args = re.sub(r'\$', r'\$', current_args);
						current_args = re.sub(r'\"', r'\"', current_args);
				# Create command line
				current_command_line = user_change+"bash --restricted -c \'"+current_command+"\' "+str(os.getpid())+" "+current_args;
				# Add ssh command
				if current_executable:
					current_command_line = re.sub(r'\"', r'\\"', current_command_line);
					current_command_line = current_executable+' '+current_host+' "'+current_command_line+'"';
				# Print command
				if print_verbose:
					print("#", current_command_line, file=current_outfile);
				# Spawn command and open a pipe to the output
				pipe = subprocess.Popen(current_command_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
				if input_start > 0:
					pipe.stdout.read(input_start);
				bytes_processed = 0;
				for b in pipe.stdout:
					if input_length > 0:
						if bytes_processed >= input_length:
							break;
						elif bytes_processed + len(b) <= input_length:
							bytes_processed += len(b);
						else:
							b = b[0:(input_length - bytes_processed)];
							bytes_processed = input_length;
					if type(b).__name__ == 'str': 
						b = bytes(b, encoding='utf8');
					filehash.update(b);
					if options.printtextdump: # For debugging commands
						print(str(b));
				# See whether there was an error
				pipe.wait();
				if pipe.returncode:
					error_message = pipe.stderr.read();
					print('$('+current_command+')', "\n", str(error_message, encoding='UTF8'), file=sys.stderr);
					exit(pipe.returncode);
			# stat() meta information
			if arg_is_stat(filename):
				if not os.path.exists(arg_is_stat(filename)): 
					print(filename, "does not exist", file=sys.stderr)
					quit();
				filestat = os.stat(arg_is_stat(filename));
				if my_statusvalues == "": my_statusvalues = 'fmidlugs'
				b = "";
				if 'f' in my_statusvalues:
					b += 'stat('+filename.lstrip('?')+') = '
				b += '[';
				if 'm' in my_statusvalues:
					b += 'st_mode='+str(oct(filestat.st_mode))+', ';
				if 'i' in my_statusvalues:
					b += 'st_ino='+str(filestat.st_ino)+', ';
				if 'd' in my_statusvalues:
					b += 'st_dev='+str(filestat.st_dev)+', '
				if 'l' in my_statusvalues:
					b += 'st_nlink='+str(filestat.st_nlink)+', '
				if 'u' in my_statusvalues:
					b += 'st_uid='+str(filestat.st_uid)+', '
				if 'g' in my_statusvalues:
					b += 'st_gid='+str(filestat.st_gid)+', '
				if 's' in my_statusvalues:
					b += 'st_size='+str(filestat.st_size)+', '
				if 'a' in my_statusvalues:
					b += 'st_atime='+str(filestat.st_atime)+', '
				if 't' in my_statusvalues:
					b += 'st_mtime='+str(filestat.st_mtime)+', '
				if 'c' in my_statusvalues:
					b += 'st_ctime='+str(filestat.st_ctime);
					
				b = b.rstrip(', ') + ']';
				# Not sure whether this makes sense at all
				if input_start > 0:
					b = b[input_start:];
				if input_length > 0:
					b = b[0:input_length];
				filehash.update(bytes(b, encoding='utf8'));
				if print_verbose:
					print ("# "+ b, file=current_outfile);
				if options.printtextdump: # For debugging commands
					print(str(b));

			# STDIN
			if arg_is_stdin(filename):
				total_bytes = 0;
				if input_start > 0:
					sys.stdin.buffer.read(input_start);
				bytes_processed = 0;
				for b in sys.stdin.buffer:
					if input_length > 0:
						if bytes_processed >= input_length:
							break;
						elif bytes_processed + len(b) <= input_length:
							bytes_processed += len(b);
						else:
							b = b[0:(input_length - bytes_processed)];
							bytes_processed = input_length;
					total_bytes += len(b);
					if type(b).__name__ == 'str': 
						b = bytes(b, encoding='utf8');
					filehash.update(b);
					if options.printtextdump: # For debugging commands
						print(str(b));
				if total_bytes == 0: 
				   print("ERROR: No bytes read from STDIN. Processing aborted.", file=sys.stderr);
				   quit(1);
			
			# Use plain file
			if arg_is_plain_file(filename):
				# Open and read the file
				with open_infile(filename, 'rb') as file:
					if input_start > 0:
						file.seek(input_start);
					bytes_processed = 0;
					for b in file:
						if input_length > 0:
							if bytes_processed >= input_length:
								break;
							elif bytes_processed + len(b) <= input_length:
								bytes_processed += len(b);
							else:
								b = b[0:(input_length - bytes_processed)];
								bytes_processed = input_length;
						if type(b).__name__ == 'str': 
							b = bytes(b, encoding='utf8');
						filehash.update(b);
						if options.printtextdump: # For debugging commands
							print(str(b));
			
			# Print the signature of the current argument
			current_digest = filehash.hexdigest();
			print_name = org_filename;
			if my_quiet or arg_is_hidden(org_filename):
			    file_argnum += 1;
			    print_name = '['+str(file_argnum)+']';
			current_hash_line = current_digest+" *"+print_name
			# Add current signature to total signature (including the argument!)
			totalhash.update(bytes(current_hash_line, encoding='ascii'));
			
			# Be careful to use this ONLY after totalhash has been updated!
			if total_only: 
			    current_hash_line = (len(current_digest)*'-')+" *"+print_name;
			
			# Write output
			if not my_check:
				if not (my_quiet and total_only) and not (my_allsalts and snum > 1):
				    print(current_hash_line, file=current_outfile);
			elif not (my_quiet or my_allsalts):
				if check_hashes[print_name] == (len(current_digest)*'-'):
					# Suppress redundant output of empty, ----, lines
					if snum <= 1 and pnum <= 1: 
						print(check_hashes[print_name]+" *"+print_name, file=current_outfile);
				elif current_digest != check_hashes[print_name]:
					print("FAILED: "+current_hash_line, file=current_outfile);
				else:
					print("ok"+" *"+print_name, file=current_outfile);
		
		# Handle total hash
		current_total_digest = totalhash.hexdigest();
		# Write (in)correct salts with the TOTAL HASH
		if my_allsalts:
			output_salt = my_salt;
			j = random.random();
			# Randomly create an incorrect salt for failed output
			if not my_check:
				if j < fail_fraction and snum != selected_salt:
					salt = dev_random.read(8);
					output_salt = str(binascii.hexlify(salt), 'ascii');
				else:
					salt_pattern_number += current_salt_power;
			current_total_digest_line = "Salt+TOTAL HASH: '"+output_salt+"' '"+current_total_digest+"'";
		else: # Standard TOTAL HASH line
			current_total_digest_line = current_total_digest+" *"+"TOTAL HASH";
		end_time = time.time();
		print("# \n# Total hash - Time to completion:", end_time - start_time, "seconds", file=current_outfile);
		total_hash_num = 0;
		if my_allsalts: total_hash_num = snum-1; # Current TOTAL HASH number of more are used
		if not my_check:
			print(current_total_digest_line+"\n", file=current_outfile);
		elif current_total_digest != total_hash_list[total_hash_num]:
			if not my_allsalts: print("FAILED: "+current_total_digest_line+"\n", file=current_outfile);
		else:
			if my_allsalts: salt_pattern_number += current_salt_power;  # Update salt bit pattern
			match_number = "";
			if len(passphrase_list) > 1 or len(salt_list): match_number = " #"
			if len(passphrase_list) > 1: match_number += " passphrase no: "+str(pnum);
			if len(salt_list) > 1: match_number += " salt no: "+str(snum);
			if not my_allsalts: print("OK"+" *"+"TOTAL HASH"+match_number+"\n", file=current_outfile);
			corrsnum = snum;
			corrpnum = pnum;
		snum += 1;
		if my_allsalts: current_salt_power *= 2;  # Update current bit position in salt pattern
	if my_check and corrpnum == pnum: matched_salt_pattern = salt_pattern_number;
	pnum += 1;
        
if my_check and len(passphrase_list) > 1:
	if corrpnum > 0:
		print("Passphrase entry:",corrpnum,"matched", file=current_outfile);
	else:
		print("No passphrase entry matched!", file=current_outfile);
if my_check and (not my_allsalts) and len(salt_list) > 1:
	if corrpnum > 0:
		if corrsnum > 0:
			print("Salt entry:",corrsnum,"matched", file=current_outfile);
		else:
			print("No salt entry matched!", file=current_outfile);
	else:
		print("No entry matched", file=current_outfile);
# Print salt bit patterns
elif my_check and my_allsalts:
	print("Salt pattern number:", matched_salt_pattern, file=current_outfile);
elif not my_check and my_allsalts:
	print("# Salt pattern number:", salt_pattern_number, file=current_private);

# Close output files if necessary
if my_output and my_output != '-':
	current_outfile.close();
if my_private and my_private != '-':
	current_private.close();
