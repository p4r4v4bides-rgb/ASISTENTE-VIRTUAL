
import { useState } from "react";
import x from "/imagen.png";
import Logi from "./Logi";
import Register from "./Register";

const Home = () => {
  const [ax, setAx] = useState(false);

  return (
    <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl flex flex-col items-center px-6 py-12 gap-6">
      <div className="shadow-sm shadow-lime-700 w-fit h-fit rounded-3xl">
        <img src={x} alt="Tuke" className="w-40 h-40 object-contain" />
      </div>
      
      <div className="flex flex-col gap-4 justify-center items-center">
        <h1 className="font-bold text-4xl text-center text-green-800 mt-2">
          Bienvenido a Tuke
        </h1>
        <p className="text-lime-600 text-center">
          Accede a tu espacio Tuke
        </p>
      </div>

      {/* Lógica de intercambio interna */}
      {ax ? (
        <Register setAx={setAx} ax={ax} />
      ) : (
        <Logi setAx={setAx} ax={ax} />
      )}
    </div>
  );
};

export default Home;