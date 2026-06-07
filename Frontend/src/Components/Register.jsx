import React from "react";
import { toast } from "react-hot-toast";
import { useForm } from "react-hook-form";
import { Registe } from "./API";

const Register = ({ setAx, ax }) => {
  const { register, handleSubmit } = useForm();

  const onSubmit = handleSubmit((data) => {
    async function ejecutarRegistro() {
      try {
        
        await Registe(data);
        
        setAx(!ax); 

      } catch (e) {
        
        throw new Error(e);
      }
    }

    toast.promise(ejecutarRegistro(), {
      loading: "Registrando...",
      success: "¡Registrado exitosamente!",
      error: "Datos incorrectos, por favor verifica tu información.",
    });
  });

  return (
    <div className="flex flex-col gap-6 w-full justify-center items-center">
      <form
        className="w-full px-20 flex flex-col gap-6"
        onSubmit={onSubmit} 
      >
        <div className="flex flex-col">
          <p className="text-lime-600">Nombre completo</p>
          <input
            type="text"
            placeholder="Ejemplo: TuQueque . . ."
            className="rounded-2xl p-4 bg-lime-50 border-2 border-lime-300 placeholder:text-slate-400 focus:border-white/30 focus:shadow-lg focus:shadow-lime-600 focus:outline-none focus:bg-white transition-all w-full"
            {...register("name")}
          />
        </div>
        <div className="flex flex-col">
          <p className="text-lime-600">Nombre de usuario</p>
          <input
            type="text"
            placeholder="Ejemplo: TuQueque . . ."
            className="rounded-2xl p-4 bg-lime-50 border-2 border-lime-300 placeholder:text-slate-400 focus:border-white/30 focus:shadow-lg focus:shadow-lime-600 focus:outline-none focus:bg-white transition-all w-full"
            {...register("username")}
          />
        </div>
        <div className="flex flex-col ">
          <p className="text-lime-600">Contraseña</p>
          <input
            type="password"
            placeholder="Full security  "
            className="rounded-2xl p-4 bg-lime-50 border-2 border-lime-300 placeholder:text-slate-400 focus:border-white/30 focus:shadow-lg focus:shadow-lime-600 focus:outline-none focus:bg-white transition-all w-full text-green-700"
            {...register("password")}
          />
        </div>

        <button 
          type="submit"
          className="bg-lime-600 hover:bg-lime-700 text-white font-bold py-4 px-4 rounded-2xl transition-all hover:shadow-lg hover:shadow-lime-600 text-xl"
        >
          Registrarme en Tuke
        </button>
      </form>
      
      <button
        className="bg-lime-600 hover:bg-lime-700 text-white font-bold py-4 px-4 rounded-2xl transition-all hover:shadow-lg hover:shadow-lime-600 text-xl"
        onClick={() => setAx(!ax)}
      >
        Volver
      </button>
    </div>
  );
};

export default Register;