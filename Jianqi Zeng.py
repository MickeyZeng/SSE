#!/usr/bin/env python
# coding: utf-8

# 
# 

# # Load libraries

# In[1]:


import numpy as np
import pandas as pd
import os

# Specify git executable file for GitPython in Jupyter Notebook (In IDE, it can still work without this line.)
os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = "C:\Program Files\Git\cmd\git.exe"

import git
from git import RemoteProgress

from git import Repo
import matplotlib.pyplot as plt
import seaborn as sns
import re
get_ipython().run_line_magic('matplotlib', 'inline')


# # Clone repo from GitHub

# Link: https://git-scm.com/docs/git-clone <br>
# <b>Note:</b> In case too-long file path issue occurs in Windows, set <code>git config --system core.longpaths true</code>

# In[2]:


class Progress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)


# In[3]:


remote_link = "https://github.com/spring-projects/spring-framework"
local_link = "spring-framework"
# Uncomment to clone
# Repo.clone_from(remote_link, local_link, progress=Progress())


# In[4]:


repo = Repo(local_link)
fixing_commit = "246a6db1cad205ca9b6fca00c544ab7443ba202"
previous = fixing_commit + '^'
affected_file = "MappingJackson2HttpMessageConverter.java"

# # Question a: show commit title and commit msg

# In[6]:


show_data = repo.git.log("--format=%B", "-n", "1",fixing_commit).splitlines()

print("The commit title and message are: ")
for line in show_data:
    print(line)


# # Question b: Show all affected files

# In[7]:


affected_file = repo.git.diff( "--name-only", fixing_commit, previous).splitlines()

print("The affected file/ files are:")
print(len(affected_file))


# # Question c: show all directories are affected

# In[8]:


affected_directories = repo.git.diff("--dirstat", fixing_commit, previous).splitlines()
print("The number of affected dir/ dirs:")

print(len(affected_directories))


# # Question d: How many lines were deleted?

# In[9]:


sum_delete = 0
deleted_lines = repo.git.diff(previous, fixing_commit).splitlines()
rule = re.compile('^-$|^-[^-]')

for line in deleted_lines:
    if rule.match(line):
        sum_delete += 1

            
print("Lines deleted: %d" %sum_delete)

# # Question e: How many lines were added?

# In[10]:

sum_add = 0
add_lines = repo.git.diff(previous, fixing_commit).splitlines()
rule = re.compile('^\+$|^\+[^\+]')

for line in deleted_lines:
        if rule.match(line):
            sum_add += 1
            
print("Lines added: %d" %sum_add)


# # Question f: How many lines were deleted (Excluding blank line & comment)

# In[11]:


sum_deleted_without = 0
delete_lines = repo.git.diff("--ignore-blank-lines",previous, fixing_commit).splitlines()
rule = re.compile('^-$|^-[^-]')
rule1 = re.compile('^[-|\+]\s*\*')
rule2 = re.compile('^[-|\+]\s*\/\/')

for line in deleted_lines:

        if rule.match(line):
            sum_deleted_without += 1
            if rule1.match(line) or rule2.match(line):
                sum_deleted_without -= 1
            
print("Lines added: %d" %sum_deleted_without)


# # Question g: How many lines were added (Excluding blank line & comment)

# In[12]:


sum_added_without = 0
add_lines = repo.git.diff("--ignore-blank-lines",previous, fixing_commit).splitlines()
rule = re.compile('^\+$|^\+[^\+]')
rule1 = re.compile('^[-|\+]\s*\*')
rule2 = re.compile('^[-|\+]\s*\/\/')

for line in add_lines:
        if rule.match(line):
            sum_added_without += 1
            if rule1.match(line) or rule2.match(line):
                sum_added_without -= 1
            
print("Lines added: %d" %sum_added_without)


# # Question h: How many days were between the current fixing commit and the previous commit of each affected file

# In[13]:


time_different = 0
sum = 0
count = 0
for line in repo.git.diff("--name-only", fixing_commit, previous).splitlines():
    creation = repo.git.log("-2", "--pretty=%ct","--", line).splitlines();
    if len(creation) == 2:
        count += 1;
        time_different = ((float(creation[0]) - float(creation[1])) / 86400)
        sum = sum + time_different
        print("%s \t%.1f"%(line,((float(creation[0]) - float(creation[1])) / 86400)))
    else:
        print("%s is New file" %line)

avg = sum / count
print("%.1f" %avg)


# # Question i: How many times has each affected file of the current fixing commit been modified in the past since their creation (including rename of the file)?

# In[14]:


sum_time = 0
count = 0
# implement code
for line in repo.git.diff("--name-only", fixing_commit, previous).splitlines():
    count = count + 1;
    times = repo.git.log("--follow", "--pretty=oneline", "--", line).splitlines();
    sum_time = sum_time + len(times)
    print(" %s: %d " %(line, len(times)))

avg = sum_time / count
print("%d" %avg)


# # Question j: Which developers have modified each affected file since its creation? 

# In[16]:


# implement code
count = 0
for line in repo.git.diff("--name-only", fixing_commit, previous).splitlines():
    print(" %s"%line)
    authors = repo.git.log("--follow", "--pretty=%aN", "--", line).splitlines()
    for author in set(authors): # set for not repeating the same author
        print(" %s" %author)
        count = count + 1;

avg = count / len(affected_file)
print("%.1f" %avg)


# # Question k: For each developer identified, how many commits have each of them submitted? From your observation, are the involving developers experienced (with many commits) or new ones (with few commits) or both?

# In[15]:


# implement code
allAuthors = []
count = 0
for line in repo.git.diff("--name-only", fixing_commit, previous).splitlines():
    allAuthors += repo.git.log("--follow", "--pretty=%aN", "--", line).splitlines()
allAuthors = list(set(allAuthors))
log = repo.git.log("--pretty=%aN")
for author in allAuthors:
    count = count + 1
    print(" %s: %d" %(author, len(re.findall(author, log))))
    
print("%d" %count)





