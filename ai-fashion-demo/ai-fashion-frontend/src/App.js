import { useState } from "react";

function App() {
  const [tab, setTab] = useState("recommend");

  // Recommendation fields
  const [segment, setSegment] = useState("");
  const [season, setSeason] = useState("");
  const [goal, setGoal] = useState("");
  const [recResult, setRecResult] = useState("");

  // Content fields
  const [product, setProduct] = useState("");
  const [tone, setTone] = useState("");
  const [avoid, setAvoid] = useState("");
  const [include, setInclude] = useState("");
  const [contentResult, setContentResult] = useState("");

  const getRecommendations = async () => {
    const res = await fetch("http://127.0.0.1:5000/recommend", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ segment, season, goal })
    });
    const data = await res.json();
    setRecResult(JSON.stringify(data, null, 2));
  };

  const generateContent = async () => {
    const res = await fetch("http://127.0.0.1:5000/content", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ product, tone, avoid, include })
    });
    const data = await res.json();
    setContentResult(JSON.stringify(data, null, 2));
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">

      {/* CENTER CARD CONTAINER */}
      <div className="bg-white p-8 rounded-xl shadow-lg w-[450px]">

        <h1 className="text-3xl font-bold mb-6 text-center">
          AI Fashion Assistant
        </h1>

        {/* Tabs */}
        <div className="flex justify-center gap-4 mb-6">
          <button
            onClick={() => setTab("recommend")}
            className={`px-4 py-2 rounded ${
              tab==="recommend" ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}
          >
            Recommendations
          </button>

          <button
            onClick={() => setTab("content")}
            className={`px-4 py-2 rounded ${
              tab==="content" ? "bg-purple-500 text-white" : "bg-gray-200"
            }`}
          >
            Content Generator
          </button>
        </div>

        {/* RECOMMENDATION TAB */}
        {tab === "recommend" && (
          <div>
            <h2 className="text-xl font-semibold mb-4 text-center">
              Product Recommendation
            </h2>

            <input
              placeholder="Customer Segment"
              className="border p-2 w-full mb-3"
              onChange={(e)=>setSegment(e.target.value)}
            />

            <input
              placeholder="Season"
              className="border p-2 w-full mb-3"
              onChange={(e)=>setSeason(e.target.value)}
            />

            <input
              placeholder="Business Goal"
              className="border p-2 w-full mb-3"
              onChange={(e)=>setGoal(e.target.value)}
            />

            <button
              onClick={getRecommendations}
              className="bg-blue-500 text-white px-4 py-2 rounded w-full"
            >
              Get Suggestions
            </button>

            {recResult && (
              <pre className="mt-4 bg-gray-100 p-3 text-sm overflow-auto">
                {recResult}
              </pre>
            )}
          </div>
        )}

        {/* CONTENT TAB */}
        {tab === "content" && (
          <div>
            <h2 className="text-xl font-semibold mb-4 text-center">
              Content Generator
            </h2>

            <input
              placeholder="Product Details"
              className="border p-2 w-full mb-3"
              onChange={(e)=>setProduct(e.target.value)}
            />

            <input
              placeholder="Brand Tone"
              className="border p-2 w-full mb-3"
              onChange={(e)=>setTone(e.target.value)}
            />

            <input
              placeholder="Banned Words"
              className="border p-2 w-full mb-3"
              onChange={(e)=>setAvoid(e.target.value)}
            />

            <input
              placeholder="Required Phrase"
              className="border p-2 w-full mb-3"
              onChange={(e)=>setInclude(e.target.value)}
            />

            <button
              onClick={generateContent}
              className="bg-purple-500 text-white px-4 py-2 rounded w-full"
            >
              Generate Content
            </button>

            {contentResult && (
              <pre className="mt-4 bg-gray-100 p-3 text-sm overflow-auto">
                {contentResult}
              </pre>
            )}
          </div>
        )}

      </div>
    </div>
  );
}

export default App;
