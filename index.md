MaterialCreator - for Autodesk Maya
======================================
***
**Version 1.4**  
**December 2021**

**Compatibility: Maya 2019, 2020 - Python 2.7**

The latest release of Material Creator is available for **download [here]()**.

**Material Creator** is a tool for Autodesk Maya developed by **[Roberto Menicatti](https://robertomenicatti.carrd.co/)**. It started as a school side-project at *BigRock Institute of Magic Technologies*. At the moment, further development is not planned to happen on a regular basis.

***

- [Quick Guide](https://robertom89.github.io/BigRig/#quick-guide)
- [Download and Install](https://robertom89.github.io/BigRig/#download-and-install)
- [Interface](https://robertom89.github.io/BigRig/#interface)
- [How to Rig Character Limbs with BigRig](https://robertom89.github.io/BigRig/#how-to-rig-character-limbs-with-bigrig)
    - [Rigging the Legs](https://robertom89.github.io/BigRig/#rigging-the-legs)
    - [Rigging the Arms](https://robertom89.github.io/BigRig/#rigging-the-arms)
    - [Rigging the Hands](https://robertom89.github.io/BigRig/#rigging-the-hands)
    - [Replacing a Control Curve](https://robertom89.github.io/BigRig/#replacing-a-control-curve)
- [Commands](https://robertom89.github.io/BigRig/#commands)
    - [Generic Commands](https://robertom89.github.io/BigRig/#generic-commands)
    - [Arm Rig](https://robertom89.github.io/BigRig/#arm-rig)
    - [Hand Rig](https://robertom89.github.io/BigRig/#hand-rig)
    - [Leg Rig](https://robertom89.github.io/BigRig/#leg-rig)
    - [Control Commands](https://robertom89.github.io/BigRig/#control-commands)
    - [Shapes](https://robertom89.github.io/BigRig/#shapes)

***

## Quick Guide
To rig the limbs of your character, place and orient 5 joints on the left leg mesh and 3 joints on the left arm mesh as in the following figures, then freeze their rotations.

<div class="row">
  <div class="column">
    <img src="https://robertom89.github.io/BigRig/images/leg_rig_02.jpg" alt="Legs" width="80%"/>
    <figcaption>Fig.1 - Leg joints</figcaption>
  </div>
  <div class="column">
    <img src="https://robertom89.github.io/BigRig/images/arm_rig_02.jpg" alt="Arms" width="100%"/>
    <figcaption>Fig.2 - Arm joints</figcaption>
  </div>
</div>



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
