


const { cylinder } = require('@jscad/modeling').primitives;
const { polygon } = require('@jscad/modeling').primitives;
const { extrudeLinear } = require('@jscad/modeling').extrusions;
const { union, subtract } = require('@jscad/modeling').booleans;
const { translate, rotateZ } = require('@jscad/modeling').transforms;

const main = () => {
  const toothWidth = 2;       // Width of the tooth base
  const toothHeight = 1;     // Height of the tooth
  const toothThickness =1.5;//Thickness of the tooth (Z-direction)

  const cylinderRadius =10;    // Outer radius of the cylinder
  const innerCylinderRadius =7.5;// Inner radius of the hollow cylinder
  const cylinderHeight =140; // Height of the cylinder
  const helixRevolutions = 7; // Number of helix revolutions
  const helixSegments=(((2*Math.PI*cylinderRadius)/(toothWidth-1))*helixRevolutions)+1;
  
  // Function to create the 2D profile of a gear tooth
  const createToothProfile = (width, height) => {
  const halfWidth = width / 2;
  const tipWidth = width * 0.4; // Width of the tooth tip (narrower than the base)
  const tipHalfWidth = tipWidth / 2;

  return polygon({
    points: [
      [-halfWidth, 0],           // Bottom-left corner of the base
      [halfWidth, 0],            // Bottom-right corner of the base
      [tipHalfWidth, height],    // Top-right corner of the tooth tip
      [-tipHalfWidth, height],   // Top-left corner of the tooth tip
    ],
  });
};

  // Create the outer cylinder
  const outerCylinder = cylinder({ radius: cylinderRadius, height: cylinderHeight+10, segments: 64 });

  // Create the inner hollow cylinder
  const innerCylinder = cylinder({ radius: innerCylinderRadius, height: cylinderHeight+10, segments: 64 });

  // Subtract the inner cylinder from the outer to create the hollow effect
  const hollowCylinder = subtract(outerCylinder, innerCylinder);

  // Create the continuous spiral helix with gear teeth
  const helixSegmentsArray = [];
  const helixPitch = cylinderHeight / helixRevolutions; // Vertical distance per revolution

  for (let i = 0; i < helixSegments ; i = i + 2) {  // Start from 3 and end at helixSegments - 3 to exclude 3 from both ends
    const angle =[(i / helixSegments) * (360 * helixRevolutions)]//gle for the current segment
    const z = (i / helixSegments) * cylinderHeight - cylinderHeight / 2;// Z-position along the height

    // Position the gear tooth along the cylinder's surface
    const x = (cylinderRadius-0.5) * Math.cos(angle * Math.PI / 180);  // X-position on the surface
    const y = (cylinderRadius-0.5) * Math.sin(angle * Math.PI / 180);  // Y-position on the surface

    // Create the 2D profile and extrude it to form the 3D tooth
    const gearTooth = extrudeLinear({ height: toothThickness }, createToothProfile(toothWidth, toothHeight));

    // Position the gear tooth along the helical path
    const toothSegment = translate(
      [x, y, z],  // Position the tooth on the cylinder's surface
      rotateZ((angle * Math.PI / 180) - 1.6, gearTooth)    // Rotate each tooth along the Z-axis
    );

    helixSegmentsArray.push(toothSegment);
  }

  // Combine the hollow cylinder and the continuous helix of gear teeth
  const continuousHelix = union(...helixSegmentsArray);
 
  // Combine the cylinder and disc
  return union(hollowCylinder, continuousHelix);
};

// Export the main function
module.exports = { main };