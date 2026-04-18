import { useState } from "react";

function Upload() {
  const [video, setVideo] = useState(null);
  const [output, setOutput] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setVideo(URL.createObjectURL(file));
      setOutput(null);
    }
  };

  const processAI = () => {
    setLoading(true);
    setOutput(null);

    setTimeout(() => {
      setLoading(false);
      setOutput([
        "Pick up object",
        "Move to target",
        "Place carefully",
        "Release grip",
      ]);
    }, 2000);
  };

  return (
    <div className="upload">
      <h2>Upload Video</h2>

      {/* Custom Upload Box */}
      <label className="upload-box">
        <input type="file" accept="video/*" onChange={handleUpload} />
        <p>📁 Click to choose a video</p>
      </label>

      {/* Preview */}
      {video && (
        <>
          <video width="420" controls src={video}></video>

          <div>
            <button className="btn" onClick={processAI} style={{ marginTop: "20px" }}>
              Process with AI
            </button>
          </div>
        </>
      )}

      {/* Loading */}
      {loading && (
        <div>
          <div className="loader"></div>
          <p className="processing-text">AI is analyzing your video...</p>
        </div>
      )}

      {/* Output */}
      {output && (
        <div className="output-box">
          {output.map((step, i) => (
            <div key={i} className="step">
              {step}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Upload;