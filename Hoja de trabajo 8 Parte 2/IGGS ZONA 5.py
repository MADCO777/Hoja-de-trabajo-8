import simpy
import random
import matplotlib.pyplot as plt
import numpy as np


random.seed(10)  # Para reproducibilidad


TIEMPO_SIMULACION = 1440  # 1 día en minutos (24 horas * 60 minutos)
INTERVALO_LLEGADA_DIA_NORMAL = 30  # Promedio de llegada cada 30 minutos en días normales
INTERVALO_LLEGADA_FIN_SEMANA = 20  # Más pacientes: cada 20 minutos
INTERVALO_LLEGADA_FESTIVO = 15     # Aún más pacientes: cada 15 minutos

# Tiempos de procesamiento
TIEMPO_TRIAGE = 10
TIEMPO_DOCTOR = 20
TIEMPO_LABORATORIO = 30
TIEMPO_RAYOS_X = 15

# Recursos iniciales 
NUM_ENFERMERAS = 2
NUM_DOCTORES = 2
NUM_LABORATORIOS = 1
NUM_RAYOS_X = 1

tiempos_espera = []
tiempos_totales = []

class SalaEmergencias:
    def __init__(self, env, num_enfermeras, num_doctores, num_laboratorios, num_rayos_x, intervalo_llegada):
        self.env = env
        self.enfermeras = simpy.PriorityResource(env, capacity=num_enfermeras)
        self.doctores = simpy.PriorityResource(env, capacity=num_doctores)
        self.laboratorios = simpy.PriorityResource(env, capacity=num_laboratorios)
        self.rayos_x = simpy.PriorityResource(env, capacity=num_rayos_x)
        self.intervalo_llegada = intervalo_llegada

    def proceso_triage(self, paciente, severidad):
        with self.enfermeras.request(priority=severidad) as req:
            yield req
            yield self.env.timeout(TIEMPO_TRIAGE)

    def proceso_atencion_doctor(self, paciente, severidad):
        with self.doctores.request(priority=severidad) as req:
            yield req
            yield self.env.timeout(TIEMPO_DOCTOR)

    def proceso_laboratorio(self, paciente, severidad):
        with self.laboratorios.request(priority=severidad) as req:
            yield req
            yield self.env.timeout(TIEMPO_LABORATORIO)

    def proceso_rayos_x(self, paciente, severidad):
        with self.rayos_x.request(priority=severidad) as req:
            yield req
            yield self.env.timeout(TIEMPO_RAYOS_X)

def paciente(env, nombre, sala):
    llegada = env.now

    # Triage: asignar severidad
    # 1-5, 1 es más urgente

    severidad = random.randint(1, 5)
    yield env.process(sala.proceso_triage(nombre, severidad))

    # Atención por doctor
    inicio_espera_doctor = env.now
    yield env.process(sala.proceso_atencion_doctor(nombre, severidad))
    tiempo_espera_doctor = env.now - inicio_espera_doctor - TIEMPO_DOCTOR

    # 50% de probabilidad de necesitar laboratorio
    tiempo_espera_lab = 0
    if random.random() < 0.5:
        inicio_espera_lab = env.now
        yield env.process(sala.proceso_laboratorio(nombre, severidad))
        tiempo_espera_lab = env.now - inicio_espera_lab - TIEMPO_LABORATORIO

    # 30% de probabilidad de necesitar rayos X
    tiempo_espera_rayos = 0
    if random.random() < 0.3:
        inicio_espera_rayos = env.now
        yield env.process(sala.proceso_rayos_x(nombre, severidad))
        tiempo_espera_rayos = env.now - inicio_espera_rayos - TIEMPO_RAYOS_X

    # Calculo de los tiempo
    tiempo_total = env.now - llegada
    tiempo_espera_total = tiempo_espera_doctor + tiempo_espera_lab + tiempo_espera_rayos
    tiempos_espera.append(tiempo_espera_total)
    tiempos_totales.append(tiempo_total)

def generador_pacientes(env, sala):
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / sala.intervalo_llegada))
        env.process(paciente(env, f"Paciente-{i}", sala))
        i += 1

def simular_dia(tipo_dia):
    global tiempos_espera, tiempos_totales
    tiempos_espera = []
    tiempos_totales = []

    # Seleccionar intervalo según el tipo de día
    if tipo_dia == "normal":
        intervalo = INTERVALO_LLEGADA_DIA_NORMAL
    elif tipo_dia == "fin_semana":
        intervalo = INTERVALO_LLEGADA_FIN_SEMANA
    else:  # festivo
        intervalo = INTERVALO_LLEGADA_FESTIVO

    # Crear entorno y sala
    env = simpy.Environment()
    sala = SalaEmergencias(env, NUM_ENFERMERAS, NUM_DOCTORES, NUM_LABORATORIOS, NUM_RAYOS_X, intervalo)
    env.process(generador_pacientes(env, sala))
    env.run(until=TIEMPO_SIMULACION)

    return np.mean(tiempos_espera) if tiempos_espera else 0, np.mean(tiempos_totales) if tiempos_totales else 0

# Simular diferentes configuraciones de recursos
resultados = []
for num_enfermeras in range(1, 4):
    for num_doctores in range(1, 4):
        NUM_ENFERMERAS = num_enfermeras
        NUM_DOCTORES = num_doctores
        espera_normal, total_normal = simular_dia("normal")
        espera_fin, total_fin = simular_dia("fin_semana")
        espera_festivo, total_festivo = simular_dia("festivo")
        resultados.append({
            "enfermeras": num_enfermeras,
            "doctores": num_doctores,
            "espera_normal": espera_normal,
            "espera_fin": espera_fin,
            "espera_festivo": espera_festivo,
            "total_normal": total_normal,
            "total_fin": total_fin,
            "total_festivo": total_festivo
        })

# Generar gráficas
enfermeras_doctores = [f"{r['enfermeras']}EN-{r['doctores']}Doc" for r in resultados]
espera_normal = [r["espera_normal"] for r in resultados]
espera_fin = [r["espera_fin"] for r in resultados]
espera_festivo = [r["espera_festivo"] for r in resultados]

plt.figure(figsize=(10, 6))
plt.plot(enfermeras_doctores, espera_normal, label="Día normal", marker="o")
plt.plot(enfermeras_doctores, espera_fin, label="Fin de semana", marker="o")
plt.plot(enfermeras_doctores, espera_festivo, label="Festivo", marker="o")
plt.xlabel("Configuración EN=Enfermeras / Doc=Doctores")
plt.ylabel("Tiempo promedio de espera")
plt.title("Tiempos de espera según los recursos seleccionados")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("tiempos_espera.png")
plt.show()