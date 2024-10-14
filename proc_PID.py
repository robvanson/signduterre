# proc_PID
# 
# Signature-du-Terroir module to handle /proc/<pid>
#
# Help text
help_text = """
Start a command that will stall on reading STDIN, eg, grep, cat, dd, perl, python, ruby, bash.
Or enter the PID of an existing, running, task.

Use /proc/<pid>/{exe, maps} to collect information, eg, all loaded libraries, the file paths, 
inode numbers, and mem addresses. Then use dbugfs to read out the inode numbers. The results can be
hashed with sha512sum (recommended) or returned raw.

System commands
reset()              : Empty cache, next call to get_info() will run the command
get_info(command)    : Run command and read all info, if command differs from current_command
get_info(PID)        : Read all info from running process PID, if command differs from current pid

Values
current_command      : Command (path) for which the current values are relevant
address_list         : The start, end, and offset addresses for each file (path) loaded (/proc/<pid>/maps). Ie, each address_list[path] is a list of address lists.
map_list             : Information for /proc/<pid>/maps - [path]={'permissions', 'device', 'inode'}
path_list            : All files (paths) loaded for the current command (/proc/<pid>/maps).
mapsfile             : The first file path in /proc/<pid>/maps, ie, the file with the command
file_system          : Device, /dev/..., on which mapsfile is stored
exe                  : The path to which /proc/<pid>/exe links

Methods returning contents of /proc/<pid>/maps as text tables
paths (command, key_list) : A table of all paths with one or more of ['permissions', 'device', 'inode'] (inode is default)

The following methods return the SHA512 hash. They use the prefix to start the hash
Files are read using the inode numbers with debugfs (sudo only)
inodeSHA (command, file, prefix): The file contents based on the inode number in /proc/<pid>/maps, if 'file' is '', the mapsfile is used. 
mapsSHA (command, prefix)    : All files in /proc/<pid>/maps, based on inode number

For debugging purposes:
fileSHA (command, prefix)    : Simple file read from disk using mapsfile
exeSHA (command, prefix)     : File read using the exe link

The following methods return the WHOLE, binary file content
Files are read using the inode numbers with debugfs (sudo only)
inode (command, file): The file based on the inode number in /proc/<pid>/maps
maps (command)       : All files in /proc/<pid>/maps, based on inode number

For debugging purposes:
file (command)       : Simple file read from disk using mapsfile
exe (command)        : File read using the exe link

Standalone use:
> python3 proc_PID.py [path1 ....]
Will run for each path:
fileSHA (path)
exeSHA (path)
inodeSHA (path, '')
mapsSHA (path)

===================
proc_PID
Signature-du-Terroir module to access /proc/<pid> pseudo files.

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
"""

import sys;
import os;
import subprocess;
import hashlib;
import re;
import time;

# Basic support routines
def create_process (command):
	devnull = open('/dev/null', 'w');
	return subprocess.Popen(command.split(), stdin = subprocess.PIPE, stdout = devnull, stderr = subprocess.PIPE, shell=False, universal_newlines=False);
	
def kill_process (process):
	process.stdin.close();
	errormess = process.stderr.read();
	if len(errormess) > 0: print(str(errormess), file=sys.stderr);

# Define values
file_system = None;
address_list= {};
map_list = {};
path_list = [];
mapsfile = None;
exe = None;
current_command = '';

# Determine the file system on which a file is stored (using df)
def get_filesystem(path):
	command = 'df -h '+path+' |tail -1';
	process = subprocess.Popen(command, stdin = None, stdout = subprocess.PIPE, stderr = sys.stderr, shell=True, universal_newlines=True);
	df_output = process.stdout.read();
	return df_output.split()[0];

def get_debugfs_command (path, inode):
	if os.getuid() != 0:
		print("ERROR: must be root to read disk blocks\n", file=sys.stderr);
		exit(1);
	file_system = get_filesystem(path);
	return "/sbin/debugfs -f - "+file_system+" -R 'cat <"+str(inode)+">'";

def reset ():
	global file_system;
	global address_list;
	global map_list;
	global path_list;
	global mapsfile;
	global exe;
	global current_command;
	file_system = None;
	address_list = {};
	map_list = {};
	path_list = [];
	mapsfile = None;
	exe = None;
	current_command = '';

# Start command and read info from /proc/<pid>/
# Do nothing if the command is identical to previous one
def getinfo (command):	# -> pid
	global file_system;
	global address_list;
	global map_list;
	global path_list;
	global mapsfile;
	global exe;
	global current_command;
	
	if command == current_command:
		return -1;

	reset();
	current_command = command;
	
	# Do not create a process if it already exists
	kill_process = False;
	if isinstance(command, int):
		pid = command;
	elif re.search(r'[^0-9]', command) == None:
		pid = int(command);
	else:
		process = create_process(command);
		pid = process.pid;
		# Wait a quarter of a second to allow the loading of the command to finish
		time.sleep(0.25);
	
	dir = '/proc/'+str(pid);
	exe = os.readlink(dir+'/exe');
	
	# Get all mapped memory and files
	with open(dir+'/maps', 'r') as file:
		for l in file:
			record_list = l.split();
			if len(record_list) == 6 and int(record_list[4]) > 0:
				(addresses, permissions, offset, device, inode, path) = record_list;
				if path not in path_list:
					path_list.append(path);
					map_list[path] = {'permissions':permissions, 'device':device, 'inode':inode};
					address_list[path] = [];
				(address1, address2) = addresses.split('-');
				address_list[path].append({'start':address1, 'end':address2, 'offset':offset});
	if kill_process: kill_process(process);
	mapsfile = path_list[0];
	file_system = get_filesystem(mapsfile);
	return pid;

