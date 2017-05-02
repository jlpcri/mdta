#/bin/bash
#PROJECTNAME=demo
#set -x 

REPO=/var/hg/repos
CLONE_LOC=/opt

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
echo "`python3 -m venv $CLONE_LOC/$1`"
source $CLONE_LOC/$1/bin/activate
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
cd $CLONE_LOC/$1/$1/$1
mkdir -p apps/core settings
cd $CLONE_LOC/$1
mkdir requirements
mv $CLONE_LOC/$1/$1/manage.py $CLONE_LOC/$1
echo "`pip freeze > $CLONE_LOC/$1/requirements/common.txt`"
hg add .
hg commit -u $USER -m "Initial commit by $USER for Django Project $1"
hg push

