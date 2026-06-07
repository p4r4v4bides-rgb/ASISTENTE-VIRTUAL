import React, { useState, useEffect, useRef } from "react";

const Bienvenida = () => {
  // HOOKS DE ESTADO (Chat)
  const [mensaje, setMensaje] = useState("");
  const [cargando, setCargando] = useState(false);
  const [historial, setHistorial] = useState([]); 

  // HOOKS DE ESTADO (Tareas)
  const [tareas, setTareas] = useState([]);
  const [mostrarFormTarea, setMostrarFormTarea] = useState(false);
  const [tituloTarea, setTituloTarea] = useState("");
  const [fechaTarea, setFechaTarea] = useState("");
  const [horaTarea, setHoraTarea] = useState("");
  const [idTareaEditando, setIdTareaEditando] = useState(null);

  // Controla el mes que se está viendo en el calendario 
  const [fechaCalendario, setFechaCalendario] = useState(new Date());

  const usuarioId = localStorage.getItem("usuario_id");
  const scrollRef = useRef(null);

  // Carga de datos iniciales
  useEffect(() => {
    if (!usuarioId) return;

    const cargarHistorialBD = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/historial/${usuarioId}/`); 
        if (res.ok) {
          const data = await res.json();
          if (data.length > 0) setHistorial(data);
          else setHistorial([{ emisor: "tuke", texto: "¡Hola! Soy Tuke, tu asistente. ¿En qué te ayudo hoy?" }]);
        }
      } catch (err) {
        console.error("Error cargando historial:", err);
        setHistorial([{ emisor: "tuke", texto: "¡Hola! Soy Tuke, tu asistente. ¿En qué te ayudo hoy?" }]);
      }
    };

    const cargarTareasBD = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/tareas/?usuario_id=${usuarioId}`);
        if (res.ok) {
          const data = await res.json();
          setTareas(data);
        }
      } catch (err) {
        console.error("Error cargando tareas:", err);
      }
    };

    cargarHistorialBD();
    cargarTareasBD();
  }, [usuarioId]);

  // Autoscroll
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [historial, cargando]);

  // Bloqueo de seguridad
  if (!usuarioId) {
    return (
      <div className="w-screen h-screen flex flex-col items-center justify-center bg-slate-100 p-4">
        <div className="bg-white p-8 rounded-3xl shadow-xl border border-lime-200 text-center max-w-md">
          <h2 className="text-2xl font-bold text-slate-700 mb-3">No has iniciado sesión</h2>
          <p className="text-slate-500 mb-6">Por favor, ingresa con tu cuenta de Tuke para acceder a tu historial de chat personalizado.</p>
          <a href="/" className="inline-block bg-lime-600 hover:bg-lime-700 text-white font-bold px-6 py-3 rounded-xl transition-colors shadow-md">Ir al Login</a>
        </div>
      </div>
    );
  }

  // Controles del Asistente
  const despertarTuke = () => { fetch('http://localhost:5005/despertar', { method: 'POST' }).catch(console.error); };
  const dormirTuke = () => { fetch('http://localhost:5005/dormir', { method: 'POST' }).catch(console.error); };
  
  const cerrarSesion = () => {
    localStorage.removeItem("usuario_id");
    window.location.href = "/";
  };

  // Tareas: Limpiar Formulario
  const limpiarFormularioTarea = () => {
    setTituloTarea("");
    setFechaTarea("");
    setHoraTarea("");
    setIdTareaEditando(null);
    setMostrarFormTarea(false);
  };

  // Tareas: Iniciar Edición
  const iniciarEdicion = (tarea) => {
    setIdTareaEditando(tarea.id);
    setTituloTarea(tarea.titulo);
    setFechaTarea(tarea.fecha);
    setHoraTarea(tarea.hora);
    setMostrarFormTarea(true);
  };

  // Tareas: Eliminar
  const eliminarTarea = async (id) => {
    if (!window.confirm("¿Seguro que deseas eliminar esta tarea permanentemente?")) return;
    try {
      const response = await fetch(`http://localhost:8000/api/tareas/${id}/`, { method: 'DELETE' });
      if (response.ok) {
        setTareas(prev => prev.filter(t => t.id !== id));
      } else {
        alert("❌ Error al intentar borrar la tarea.");
      }
    } catch (error) {
      alert("🔌 Error de conexión con el servidor.");
    }
  };

  // Tareas: Guardar (Crear / Editar)
  const guardarTarea = async (e) => {
    e.preventDefault();
    if (!tituloTarea.trim() || !fechaTarea) {
      alert("⚠️ El título y la fecha son obligatorios.");
      return;
    }

    try {
      if (idTareaEditando) {
        const response = await fetch(`http://localhost:8000/api/tareas/${idTareaEditando}/`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ titulo: tituloTarea, fecha_limite: fechaTarea, hora_limite: horaTarea })
        });

        if (response.ok) {
          setTareas(prev => prev.map(t => 
            t.id === idTareaEditando ? { ...t, titulo: tituloTarea, fecha: fechaTarea, hora: horaTarea } : t
          ));
          limpiarFormularioTarea();
        } else alert("❌ Error al actualizar la tarea.");

      } else {
        const response = await fetch('http://localhost:8000/api/tareas/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ usuario_id: usuarioId, titulo: tituloTarea, fecha_limite: fechaTarea, hora_limite: horaTarea })
        });

        if (response.ok) {
          const resData = await response.json();
          setTareas(prev => [...prev, { id: resData.id, titulo: tituloTarea, fecha: fechaTarea, hora: horaTarea }]);
          
          // Mueve el calendario al mes de la tarea creada para verla al instante
          const [anio, mes] = fechaTarea.split("-");
          setFechaCalendario(new Date(anio, mes - 1, 1));
          
          limpiarFormularioTarea();
        } else alert("❌ Error al guardar la nueva tarea.");
      }
    } catch (error) {
      alert("🔌 Error de conexión con el servidor.");
    }
  };

  // Lógica del chat con Tuke
  const hablarConTuke = async (e) => {
    e.preventDefault();
    if (!mensaje.trim()) return;

    const textoUsuario = mensaje;
    setMensaje(""); 
    setHistorial(prev => [...prev, { emisor: "yo", texto: textoUsuario }]);
    setCargando(true); 

    try {
      const response = await fetch('http://localhost:8000/api/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensaje: textoUsuario, usuario_id: usuarioId })
      });
      
      const data = await response.json();

      if (data.accion === "abrir_musica") {
        if (data.plataforma === "spotify" && data.url_spotify) {
          setHistorial(prev => [...prev, { emisor: "tuke", texto: data.respuesta }]);
          window.open(data.url_spotify, '_blank');
        } else if (data.plataforma === "youtube" && data.url_youtube) {
          setHistorial(prev => [...prev, { emisor: "tuke", texto: data.respuesta }]);
          window.open(data.url_youtube, '_blank');
        } else {
          setHistorial(prev => [...prev, { emisor: "tuke", texto: data.respuesta || "¿Dónde prefieres escuchar esto?", opcionesMusica: { spotify: data.url_spotify, youtube: data.url_youtube } }]);
        }
      } else {
        setHistorial(prev => [...prev, { emisor: "tuke", texto: data.respuesta }]);
      }
    } catch (error) {
      setHistorial(prev => [...prev, { emisor: "tuke", texto: "Uy, parece que mi servidor inteligente en Django está apagado. ¡Enciéndelo!" }]);
    } finally {
      setCargando(false); 
    }
  };

  // ==========================================
  // LÓGICA DEL CALENDARIO DINÁMICO
  // ==========================================
  const mesActual = fechaCalendario.getMonth();
  const anioActual = fechaCalendario.getFullYear();
  
  // Días que tiene el mes (28, 29, 30, 31)
  const diasEnMes = new Date(anioActual, mesActual + 1, 0).getDate();
  // Día de la semana en que empieza el mes (0 = Dom, 1 = Lun, etc.)
  const primerDiaMes = new Date(anioActual, mesActual, 1).getDay();

  const cambiarMes = (incremento) => {
    setFechaCalendario(new Date(anioActual, mesActual + incremento, 1));
  };

  // Nombres de meses para mostrar
  const meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

  const renderizarDias = () => {
    const celdas = [];
    const hoy = new Date();

    // Rellenamos los espacios vacíos antes del día 1
    for (let i = 0; i < primerDiaMes; i++) {
      celdas.push(<div key={`vacio-${i}`} className="p-1"></div>);
    }

    // Dibujamos los días reales del mes
    for (let dia = 1; dia <= diasEnMes; dia++) {
      // Formateamos la fecha a YYYY-MM-DD para compararla con las tareas de la BD
      const fechaStr = `${anioActual}-${String(mesActual + 1).padStart(2, '0')}-${String(dia).padStart(2, '0')}`;
      
      // Comprobamos si es "hoy"
      const esHoy = hoy.getDate() === dia && hoy.getMonth() === mesActual && hoy.getFullYear() === anioActual;
      
      // Buscamos si hay alguna tarea en esta fecha exacta
      const tareasDelDia = tareas.filter(t => t.fecha === fechaStr);
      const tieneTareas = tareasDelDia.length > 0;

      celdas.push(
        <div 
          key={dia} 
          title={tieneTareas ? `${tareasDelDia.length} tarea(s) pendiente(s)` : ""}
          className={`h-8 w-8 mx-auto flex items-center justify-center rounded-full text-sm relative cursor-default transition-all
            ${esHoy ? 'bg-purple-600 text-white font-bold shadow-md' : 'text-slate-700 hover:bg-slate-200'}
            ${tieneTareas && !esHoy ? 'bg-blue-100 font-bold text-blue-900 border border-blue-300' : ''}
          `}
        >
          {dia}
          {/* Pequeño punto indicador si hay tareas */}
          {tieneTareas && !esHoy && (
            <span className="absolute bottom-1 w-1 h-1 bg-blue-600 rounded-full"></span>
          )}
        </div>
      );
    }
    return celdas;
  };


  return (
    <div className="w-screen h-screen bg-slate-100 flex p-6 gap-6">
      {/* SECCIÓN IZQUIERDA: CHAT */}
      <div className="flex-1 bg-white rounded-3xl shadow-xl flex flex-col overflow-hidden border border-lime-200">
        <div className="bg-lime-600 p-4 text-white font-bold text-center">Chat con Tuke</div>
        
        <div ref={scrollRef} className="flex-1 p-4 overflow-y-auto bg-slate-50 flex flex-col gap-4 scroll-smooth">
          {historial.map((msg, index) => (
            <div key={index} className={`max-w-[80%] flex flex-col ${msg.emisor === "yo" ? "self-end" : "self-start"}`}>
              <div className={`p-3 rounded-2xl ${msg.emisor === "yo" ? "bg-lime-200 rounded-tr-none text-right shadow-sm" : "bg-lime-100 rounded-tl-none border border-lime-200 shadow-sm"}`}>
                {msg.texto}
              </div>
              {msg.opcionesMusica && (
                <div className="flex gap-2 mt-2 ml-2">
                  {msg.opcionesMusica.spotify && (
                    <button onClick={() => window.open(msg.opcionesMusica.spotify, '_blank')} className="bg-green-500 hover:bg-green-600 text-white text-sm px-4 py-2 rounded-full shadow flex items-center gap-1">🎵 Spotify</button>
                  )}
                  {msg.opcionesMusica.youtube && (
                    <button onClick={() => window.open(msg.opcionesMusica.youtube, '_blank')} className="bg-red-500 hover:bg-red-600 text-white text-sm px-4 py-2 rounded-full shadow flex items-center gap-1">▶️ YouTube Music</button>
                  )}
                </div>
              )}
            </div>
          ))}
          {cargando && <div className="bg-lime-100 p-3 rounded-2xl self-start rounded-tl-none border border-lime-200 shadow-sm animate-pulse text-lime-800 font-medium text-sm max-w-[80%]">Tuke está escribiendo...</div>}
        </div>

        <form onSubmit={hablarConTuke} className="p-4 bg-white border-t flex gap-2">
          <input type="text" value={mensaje} onChange={(e) => setMensaje(e.target.value)} placeholder="Escribe a Tuke..." className="flex-1 p-3 rounded-xl border-2 border-lime-200 focus:outline-none focus:border-lime-500" />
          <button type="submit" className="bg-lime-600 text-white px-6 rounded-xl hover:bg-lime-700 transition-colors">Enviar</button>
        </form>
      </div>

      {/* SECCIÓN DERECHA: CONTROLES Y WIDGETS */}
      <div className="w-80 flex flex-col gap-6">
        
        {/* PANEL DE CONTROL */}
        <div className="bg-white p-5 rounded-3xl shadow-lg border border-green-100 text-center shrink-0">
          <h3 className="font-bold text-green-800 mb-4">Control de Asistente</h3>
          <div className="flex flex-col gap-3">
            <button onClick={despertarTuke} className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 rounded-xl transition-all text-sm">Despertar Tuke</button>
            <button onClick={dormirTuke} className="bg-slate-400 hover:bg-slate-500 text-white font-bold py-2 rounded-xl transition-all text-sm">Dormir Tuke</button>
            <button onClick={cerrarSesion} className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 rounded-xl transition-all mt-1 text-sm">Cerrar Sesión</button>
          </div>
        </div>

        {/* SECCIÓN NOVEDADES / TAREAS */}
        <div className="flex-1 bg-white p-5 rounded-3xl shadow-lg border border-blue-100 overflow-y-auto flex flex-col min-h-0">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-bold text-blue-800 italic">Novedades</h3>
            <button 
              onClick={() => {
                if (mostrarFormTarea) limpiarFormularioTarea();
                else setMostrarFormTarea(true);
              }}
              className="bg-blue-600 hover:bg-blue-700 text-white text-[10px] uppercase font-bold px-3 py-1.5 rounded-lg transition-all"
            >
              {mostrarFormTarea ? "Cancelar" : "+ Tarea"}
            </button>
          </div>
          <hr className="mb-3"/>

          {mostrarFormTarea && (
            <form onSubmit={guardarTarea} className="bg-blue-50 p-3 rounded-xl border border-blue-200 flex flex-col gap-2 mb-4 text-xs">
              <p className="font-bold text-blue-700 uppercase tracking-wide text-[10px]">{idTareaEditando ? "✏️ Editando Tarea" : "🚀 Nueva Tarea"}</p>
              <input type="text" placeholder="¿Qué debes hacer?" value={tituloTarea} onChange={(e) => setTituloTarea(e.target.value)} required className="p-2 rounded-lg border focus:outline-none w-full" />
              <div className="flex gap-2">
                <input type="date" value={fechaTarea} onChange={(e) => setFechaTarea(e.target.value)} required className="p-2 rounded-lg border focus:outline-none flex-1" />
                <input type="time" value={horaTarea} onChange={(e) => setHoraTarea(e.target.value)} className="p-2 rounded-lg border focus:outline-none flex-1" />
              </div>
              <button type="submit" className="bg-blue-600 text-white p-2 rounded-lg font-bold hover:bg-blue-700 transition-colors">
                {idTareaEditando ? "Actualizar Tarea" : "Guardar Tarea"}
              </button>
            </form>
          )}

          <ul className="text-sm flex flex-col gap-3 flex-1 overflow-y-auto pr-1">
            {tareas.length > 0 ? (
              tareas.map((tarea) => (
                <li key={tarea.id} className="bg-blue-50 p-3 rounded-lg border-l-4 border-blue-400 flex justify-between items-start gap-2 shadow-sm">
                  <div className="flex flex-col flex-1">
                    <span className="font-semibold text-slate-700 leading-tight">📌 {tarea.titulo}</span>
                    <span className="text-[11px] text-slate-500 mt-1">⏰ {tarea.fecha} {tarea.hora && `| ${tarea.hora}`}</span>
                  </div>
                  <div className="flex gap-1 shrink-0">
                    <button onClick={() => iniciarEdicion(tarea)} className="p-1 hover:bg-blue-200 rounded transition-colors" title="Editar">✏️</button>
                    <button onClick={() => eliminarTarea(tarea.id)} className="p-1 hover:bg-red-200 rounded transition-colors" title="Eliminar">❌</button>
                  </div>
                </li>
              ))
            ) : (
              <p className="text-slate-400 text-xs text-center mt-4">No tienes tareas pendientes.</p>
            )}
          </ul>
        </div>

        {/* CALENDARIO DINÁMICO */}
        <div className="bg-white p-5 rounded-3xl shadow-lg border border-purple-200 shrink-0 select-none">
          {/* Navegación del mes */}
          <div className="flex justify-between items-center mb-3 text-purple-900">
            <button onClick={() => cambiarMes(-1)} className="hover:bg-purple-100 p-1 rounded-lg px-2 transition-colors font-bold">&lt;</button>
            <h3 className="font-black text-center text-sm uppercase tracking-widest">
              {meses[mesActual]} {anioActual}
            </h3>
            <button onClick={() => cambiarMes(1)} className="hover:bg-purple-100 p-1 rounded-lg px-2 transition-colors font-bold">&gt;</button>
          </div>
          
          {/* Cabecera de los días */}
          <div className="grid grid-cols-7 text-center text-[10px] font-bold text-slate-400 mb-2">
            <div>Do</div><div>Lu</div><div>Ma</div><div>Mi</div><div>Ju</div><div>Vi</div><div>Sa</div>
          </div>
          
          {/* Cuadrícula de fechas */}
          <div className="grid grid-cols-7 gap-y-1 text-center">
            {renderizarDias()}
          </div>
        </div>

      </div>
    </div>
  );
};

export default Bienvenida;