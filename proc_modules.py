# proc_modules
# 
# Signature-du-Terroir module to handle /proc/modules
#
# Help text
help_text = """
Values:
modulelist:   List of module names
moduledict:   Dictionary of [module-name] = {'size', 'loadnum', 'dependencies', 'state', 'offset'}
              moduledict['video']['offset'] -> offset adress in kernel of the 'video' module
min_address:  Lowest offset address
max_load:     Highest offset address
max_address:  max_load + size-of-last-module
sum_sizes:    sum of all module sizes
memory_range: max_address - min_address
kallsyms_modulelist:   List of module names constructed from the exported kernel symbols in /proc/kallsyms

Functions:
sorted_sizes_table():        Alphabetically sorted table of modules+sizes as a string
sorted_offset_table():       Alphabetically sorted table of modules+offset as a string
sorted_loadnum_table():      Alphabetically sorted table of modules+loadnum as a string
sorted_dependencies_table(): Alphabetically sorted table of modules+dependencies as a string
sorted_state_table():        Alphabetically sorted table of modules+state as a string

===================
proc_modules
Signature-du-Terroir module to access /proc/modules pseudo file.

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

import re;
modulelist = [];
moduledict = {};
min_address = 10**100;
max_address = -1;
max_load = -1;
sum_sizes = 0;
with open('/proc/modules') as m:
   for l in m:
      module_value = re.split(r'\s+', l.rstrip('\s\n'));
      (module, size, loadnum, dependencies, state, offset) = module_value[0:6];
      modulelist.append(module);
      size = int(size);
      loadnum = int(loadnum);
      offset = int(offset, 16);
      module_entry = {'size':size, 'loadnum':loadnum, 'dependencies':dependencies, 'state':state, 'offset':offset};
      moduledict[module] = module_entry;
      if min_address > offset: min_address = offset;
      if max_address < offset+size: max_address = offset + size;
      if max_load < offset: max_load = offset;
      sum_sizes += size;
      
kallsyms_modulelist = [];
with open('/proc/kallsyms') as m:
   for l in m:
      	module_value = re.split(r'\s+', l.rstrip('\s\n'));
      	module = module_value[-1];
      	if module.startswith('['):
      		modulename = module.lstrip('[').rstrip(']');
      		if not modulename in kallsyms_modulelist:
      			kallsyms_modulelist.append(modulename);
      	kallsyms_modulelist.sort();

memory_range = max_address - min_address

def sorted_sizes_table():
   modulelist.sort();
   s="";
   for m in modulelist:
      s += m+"\t"+str(moduledict[m]['size'])+"\n";
   return s;
   
def sorted_offset_table():
   modulelist.sort();
   s="";
   for m in modulelist:
      s += m+"\t"+str(moduledict[m]['offset'])+"\n";
   return s;

def sorted_loadnum_table():
   modulelist.sort();
   s="";
   for m in modulelist:
      s += m+"\t"+str(moduledict[m]['loadnum'])+"\n";
   return s;
   
def sorted_dependencies_table():
   modulelist.sort();
   s="";
   for m in modulelist:
      s += m+"\t"+str(moduledict[m]['dependencies'])+"\n";
   return s;
   
def sorted_state_table ():
   modulelist.sort();
   s="";
   for m in modulelist:
      s += m+"\t"+str(moduledict[m]['state'])+"\n";
   return s;

def dump_module_binary (name):
   module_binary = open('/proc/kcore');

if __name__ == "__main__":
    print(help_text);
    print(kallsyms_modulelist);
