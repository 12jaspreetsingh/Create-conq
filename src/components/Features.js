function Features() {
  const features = [
    {
      title: "Skill Extraction",
      desc: "Convert videos into step-by-step robot actions",
    },
    {
      title: "AI Understanding",
      desc: "Detect objects, hands, and interactions",
    },
    {
      title: "Failure Prediction",
      desc: "Identify risky steps before execution",
    },
    {
      title: "Learning Memory",
      desc: "Store and reuse learned robot skills",
    },
  ];

  return (
    <div className="section">
      <h2>What We Do</h2>

      <div className="grid">
        {features.map((f, i) => (
          <div key={i} className="card">
            <h3>{f.title}</h3>
            <p>{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Features;