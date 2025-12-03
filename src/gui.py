import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, ttk
from auth import register, login, logout, current_user
from core import process_message
from data_loader import load_info
from storage import append_to_json_list, write_json, read_json
from datetime import datetime
import json, os

INFO_PATH = "info.json"
CONV_DIR = "conversations"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MentorCORE - GUI")
        self.root.geometry("800x600")
        self.user = current_user()
        # CAMBIO 1.2: Cargar respuestas avanzadas
        self.respuestas, self.reglas, self.sinonimos, self.respuestas_avanzadas = load_info(INFO_PATH)
        self.modo = "basico"
        # La línea self.respuestas_avanzadas = {} original en el código del usuario se ha eliminado
        self.build_login_screen()
    
    def _append_user(self, text: str):
        self.txt_widget.config(state="normal")
        self.txt_widget.insert(tk.END, f"Tú: {text}\n")
        self.txt_widget.config(state="disabled")
        self.txt_widget.see(tk.END)

    def _append_bot(self, text: str):
        self.txt_widget.config(state="normal")
        self.txt_widget.insert(tk.END, f"MentorCORE: {text}\n")
        self.txt_widget.config(state="disabled")
        self.txt_widget.see(tk.END)

    def build_login_screen(self):
        for w in self.root.winfo_children(): w.destroy()
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)
        tk.Label(frame, text="Usuario").grid(row=0, column=0)
        user_entry = tk.Entry(frame); user_entry.grid(row=0, column=1)
        tk.Label(frame, text="Contraseña").grid(row=1, column=0)
        pass_entry = tk.Entry(frame, show="*"); pass_entry.grid(row=1, column=1)

        def do_login():
            u = user_entry.get().strip()
            p = pass_entry.get().strip()
            if login(u, p):
                messagebox.showinfo("OK", "Login exitoso")
                self.user = u
                self.build_chat_screen()
            else:
                messagebox.showerror("Error", "Credenciales inválidas")

        def do_register():
            u = user_entry.get().strip()
            p = pass_entry.get().strip()
            if register(u,p):
                messagebox.showinfo("OK","Usuario creado. Inicia sesión.")
            else:
                messagebox.showwarning("Aviso","Usuario ya existe")

        tk.Button(frame, text="Ingresar", command=do_login).grid(row=2, column=0)
        tk.Button(frame, text="Registrar", command=do_register).grid(row=2, column=1)

    def build_chat_screen(self):
        for w in self.root.winfo_children(): w.destroy()
        top = tk.Frame(self.root); top.pack(fill=tk.BOTH, expand=True)
        txt = scrolledtext.ScrolledText(top, state=tk.DISABLED)
        txt.pack(fill=tk.BOTH, expand=True)

        txt.config(state=tk.NORMAL)
        txt.insert(tk.END, "Bienvenido a MentorCORE, soy tu asistente del curso de Lenguajes de Programación. Escribe 'salir' para terminar. Escribe 'comandos' para listar todos los comandos disponibles.\n\n")
        txt.config(state=tk.DISABLED)

        bottom = tk.Frame(self.root); bottom.pack(fill=tk.X)
        entry = tk.Entry(bottom); entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        send_btn = tk.Button(bottom, text="Enviar", command=lambda: self.on_send(entry, txt))
        send_btn.pack(side=tk.RIGHT)

        # menu
        men = tk.Menu(self.root)
        men.add_command(label="Estadísticas", command=self.open_stats)
        men.add_command(label="Admin", command=self.open_admin)
        men.add_command(label="Cerrar sesión", command=self.do_logout)
        self.root.config(menu=men)

        # store references
        self.txt_widget = txt
        self.entry_widget = entry

    def do_logout(self):
        logout()
        self.user = None
        self.build_login_screen()

    def on_send(self, entry, txt_widget):
        msg = entry.get().strip()
        if not msg:
            return
        entry.delete(0, tk.END)
        # mostrar usuario
        txt_widget.config(state=tk.NORMAL)
        txt_widget.insert(tk.END, f"Tú: {msg}\n")
        txt_widget.config(state=tk.DISABLED)

        # --- CAMBIO 1.3: Procesamiento con comandos y modo avanzado ---

        msg_lower = msg.lower().strip()
        if msg_lower == "comandos":
            comandos_text = (
                "Comandos disponibles:\n"
                "- estadisticas: muestra análisis del uso del bot (gráfico de temas)\n"
                "- estadisticas hora: muestra análisis por horas\n"
                "- agregar sinonimo X = Y: añade un nuevo sinónimo\n"
                "- modo basico: cambia al modo básico\n"
                "- modo avanzado: cambia al modo avanzado\n"
                "- cerrar sesión: cierra sesión actual\n"
            )
            self._append_bot(comandos_text)
            return
        # cambiar modo
        if msg_lower == "modo avanzado":
            self.modo = "avanzado"
            self._append_bot("Modo avanzado activado.\n")
            return
        if msg_lower == "modo basico":
            self.modo = "basico"
            self._append_bot("Modo básico activado.\n")
            return
        # agregar sinonimo
        if msg_lower.startswith("agregar sinonimo"):
            try:
                # ejemplo: agregar sinonimo prof = profesor
                _, data = msg_lower.split("agregar sinonimo", 1)
                x, y = map(str.strip, data.split("="))

                self.sinonimos[x] = y

                # guardar en info.json
                with open(INFO_PATH, "r", encoding="utf-8") as f:
                    data_json = json.load(f)
                data_json.setdefault("sinonimos", {}).setdefault(y, [])
                # Solo añade el sinónimo si no existe ya para evitar duplicados en el archivo JSON
                if x not in data_json["sinonimos"][y]:
                    data_json["sinonimos"][y].append(x)
                
                with open(INFO_PATH, "w", encoding="utf-8") as f:
                    json.dump(data_json, f, ensure_ascii=False, indent=4)

                self._append_bot(f"Sinónimo agregado: {x} → {y}\n")
            except:
                self._append_bot("Formato incorrecto. Usa: agregar sinonimo X = Y\n")
            return
        # estadísticas normales
        if msg_lower == "estadisticas":
            import analysis
            # Se añade un try/except simple en caso de que 'analysis' no pueda importarse
            try:
                df, temas, horas = analysis.analisis_completo()
                analysis.grafico_temas(temas)
                self._append_bot("Estadísticas generadas (temas).\n")
            except ImportError:
                self._append_bot("Error: La librería 'analysis' no está disponible o incompleta.\n")
            return
        # estadísticas por hora
        if msg_lower == "estadisticas hora":
            import analysis
            try:
                df, temas, horas = analysis.analisis_completo()
                analysis.grafico_horas(horas)
                self._append_bot("Estadísticas por hora generadas.\n")
            except ImportError:
                self._append_bot("Error: La librería 'analysis' no está disponible o incompleta.\n")
            return
        # --- procesamiento normal del mensaje ---
        coincidence, response = process_message(msg, self.reglas, self.respuestas, self.sinonimos)

        # modo avanzado
        if self.modo == "avanzado" and coincidence in self.respuestas_avanzadas:
            response = self.respuestas_avanzadas[coincidence]

        # guardar conversacion
        user = current_user() or "anon"
        os.makedirs(CONV_DIR, exist_ok=True)
        conv_path = os.path.join(CONV_DIR, f"{user}.json")
        append_to_json_list(conv_path, "turnos", {"timestamp": datetime.now().isoformat(), "input": msg, "intent": coincidence, "response": response})

        # estadística
        # Se añade un try/except simple en caso de que 'ChatBot' no pueda importarse
        try:
            from ChatBot import registrar_estadistica
            registrar_estadistica(coincidence if coincidence else "fallback")
        except ImportError:
            # Si no se puede importar la función, simplemente se ignora y continúa
            pass
        
        self._append_bot(response + "\n")

    def open_stats(self):
        # abrir analysis.py o mostrar mini resúmen
        import analysis
        df, temas, horas = analysis.analisis_completo()
        # mostrar en ventana simple
        win = tk.Toplevel(self.root)
        win.title("Estadísticas")
        lbl = tk.Label(win, text=str(temas.to_dict()))
        lbl.pack()

    def open_admin(self):
        # ventana para agregar reglas/respuestas/sinonimos
        win = tk.Toplevel(self.root)
        win.title("Admin - Añadir contenido")
        tk.Label(win, text="Trigger (regex)").pack()
        trigger = tk.Entry(win); trigger.pack(fill=tk.X)
        tk.Label(win, text="Clave (topic)").pack()
        key = tk.Entry(win); key.pack(fill=tk.X)
        tk.Label(win, text="Respuesta básica").pack()
        basic = tk.Entry(win); basic.pack(fill=tk.X)
        tk.Label(win, text="Respuesta avanzada (opcional)").pack()
        adv = tk.Entry(win); adv.pack(fill=tk.X)

        def add_rule():
            trg = trigger.get().strip()
            k = key.get().strip()
            b = basic.get().strip()
            a = adv.get().strip()
            # Validaciones mínimas
            if not trg or not k or not b:
                messagebox.showerror("Error", "Trigger, Clave y Respuesta básica son obligatorios.")
                return

            # cargar info.json
            with open(INFO_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            # agregar regla y respuestas
            data.setdefault("reglas", []).append([trg, k])
            data.setdefault("respuestas", {})[k] = b
            if a:
                data.setdefault("respuestas_avanzadas", {})[k] = a
            # guardar
            with open(INFO_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("OK","Regla agregada. Reinicia la app para recargar reglas.")
        tk.Button(win, text="Agregar", command=add_rule).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()