package HDT8P1;

import java.util.Vector;

public class VectorHeap<E extends Comparable<E>> implements PriorityQueue<E> {
    private Vector<E> heap;

    public VectorHeap() {
        heap = new Vector<>();
    }

    @Override
    public void add(E value) {
        heap.add(value);
        siftUp(heap.size() - 1);
    }

    @Override
    public E remove() {
        if (heap.isEmpty()) return null;

        E result = heap.get(0);
        heap.set(0, heap.get(heap.size() - 1));
        heap.remove(heap.size() - 1);

        if (!heap.isEmpty()) {
            siftDown(0);
        }
        return result;
    }

    private void siftUp(int index) {
        while (index > 0) {
            int parent = (index - 1) / 2;
            if (heap.get(parent).compareTo(heap.get(index)) <= 0) {
                break;
            }
            swap(parent, index);
            index = parent;
        }
    }

    private void siftDown(int index) {
        int size = heap.size();
        while (2 * index + 1 < size) {
            int left = 2 * index + 1;
            int right = 2 * index + 2;
            int smallest = left;

            if (right < size && heap.get(right).compareTo(heap.get(left)) < 0) {
                smallest = right;
            }
            if (heap.get(index).compareTo(heap.get(smallest)) <= 0) {
                break;
            }
            swap(index, smallest);
            index = smallest;
        }
    }

    private void swap(int i, int j) {
        E temp = heap.get(i);
        heap.set(i, heap.get(j));
        heap.set(j, temp);
    }

    @Override
    public boolean isEmpty() {
        return heap.isEmpty();
    }

    @Override
    public int size() {
        return heap.size();
    }
}

// Interfaz PriorityQueue simple
interface PriorityQueue<E> {
    void add(E value);
    E remove();
    boolean isEmpty();
    int size();
}