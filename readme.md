# DogMatch

This is a Flask-based web application that facilitates scheduling and managing dog walkers for dog owners, allowing users to add, edit, and delete information about dog owners, dogs, and walkers.

It also lets users manage availability for dogs and walkers, automatically matches dogs with walkers based on overlapping availability, and displays the matches. The app uses a SQLite database for storing data and supports CRUD operations via user-friendly forms and interfaces.

Line count:
  Python 401
  HTML 268

Project created with PyCharm Pro with AI Assistant Ultimate.
PyCharm 2025.2.0.1
Build #PY-252.23892.515, built on August 11, 2025
Source revision: a49d407cfb992
Licensed to Stefaan Meeuws
You have a perpetual fallback license for this version.
Subscription is active until August 12, 2028.
Runtime version: 21.0.7+6-b1038.58 amd64 (JCEF 122.1.9)
VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
Toolkit: sun.awt.windows.WToolkit
Windows 11.0
GC: G1 Young Generation, G1 Concurrent GC, G1 Old Generation
Memory: 2048M
Cores: 28
Registry:
  ide.windowSystem.autoShowProcessPopup=true
  ide.experimental.ui=true
Non-Bundled Plugins:
  Batch Scripts Support (1.0.13)
  com.bottlerocket.plugin.jsonfilter.JsonFilter (0.0.7)
  com.jetbrains.edu (2025.7-2025.2-431)
  dev.turingcomplete.intellijdevelopertoolsplugins (7.1.0)
  me.bytebeats.jsonmstr (1.1.0)
  org.jetbrains.junie (252.284.66)
  String Manipulation (9.16.0)
  CMD Support (1.0.5)
  co.anbora.labs.jsoncrack (1.4.1)
  com.intellij.ml.llm (252.23892.530)
  com.cn.json.simple (3.1.7)
  com.intellij.grazie.pro (0.3.390)
  Karma (252.25204.0)
  izhangzhihao.rainbow.brackets (2025.3.2)


## Prerequisites

Python 3.9+ and `pip`.

An SQLite DB with the following tables and fields (Summary SQL is next):
  Tables (6)
    alembic_version
      version_num VARCHAR(32) not null
    availability
      id = integer not null
      weekday = integer not null
      start_time = time not null
      end_time = time not null
      dog_id = integer
      walker_id = integer
    dog
      id = integer not null
      name = varchar(80) not null
      breed = varchar(80)
      owner_id = integer not null
    dog_owner
      id = integer not null
      name = varchar(100) not null
      email = varchar(120)
      phone = varchar(40)
    dog_walker
      id = integer not null
      name = varchar(100) not null
      phone = varchar(40)
    matches
      id = integer
      field1 = text
      field2 = text
  Indices (0)
  Views (0)
  Triggers (0)
  

Summary SQL:
CREATE TABLE alembic_version ( version num VARCHAR(32) NOT NULL, CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num) )
CREATE TABLE availability ( id INTEGER NOT NULL, weekday INTEGER NOT NULL, start_time TIME NOT NULL, end_time TIME NOT NULL, dog_id INTEGER, walker_id INTEGER, PRIMARY KEY (id), FOREIGN KEY(dog_id) REFERENCES dog (id), FOREIGN KEY(walker_id) REFERENCES dog_walker(id) )
CREATE TABLE dog ( id INTEGER NOT NULL, name VARCHAR(80) NOT NULL, breed VARCHAR(80), owner_id INTEGER NOT NULL, PRIMARY KEY (id), FOREIGN KEY(owner_id) REFERENCES dog_owner(id) )
CREATE TABLE dog_owner ( id INTEGER NOT NULL, name VARCHAR(100) NOT NULL, email VARCHAR(120), phone VARCHAR(40), PRIMARY KEY (id) )
CREATE TABLE dog_walker ( id INTEGER NOT NULL, name VARCHAR(100) NOT NULL, phone VARCHAR(40), PRIMARY KEY (id) )
CREATE TABLE matches ( "id" INTEGER, "field1" TEXT, "field2" TEXT )



## Setup

On Windows, start the Command Prompt by typing "cmd".
Change Working Directory to the Root Directory of the Project.

1. Create the Virtual Environment
     python -m venv venv
3. Activate the Virtual Environment
     venv\Scripts\activate (and press Enter)
5. Install Dependencies (If Not Already Done)
     pip install -r requirements.txt
7. Run the App
     python app.py
9. Run Flask
      flask run
11. Use Your Browser
    Type in the Address Bar: http://127.0.0.1:5000/
    
12. Deactivate the Virtual Environment
    deactivate (This will return you to your system's default Python environment.)
