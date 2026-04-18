function Pipeline() {
  const steps = [
    "Upload Video",
    "Frame Sampling",
    "Object Detection",
    "Action Segmentation",
    "Skill Extraction",
    "Failure Prediction",
    "Structured Output",
  ];

  return (
    <div className="section">
      <h2>How It Works</h2>

      <div className="pipeline">
        {steps.map((step, i) => (
          <div key={i} className="step">
            {step}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Pipeline;