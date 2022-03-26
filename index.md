MaterialCreator - for Autodesk Maya
======================================
***
**Version 1.5**  
**March 2022**

**Compatibility: Maya 2019, 2020, 2022 - Python 2.7, Python 3**

The latest release of Material Creator is available for **download [here](https://github.com/RobertoM89/MaterialCreator/releases/download/v1.5/MaterialCreator_v1.5.zip)**.

**Material Creator** is a tool for Autodesk Maya developed by **[Roberto Menicatti](https://allmylinks.com/robertom89)**. It started as a school side-project at *BigRock Institute of Magic Technologies*. At the moment, further development is not planned to happen on a regular basis.

***

- [Quick Guide](https://robertom89.github.io/MaterialCreator/#quick-guide)
- [Download and Install](https://robertom89.github.io/MaterialCreator/#download-and-install)

***

## Quick Guide

<img src="https://robertom89.github.io/MaterialCreator/images/material_creator_interface.jpg" alt="Interface" width="400"/>

First, enter a name for the material you want to create on the top input field. The material can't be created if a name is not inserted. By default the suffix **"_MAT"** is appended to the name you insert. You can change the text of the suffix in the field below, or convert it into a prefix from the checkbox. If you don't want any prefix or suffix, simply tick **None**.

Click on the folder icon and browse to the folder containing the textures that you want to use for your PBR material, then click on **Save**. The folder must contain the textures for the desired material only, i.e. you cannot have the textures for a wood material and a stone material inside the same folder. The textures files must be named properly, containing the map type in their names (variants like metalness/metallic, ao/occlusion etc. are accepted).

After selecting the folder, MaterialCreator will show the files that have been found in the fields below. If more than one UDIM is found, the number is displayed together with the filename.
- if you want to change or manually select the file for each map, simply click on **Change** and select the file;
- if you don't want to load a specific map, simply untick the relative checkbox on the left.

Select the render engine you are using. MaterialCreator supports only Arnold, VRay and Octane.

If you want to immediately assign the new material to your selection, tick **Assign new material to selected elements**.

Finally, click on **Create** to create the new material and leave MaterialCreator open, or click on **Create and Close** to close MaterialCreator after creation.

## Download and Install
First, download the latest version of MaterialCreator [here](https://github.com/RobertoM89/MaterialCreator/releases/download/v1.5/MaterialCreator_v1.5.zip). After downloading the zipped folder, uncompress it wherever you want and move the inner content, i.e. *MaterialCreator* folder, to Maya scripts folder. Depending on how you unzipped the folder, you may have two nested MaterialCreator folders; make sure to move the inner one, which is the one containing the Python files.

You cand find Maya scripts folder here:  

- on **Windows**   
~~~
    <user’s directory>/Documents/maya/scripts/  
~~~
- on **macOS**  
~~~
    Library/Preferences/Autodesk/maya/scripts/  
~~~

Then, open **material_creator_shelf.py** with a text editor, copy the few lines of code you will find and paste them into Maya *Script Editor*. Click on *File → Save Script to Shelf...* to add MaterialCreator to the active shelf. Finally, click on the new shelf button to run MaterialCreator.

Optionally, you can edit the shelf icon and use the **material_creator.svg** file that you can find inside the *icons* folder of MaterialCreator folder.

<button onclick="topFunction()" id="myBtn" title="Go to top" style="display: none;
  width: 50px;
  height: 50px;
  position: fixed;
  bottom: 20px;
  right: 30px;
  z-index: 99;
  font-size: 18px;
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: none;
  outline: none;
  background-color: #2D7180;
  color: white;
  cursor: pointer;
  padding: 15px;
  border-radius: 100%;">Top</button>

<script>
//Get the button
var mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}
</script>

<style>
* {
  box-sizing: border-box;
}

.column {
  float: left;
  width: 50%;
  padding: 5px;
}

/* Clearfix (clear floats) */
.row::after {
  content: "";
  clear: both;
  display: table;
}
</style>
