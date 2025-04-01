package HDT8P1;

// Nombre del archivo: VectorHeapTest.java
import org.junit.Test;
import static org.junit.Assert.*;

public class VectorHeapTest {
    @Test
    public void testAddAndRemove() {
        VectorHeap<Paciente> heap = new VectorHeap<>();

        // Agregar pacientes
        heap.add(new Paciente("Juan Perez", "fractura de pierna", "C"));
        heap.add(new Paciente("Maria Ramirez", "apendicitis", "A"));
        heap.add(new Paciente("Lorenzo Toledo", "chikungunya", "E"));
        heap.add(new Paciente("Carmen Sarmientos", "dolores de parto", "B"));

        // Verificar tamaño
        assertEquals(4, heap.size());

        // Verificar orden de remoción
        assertEquals("Maria Ramirez, apendicitis, A", heap.remove().toString());
        assertEquals("Carmen Sarmientos, dolores de parto, B", heap.remove().toString());
        assertEquals("Juan Perez, fractura de pierna, C", heap.remove().toString());
        assertEquals("Lorenzo Toledo, chikungunya, E", heap.remove().toString());

        // Verificar que está vacío
        assertTrue(heap.isEmpty());
    }
}