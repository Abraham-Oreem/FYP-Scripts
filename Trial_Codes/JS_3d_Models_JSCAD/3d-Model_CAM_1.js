const { primitives, transforms } = require('@jscad/modeling');
const { polygon } = primitives;
const { rotateZ } = transforms;

const main = () => {
  // Cam parameters
  const baseRadius = 40; // Base cam radius
  const riseHeight = 20; // Total rise height
  const sections = 8;    // Number of sections
  const stepsPerSection = 100; // Resolution for smoothness
  const totalSteps = sections * stepsPerSection;

  const points = []; // Array to store cam profile points

  // Function to convert degrees to radians
  const degToRad = (degrees) => (degrees * Math.PI) / 180;

  // Generate cam profile using cycloidal motion
  for (let i = 0; i <= totalSteps; i++) {
    const angle = (i / totalSteps) * 360; // Total angle for 360° rotation
    const radians = degToRad(angle);
    let displacement = 0;

    // Define rise and fall regions with cycloidal motion
    const phase = ((i % stepsPerSection)) / stepsPerSection;
    if ((angle >= 0 && angle < 45) ) {
      
      displacement = riseHeight * (phase - Math.sin(2 * Math.PI * phase) / (2 * Math.PI));
    }else if ((angle >= 45 && angle < 90)) {
      
      displacement = riseHeight 
    }else if ((angle >= 90 && angle < 135)) {
      
      displacement = riseHeight * (1 - phase + Math.sin(2 * Math.PI * phase) / (2 * Math.PI));
    
    }else if ((angle >= 135 && angle < 180) ) {
      
      displacement = riseHeight * (phase - Math.sin(2 * Math.PI * phase) / (2 * Math.PI));
    }else if ((angle >= 180 && angle < 225)) {
      
      displacement = riseHeight * (1 - phase + Math.sin(2 * Math.PI * phase) / (2 * Math.PI));
    
    }else if ((angle >= 225 && angle < 270)) {
      
      displacement = 0 
    }
    else if ((angle >= 270 && angle < 315)) {
      
      displacement = riseHeight * (phase - Math.sin(2 * Math.PI * phase) / (2 * Math.PI));
    }else if ((angle >= 315 && angle < 360)) {
      
      displacement = riseHeight * (1 - phase + Math.sin(2 * Math.PI * phase) / (2 * Math.PI));
    }

    const radius = baseRadius + displacement; // Adjust radius with displacement
    const x = radius * Math.cos(radians);
    const y = radius * Math.sin(radians);

    points.push([x, y]); // Add point to profile
  }

  // Close the profile by adding the first point
  points.push(points[0]);

  // Generate the cam profile as a polygon
  const camProfile = polygon({ points });

  return [camProfile];
};

module.exports = { main };