package HDT8P1;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;

public class EmergenciaVectorHeap {
    public static void main(String[] args) {
        VectorHeap<Paciente> cola = new VectorHeap<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String opcion = "";

        // Leer pacientes desde el archivo
        try (BufferedReader br = new BufferedReader(new FileReader("HDT8P1/pacientes.txt"))) {
            String linea;
            while ((linea = br.readLine()) != null) {
                String[] datos = linea.split(",");
                Paciente paciente = new Paciente(datos[0].trim(), datos[1].trim(), datos[2].trim());
                cola.add(paciente);
            }
        } catch (IOException e) {
            System.out.println("No se pudo leer el archivo de pacientes. Se comenzará con una cola vacía.");
        }

        do {
            try {
                System.out.println("Seleccione una opción:");
                System.out.println("1. Agregar paciente");
                System.out.println("2. Atender paciente (eliminar de la cola)");
                System.out.println("3. Salir");
                opcion = reader.readLine().trim();

                switch (opcion) {
                    case "1":
                        System.out.print("Ingrese el nombre del paciente: ");
                        String nombre = reader.readLine().trim();

                        System.out.print("Ingrese el síntoma del paciente: ");
                        String sintoma = reader.readLine().trim();

                        System.out.print("Ingrese el código de emergencia (A, B, C, etc.): ");
                        String codigoEmergencia = reader.readLine().trim();

                        Paciente paciente = new Paciente(nombre, sintoma, codigoEmergencia);
                        cola.add(paciente);
                        System.out.println("Paciente agregado.");

                        // Guardar el paciente en el archivo
                        try (BufferedWriter bw = new BufferedWriter(new FileWriter("HDT8P1/pacientes.txt", true))) {
                            bw.write(nombre + ", " + sintoma + ", " + codigoEmergencia);
                            bw.newLine();
                        } catch (IOException e) {
                            System.out.println("Error al guardar el paciente en el archivo.");
                        }
                        break;

                    case "2":
                        if (!cola.isEmpty()) {
                            System.out.println("Atendiendo paciente: " + cola.remove());
                        } else {
                            System.out.println("No hay pacientes en la cola.");
                        }
                        break;

                    case "3":
                        System.out.println("Saliendo del programa.");
                        break;

                    default:
                        System.out.println("Opción no válida. Intente de nuevo.");
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        } while (!opcion.equals("3"));

        System.out.println("Pacientes restantes en la cola:");
        while (!cola.isEmpty()) {
            System.out.println(cola.remove());
        }
    }
}