from common import *

# ---------------------------------------------
# step 1 -> compile benchmarks
# ---------------------------------------------
for benchmark_application in benchmark_applications:
    # Change current directory to samples/<benchmark_application>
    application_path = os.path.join(samples_directory, benchmark_application)
    os.chdir(application_path)

    application_built = subprocess.run(f"go build", shell=True)
    
    if application_built.returncode != 0:
        print(f"Building {benchmark_application} failed!")
        exit()

    run_command = f"./{benchmark_application} -timing -report-all " \
            f"-metric-file-name {output_metric_file}"

    run_successfully = subprocess.run(run_command, shell=True)
    
    if run_successfully.returncode != 0:
        print(f"Running the application {benchmark_application} failed!")
        exit()
    counter += 1

