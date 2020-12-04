# prototyping-server

## How to run the server

The server is written python, and uses a virtual environment to reduce the
necessary requirements on the host machine. You will only need to have 
`pipenv` to run the server. Once you have `pipenv` installed, run
```
pipenv install
```
in the root of the project to download all the python dependencies necessary.

In order to launch the server and GUI, simply execute the following command:
```
pipenv run python server.py
```

If all goes well, you should see a window that looks similar to this:
![Server Startup](./readme_resources/server_gui.png)

For details about how to use the GUI, see the [usage section](#usage).

## System Overview

This repository contains code necessary to run the server in the prototyping 
system. See the diagram below for a high level overview of the system.

![Star Architecture Diagram](./readme_resources/star_architecture_diagram.jpg)

In this system, widgets can talk any other widget. However, in order to keep the
clients as slim as possible, the logic of who to communicate with and what to 
send is all contained in the server. See diagram below of a "zoomed in" 
communication example.

![Event Diagram](./readme_resources/event_tracing.jpg)

This diagram is crucial in understanding the implementation of the system as a
whole. Imagine if every widget were to communicate with every other widget
individually. This would require each widget to have to "scan" for other 
widgets in the system, and for the server to update the executing code of
every widget in the system whenever the system designer updates the  

## Firebase

## Server Codebase

## Usage

See this quick demo about typical usage:
![Server Demo](./readme_resources/server-optimized.gif)

### Widgets Section

This section shows a selectable box of all the widgets that are currently 
registered from the server-side. Note that this does *not* display all 
widgets that are registered in firebase. The two should stay in sync, but
if you manually create a widget in firebase (rather than through the server)
it will not be displayed in this list.

If you click on a widget within this box, the GUI will load the code for this 
widget into the large text area. It will also load widget attributes beneath 
the widget select box. Here are the attributes that are loaded, from top to bottom:

1. **Widget Type**: This field displays the widget type that was selected when it was created.
  This type is used by the widget to determine what UI should be displayed on
  the phone screen.
2. **Photo Identifier**: This field displays