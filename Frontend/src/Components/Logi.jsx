
import React from "react";
import { Login } from "./API";
import { useForm } from "react-hook-form";
import { toast } from "react-hot-toast";
import { useNavigate } from "react-router-dom"; // Importante para saltar de página

const Logi = ({ setAx, ax }) => {
  const { register, handleSubmit } = useForm();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    // Función interna para manejar la promesa del toast
    const ejecutarLogin = async () => {
      try {
        await Login(data);
        // Si el backend de Django responde OK, navegamos a bienvenida
        navigate("/bienvenida");
      } catch (e) {
        throw e; // El toast capturará este error
      }
    };

    toast.promise(ejecutarLogin(), {
      loading: "Iniciando sesión...",
      success: "¡Bienvenido a Tuke!",
      error: "Error en las credenciales, intenta de nuevo.",
    });
  };

  return (
    <div className="flex flex-col gap-6 w-full justify-center items-center">
      <form
        className="w-full px-4 flex flex-col gap-6"
        onSubmit={handleSubmit(onSubmit)}
      >
        <div className="flex flex-col">
          <p className="text-lime-600 mb-1">Usuario</p>
          <input
            type="text"
            placeholder="Ejemplo: TuQueque . . ."
            className="rounded-2xl p-4 bg-lime-50 border-2 border-lime-300 focus:shadow-lg focus:shadow-lime-200 focus:outline-none focus:bg-white transition-all w-full"
            {...register("username", { required: true })}
          />
        </div>
        
        <div className="flex flex-col">
          <p className="text-lime-600 mb-1">Contraseña</p>
          <input
            type="password"
            placeholder="Full security"
            className="rounded-2xl p-4 bg-lime-50 border-2 border-lime-300 focus:shadow-lg focus:shadow-lime-200 focus:outline-none focus:bg-white transition-all w-full text-green-700"
            {...register("password", { required: true })}
          />
        </div>

        <button 
          type="submit"
          className="bg-lime-600 hover:bg-lime-700 text-white font-bold py-4 px-4 rounded-2xl transition-all hover:shadow-lg hover:shadow-lime-600 text-xl"
        >
          Ingresa a Tuke
        </button>
      </form>

      <div className="flex gap-2 mt-2">
        <p className="text-slate-500">¿Nuevo por aquí?</p>
        <button
          className="text-green-800 font-black hover:underline transition-all cursor-pointer"
          onClick={() => setAx(!ax)} // Esto vuelve a funcionar como antes
        >
          Crear cuenta Tuke
        </button>
      </div>
    </div>
  );
};

export default Logi;