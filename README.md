PCAF Reporting
==============

Commcare extract and reporting system for www.petercaldermanfoundation.org.

Installing PyCharm and Anaconda/Miniconda
--------
Download and install Pycharm Community Edition

Install Anaconda3:
* https://conda.io/docs/user-guide/install/index.html
* Install "Miniconda" for the minimal installation, about 40 megs
* Or install "Anaconda" for the full installation, about 600 MB.
   Either way, pick the installation for your OS

Prepare PyCharm for working on GitHub projects:
* Follow the directions at https://www.jetbrains.com/help/pycharm/manage-projects-hosted-on-github.html
 to register new GitHub account and to get PyCharm ready for working with GitHub projects.

First Time PyCharm Setup for the PCAF project
-----
* Create a new PyCharm project by checking out the project from GitHub.
The project URL is https://github.com/lerouxt/pcaf.git

* Create a new Python environment for the project:
  1. Make sure the PCAF project is open
  1. File, Default Settings...
  1. Project Interpreter:
      * Add a new interpreter
      * Conda project
      * Choose the miniconda project you installed earlier
      * Git it a directory name like 'pcafenv' instead of the default 'untitled'
  
Now, open any .py file (like src/box.py).  You should see an option at the
top of the file to import dependencies.  Select this, and wait for a few minutes
while all the necessary Python modules are installed.

Create a pcaf.cfg file
-----
Create pcaf.cfg file at the root. **Do not add this file to Git since
it contains sensitive passwords.**
