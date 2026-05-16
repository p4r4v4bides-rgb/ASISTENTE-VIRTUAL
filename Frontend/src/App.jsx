
import { Routes, Route } from "react-router-dom";
import Home from "./Components/Home";
import Bienvenida from "./Components/Bienvenida";
import { Toaster } from "react-hot-toast";

function App() {
  return (
    
    <div className="bg-linear-to-br from-green-900 via-green-600 to-lime-600 min-h-screen flex items-center justify-center p-4">
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/bienvenida" element={<Bienvenida />} />
      </Routes>

      <Toaster
        position="top-center"
        reverseOrder={true}
        toastOptions={{
          style: {
            background: "rgba(255, 255, 255, 0.3)",
            backdropFilter: "blur(16px)",
            border: "1px solid rgba(255, 255, 255, 0.3)",
            padding: "16px",
            color: "#334155",
            borderRadius: "16px",
            boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
          },
          className: "!shadow-2xl !max-w-md",
        }}
      />
    </div>
  );
}

export default App;