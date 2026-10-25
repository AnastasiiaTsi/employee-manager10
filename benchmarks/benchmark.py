from time import perf_counter
import statistics
from employee_manager.analytics import (
    generate_employees, 
    calculate_statistics_python, 
    process_employee_scores
)
from employee_manager.numpy_analytics import calculate_statistics_numpy
from employee_manager.parallel import (
    process_scores_threads, 
    process_scores_processes
)
from employee_manager.caching import (
    get_department_statistics, 
    invalidate_cache
)

def benchmark(func, *args, repeats=5):
    """
    Вимірює середній час виконання функції за кілька повторів.
    
    :param func: функція для вимірювання
    :param args: аргументи для функції
    :param repeats: кількість повторів
    :return: кортеж (середній час, результат)
    """
    times = []
    result = None
    for _ in range(repeats):
        start = perf_counter()
        result = func(*args)
        times.append(perf_counter() - start)
    
    return statistics.mean(times), result

def main():
    print("Generating data (100 000 employees)...")
    employees = generate_employees(100_000)
    
    # 1. Статистика (Python baseline vs NumPy)
    py_time, py_res = benchmark(calculate_statistics_python, employees)
    np_time, np_res = benchmark(calculate_statistics_numpy, employees)
    
    print(f"\n--- Statistics ---")
    print(f"Python baseline: {py_time:.4f} s")
    print(f"NumPy vectorized:{np_time:.4f} s | Speedup: {py_time/np_time:.2f}x")
    
    # 2. CPU-bound навантаження (Sequential vs Threads vs Processes)
    seq_time, _ = benchmark(process_employee_scores, employees)
    thr_time, _ = benchmark(process_scores_threads, employees, 4)
    proc_time, _ = benchmark(process_scores_processes, employees, 4)
    
    print(f"\n--- CPU-bound processing (GIL impact) ---")
    print(f"Sequential:       {seq_time:.4f} s")
    print(f"Threads (4):      {thr_time:.4f} s | Speedup: {seq_time/thr_time:.2f}x")
    print(f"Processes (4):    {proc_time:.4f} s | Speedup: {seq_time/proc_time:.2f}x")
    
    # 3. Caching (lru_cache)
    print(f"\n--- Caching (Department Statistics) ---")
    # Для кешу передаємо кортеж, оскільки lru_cache вимагає хешованих аргументів
    emp_tuple = tuple(employees)
    
    t0 = perf_counter()
    get_department_statistics(emp_tuple, "IT")
    cold_time = perf_counter() - t0
    print(f"Cache cold:       {cold_time:.4f} s")
    
    t0 = perf_counter()
    get_department_statistics(emp_tuple, "IT")
    warm_time = perf_counter() - t0
    print(f"Cache warm:       {warm_time:.6f} s | Speedup: {cold_time/warm_time:.0f}x")
    
    print("\nCache info before invalidation:", get_department_statistics.cache_info())
    invalidate_cache()
    print("Cache info after invalidation: ", get_department_statistics.cache_info())

if __name__ == "__main__":
    main()