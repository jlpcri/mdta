#/bin/bash
#PROJECTNAME=demo
#set -x 
# This script generates a New Django Project.

REPO=/var/hg/repos
CLONE_LOC=/opt
VENVWRP_LOC=`locate virtualenvwrapper.sh`

if [ -z $1 ]; then
        echo "Usage: $0 <Django Project Name>"
        echo "eg."
        echo "$0 MyNewProject"
        exit
fi

#Create directory
echo "Creating Project Directory......."
rm -r $REPO/$1
mkdir -p $REPO/$1

#Initiate and clone mercurial repository
echo "Initiating empty mercurial repository at $REPO/$1...."
cd $REPO/$1
hg init
rm -rf $CLONE_LOC/$1
hg clone $REPO/$1 $CLONE_LOC/$1 
echo "Empty repository cloned to $CLONE_LOC/$1"

#Create virtual environment
echo "Creating virtual environment for new django project $1"
if [ -z "$VENVWRP_LOC" ]; then
	echo "Installing virtualenvwrapper package....."	
	echo "`pip install virtualenvwrapper`"
	export WORKON_HOME=~/.virtualenvs
	VENVSCRIPT_LOC=`locate virtualenvwrapper.sh`
	echo "`source $VENVSCRIPT_LOC`"
	echo "`mkvirtualenv $1`"
	echo "Succesfully installed virtualenvwrapper and created a new virtual env $1 in $WORKON_HOME"
else
	export WORKON_HOME=~/.virtualenvs
	echo "`source ~/.bashrc`"
	echo "$WORKON_HOME"
	echo "$VENVWRP_LOC"
	echo "`mkvirtualenv $1`"
	echo "Virtual environment $1 created in $WORKON_HOME"
fi
#echo "`python3 -m venv $CLONE_LOC/$1`"
echo "`workon $1`"
echo "....."
echo "........"
echo "Virtual environment $1 activated"
echo "`pip install django django-auth-ldap psycopg2`"
cd $CLONE_LOC/$1
echo "Starting new project $1 in $CLONE_LOC/$1"
echo "`django-admin startproject $1`"
echo "....."
echo "........"
echo "New project $1 started"
echo "Creating directory structure for new project $1....."
cd $CLONE_LOC/$1/$1/$1
mkdir -p apps/core settings
cd $CLONE_LOC/$1
mkdir requirements
mv $CLONE_LOC/$1/$1/manage.py $CLONE_LOC/$1
echo "`pip freeze > $CLONE_LOC/$1/requirements/common.txt`"
echo "Directory structure created"
echo "Adding the new project to remote repository......"
hg add .
echo "Comitting new project to remote repository......."
hg commit -u $USER -m "Initial commit by $USER for Django Project $1"
echo "Pushing the project to remote repository....."
hg push

