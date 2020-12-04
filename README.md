# prototyping-server

## Setup

The server is written python, and uses a virtual environment to reduce the
necessary requirements on the host machine. You will only need to have 
`pipenv` to run the server. Once you have `pipenv` installed, run
```
pipenv install
```
in the root of the project to download all the python dependencies necessary.

There is also a git ignored secrets file that allows the code to interact
with [Firebase](#firebase). This file is named `service_account.json`, and can
be downloaded from the [firebase console](https://console.firebase.google.com).
If you aren't able to view the project, please reach out to Eric Romrell or 
Mike Jones, who should be able to add you as a member 
[here](https://console.firebase.google.com/u/0/project/prototyping-a7600/settings/iam).

## Running the server

For any communication to happen in the system, the server must be running.

To launch the server with it's GUI, simply execute the following command:
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

TODO

## Server Codebase

TODO

## Usage

See this quick demo about typical usage:
![Server Demo](./readme_resources/server-optimized.gif)

### Widgets Section

This section shows a selectable box of all the widgets that are currently 
registered from the server-side. Note that this does *not* display all 
widgets that are registered in firebase. The two should stay in sync, but
if you manually create a widget in firebase (rather than through the server)
it will not be displayed in this list.

If you click on a widget within this box, the GUI will load the attributes for
the selected widget. You will notice property attributes beneath the widget 
select box, as well as the code in the large text area. Here are descriptions
and details about each of the attributes that are loaded (top -> bottom, left -> right):

1. **Widget Type**: This field displays the widget type that was selected when 
it was created. This type is used by the widget to determine what UI should be 
displayed on the phone screen.
2. **Photo Identifier**: This field displays the ID of the photo that will be
displayed on the Android app, and will also be used by the AR app to identify the 
widget that is being scanned.
3. **Widget Code**: This field contains the code that is executed when the widget
sends an event to the server. For instance, if a *Button* widget is clicked, it
will send an event to the server that will execute the `button_tapped` function
in that widget's code. For more details, see the [widget code](#widget-code-details) 
section. This code is saved to a local file `widgets/<widget_id.py` which will
be executed the next time that widget pushes an event.

### Add New Widget Section

This section allow you to add a new widget to the system. There are three attributes
that you select before creating a new widget. Here are the descriptions about each
of those fields:

1. **Widget Name**: This will be the name that the widget will be associated with in 
all three applications. It will be used in all of the following scenarios:
    * The widgets selection box of the server GUI
    * The widget's code on the server (e.g. `widgets.widget_name.speak(...)`). For more
details, see the [widget code](#widget-code-details) section
    * The Android app's drop-down list to select a widget to display
    * The AR app's banner after scanning a widget
2. **Widget Type**: This type is used by the Android app to determine what UI should
be displayed on the phone screen. It will also be used to create a template for the
code that includes the functions that a widget of that type typically uses.
3. **Photo ID**: This ID will be used to determine the photo that will be
displayed on the Android app, and will also be used by the AR app to identify the 
widget that is being scanned.

### Modification Buttons

At the bottom of the GUI, there are two buttons
1. **Save**: This button will send attribute changes to firebase (such as the widget
type or photo ID), as well as overwriting the local file containing the widget's code.
2. **Delete**: This button will delete the widget from firebase, as well as deleting
the local file containing the widget's code.

## Widget Code Details

TODO