# Print out running proc stats
def paths (command, key_list = 'inode'):   # 'key'/['key1', 'key2', ...] -> text-table
	getinfo (command);
	
	# Normalize keys
	if isinstance(key_list, str):
		key_list = [key_list];
	# Construct a line for each path, 
	result_table = '';
	for path in path_list:
		line = path ;
		for key in key_list:
			line += '\t'+map_list[path][key];
		line += '\n';
		result_table += line;
	return result_table;

# Methods that return the raw file contents (could be LARGE)
def file (command):
	getinfo (command);
	return_value = b'';
	with open(mapsfile, 'rb') as file:
		for l in file:
			if type(l).__name__ == 'str': 
				l = bytes(l, encoding='utf8');
			return_value += l;
	return return_value;
	
def exe (command):
	getinfo (command);
	return_value = b'';
	with open(exe, 'rb') as file:
		for l in file:
			if type(l).__name__ == 'str': 
				l = bytes(l, encoding='utf8');
			return_value += l;
	kill_process(process);
	return return_value;
	
def inode (command, path):
	getinfo(command);
	
	# Get file contents on inode number
	return_value = b'';
	inode = map_list[path]['inode'];
	debugfs = subprocess.Popen(get_debugfs_command(path, inode), stdin = None, stdout = subprocess.PIPE, stderr = sys.stderr, shell=True, universal_newlines=False);
	# read out the file contents		
	for l in debugfs.stdout:
		if type(l).__name__ == 'str': 
			l = bytes(l, encoding='utf8');
		return_value += l;

	return return_value;
	
def maps (command):
	getinfo(command);
	
	# Get file contents on inode number
	return_value = b'';
	for file in path_list:
		inode = map_list[file]['inode'];
		debugfs = subprocess.Popen(get_debugfs_command(path, inode), stdin = None, stdout = subprocess.PIPE, stderr = sys.stderr, shell=True, universal_newlines=False);
		# read out the file contents		
		for l in debugfs.stdout:
			if type(l).__name__ == 'str': 
				l = bytes(l, encoding='utf8');
			return_value += l;

	return return_value;

# Methods that return the SHA512sum
def fileSHA (command, prefix=''):
	getinfo (command);
	filehash = hashlib.sha512(bytes(prefix, encoding='ascii'));
	with open(mapsfile, 'rb') as file:
		for l in file:
			if type(l).__name__ == 'str': 
				l = bytes(l, encoding='utf8');
			filehash.update(l);
	return str(filehash.hexdigest());
	
def exeSHA (command, prefix=''):
	getinfo(command);
	exehash = hashlib.sha512(bytes(prefix, encoding='ascii'));
	with open(exe, 'rb') as file:
		for l in file:
			if type(l).__name__ == 'str': 
				l = bytes(l, encoding='utf8');
			exehash.update(l);
	return str(exehash.hexdigest());
	
def inodeSHA (command, path='', prefix=''):
	getinfo(command);
	if len(path) == 0: path = mapsfile;
	
	# Get file contents on inode number
	mapshash = hashlib.sha512(bytes(prefix, encoding='ascii'));
	inode = map_list[path]['inode'];
	debugfs = subprocess.Popen(get_debugfs_command(path, inode), stdin = None, stdout = subprocess.PIPE, stderr = sys.stderr, shell=True, universal_newlines=False);
	# read out the file contents		
	for l in debugfs.stdout:
		if type(l).__name__ == 'str': 
			l = bytes(l, encoding='utf8');
		mapshash.update(l);

	return str(mapshash.hexdigest());
	
def mapsSHA (command, prefix=''):
	getinfo(command);
	
	# Get file contents on inode number
	mapshash = hashlib.sha512(bytes(prefix, encoding='ascii'));
	for path in path_list:
		inode = map_list[path]['inode'];
		debugfs = subprocess.Popen(get_debugfs_command(path, inode), stdin = None, stdout = subprocess.PIPE, stderr = sys.stderr, shell=True, universal_newlines=False);
		# read out the file contents		
		for l in debugfs.stdout:
			if type(l).__name__ == 'str': 
				l = bytes(l, encoding='utf8');
			mapshash.update(l);

	return str(mapshash.hexdigest());
	
if __name__ == "__main__":
	if len(sys.argv) == 1:
		print(help_text);
	else:
		for command in sys.argv[1:]:
			result = fileSHA(command);
			print(mapsfile+(len("/proc/<pid>/inode") - len(mapsfile))*' ', result);
			result = exeSHA(command);
			print("/proc/<pid>/exe"+(len("/proc/<pid>/inode") - len("/proc/<pid>/exe"))*' ', result);
			if os.getuid() == 0:
				result = inodeSHA(command);
				print("/proc/<pid>/inode"+(len(mapsfile) - len("/proc/<pid>/inode"))*' ', result);
				result = mapsSHA(command);
				print("/proc/<pid>/maps"+(len("/proc/<pid>/inode") - len("/proc/<pid>/all"))*' ', result);
				
			print("");
			result = paths(command);
			print(result);
			print("");
