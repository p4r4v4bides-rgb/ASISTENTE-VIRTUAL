// src/Components/Bienvenida.jsx

/*const Bienvenida = () => {
    return (
    <div className="bg-white p-10 rounded-3xl shadow-2xl text-center">
        <h1 className="text-4xl font-bold text-green-800">¡Acceso Correcto!</h1>
        <p className="text-slate-600 mt-4">Bienvenido a tu espacio en Tuke.</p>
    </div>
    );
};

export default Bienvenida;*/

import React, { useState } from "react";

const Bienvenida = () => {
  const [mensaje, setMensaje] = useState("");

  // Funciones para controlar el estado de Tuke (despertar/dormir) y enviar mensajes
  const despertarTuke = () => {
    fetch('http://localhost:5005/despertar', { method: 'POST' })
      .catch(err => console.error("¿Está corriendo el script de Python?", err));
  };

  const dormirTuke = () => {
    // Apuntamos a la nueva ruta /dormir
    fetch('http://localhost:5005/dormir', { method: 'POST' })
      .catch(err => console.error("Error al intentar dormir a Tuke:", err));
  };

  const hablarConTuke = (e) => {
    e.preventDefault();
    if (!mensaje.trim()) return;

    fetch('http://localhost:5005/hablar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mensaje: mensaje })
    });
    setMensaje("");
  };

  return (
    <div className="w-screen h-screen bg-slate-100 flex p-6 gap-6">
      
      {/* SECCIÓN IZQUIERDA: CHAT ASISTENTE */}
      <div className="flex-1 bg-white rounded-3xl shadow-xl flex flex-col overflow-hidden border border-lime-200">
        <div className="bg-lime-600 p-4 text-white font-bold text-center">
          Chat con Tuke
        </div>
        
        <div className="flex-1 p-4 overflow-y-auto bg-slate-50">
          {/* Aquí irían los globos de texto del historial */}
          <div className="bg-lime-100 p-3 rounded-2xl self-start max-w-[80%] mb-4">
            ¡Hola! Soy Tuke, tu asistente. ¿En qué te ayudo hoy?
          </div>
        </div>

        <form onSubmit={hablarConTuke} className="p-4 bg-white border-t flex gap-2">
          <input 
            type="text" 
            value={mensaje}
            onChange={(e) => setMensaje(e.target.value)}
            placeholder="Escribe a Tuke..."
            className="flex-1 p-3 rounded-xl border-2 border-lime-200 focus:outline-none focus:border-lime-500"
          />
          <button type="submit" className="bg-lime-600 text-white px-6 rounded-xl hover:bg-lime-700">
            Enviar
          </button>
        </form>
      </div>

      {/* SECCIÓN DERECHA: WIDGETS Y CONTROLES */}
      <div className="w-80 flex flex-col gap-6">
        
        {/* PANEL DE CONTROL DEL TUKE*/}
        <div className="bg-white p-6 rounded-3xl shadow-lg border border-green-100 text-center">
          <h3 className="font-bold text-green-800 mb-4">Control de Asistente</h3>
          <div className="flex flex-col gap-3">
            <button 
              onClick={despertarTuke}
              className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 rounded-xl transition-all"
            >
              Despertar Tuke
            </button>
            <button 
              onClick={dormirTuke}
              className="bg-slate-400 hover:bg-slate-500 text-white font-bold py-2 rounded-xl transition-all"
            >
              Dormir Tuke
            </button>
          </div>
        </div>

        {/* NOVEDADES / NOTIFICACIONES */}
        <div className="flex-1 bg-white p-6 rounded-3xl shadow-lg border border-blue-100 overflow-y-auto">
          <h3 className="font-bold text-blue-800 mb-2 italic">Novedades</h3>
          <hr className="mb-3"/>
          <ul className="text-sm flex flex-col gap-3">
            <li className="bg-blue-50 p-2 rounded-lg border-l-4 border-blue-400">
              📌 Revisar diagramas de flujo de Sistemas II.
            </li>
            <li className="bg-orange-50 p-2 rounded-lg border-l-4 border-orange-400">
              🚀 Nueva actualización de Tuke v2.0 disponible.
            </li>
          </ul>
        </div>

        {/* CALENDARIO SIMPLE, Se va a modiicar despues */}
        <div className="bg-white p-6 rounded-3xl shadow-lg border border-purple-100">
          <h3 className="font-bold text-purple-800 text-center mb-2">Calendario</h3>
          <div className="text-center">
            <p className="text-4xl font-black text-slate-700">{new Date().getDate()}</p>
            <p className="text-slate-500 uppercase tracking-widest text-sm">
              {new Date().toLocaleString('es-ES', { month: 'long' })}
            </p>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Bienvenida;