import tkinter as tk
from tkinter import ttk
from datetime import datetime
import multiprocessing
import threading
import time
import platform
import psutil

# Constants
TEST_DURATION = 30  # Test duration in seconds
REFERENCE_OPERATIONS = 10**9  # Hypothetical max operations for score scaling
PROCESS_TERMINATION_TIMEOUT = 5  # Timeout in seconds for process termination
INTENSITY = 10**8  # Intensity for integer operations to stress CPU

def cpu_benchmark_worker(counter):
    """Perform continuous intensive integer operations to stress CPU."""
    count = 0
    for _ in range(INTENSITY):
        count += (count * 3 + 1) % 123456789  # Intensive integer operation
        counter.value += 1

def calculate_score(total_operations):
    """Calculate score based on the number of operations completed."""
    score = min(1000, int((total_operations / REFERENCE_OPERATIONS) * 1000))
    return score

def sample_cpu_speed():
    """Sample the current CPU frequency in MHz."""
    return psutil.cpu_freq().current if psutil.cpu_freq() else 0

def run_test():
    """Runs the CPU benchmark test, tracks CPU speed, and updates the GUI with results."""
    print("Starting CPU benchmark test...")
    # Prepare shared counters and process list
    counters = [multiprocessing.Value("i", 0) for _ in range(multiprocessing.cpu_count())]
    processes = []

    # Start worker processes
    for counter in counters:
        p = multiprocessing.Process(target=cpu_benchmark_worker, args=(counter,))
        processes.append(p)
        p.start()

    # Track CPU speed over the test duration
    speeds = []
    start_time = time.time()
    
    while time.time() - start_time < TEST_DURATION:
        # Sample CPU speed and store it
        speeds.append(sample_cpu_speed())
        time.sleep(0.5)  # Sample every half second for better speed tracking

    # Ensure all processes are terminated
    print("Terminating processes...")
    for p in processes:
        p.terminate()
        p.join()  # Wait for the process to terminate
        
    # Additional check to enforce process termination
    for p in processes:
        if p.is_alive():
            p.join(PROCESS_TERMINATION_TIMEOUT)  # Wait with timeout
            if p.is_alive():
                print("Process did not terminate, forcing termination...")
                p.terminate()
                p.join()  # Ensure termination
    print("Processes terminated.")

    # Calculate total operations and score
    total_operations = sum(counter.value for counter in counters)
    score = calculate_score(total_operations)

    # Calculate mean CPU speed
    mean_speed = sum(speeds) / len(speeds) if speeds else 0

    # Get CPU info
    cpu_info = platform.processor() or "Unknown CPU"

    # Update GUI with results
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    root.after(0, lambda: finalize_test(timestamp, cpu_info, mean_speed, score))

def finalize_test(timestamp, cpu_info, mean_speed, score):
    """Displays test results in the main GUI as a table."""
    print("Finalizing test...")
    # Re-enable the button here
    start_button.config(state=tk.NORMAL)

    # Insert results into the table
    result_table.insert("", "end", values=(timestamp, cpu_info, f"{mean_speed:.2f} MHz", f"{score} / 1000"))

def start_test():
    """Starts the test in a new thread to keep the GUI responsive."""
    print("Starting the test thread...")
    start_button.config(state=tk.DISABLED)  # Disable the button while the test runs
    test_thread = threading.Thread(target=run_test)
    test_thread.start()

if __name__ == "__main__":
    # GUI setup
    root = tk.Tk()
    root.title("Multi-Core CPU Benchmark")
    root.geometry("600x300")

    # UI Elements
    label = tk.Label(root, text="CPU Performance Test", font=("Arial", 14))
    label.pack(pady=10)

    start_button = tk.Button(root, text="Start Test", command=start_test, font=("Arial", 12))
    start_button.pack(pady=5)

    # Treeview for displaying the results in a table format
    columns = ("Timestamp", "CPU Model", "Mean CPU Speed", "CPU Score")
    result_table = ttk.Treeview(root, columns=columns, show="headings")
    result_table.heading("Timestamp", text="Timestamp")
    result_table.heading("CPU Model", text="CPU Model")
    result_table.heading("Mean CPU Speed", text="Mean CPU Speed (MHz)")
    result_table.heading("CPU Score", text="CPU Score")

    # Set column widths for better display
    result_table.column("Timestamp", width=150)
    result_table.column("CPU Model", width=150)
    result_table.column("Mean CPU Speed", width=200)
    result_table.column("CPU Score", width=80)

    result_table.pack(pady=10, fill="x")

    # Run the app
    root.mainloop()
