import os
import subprocess
import time
import json

def run_subprocess_with_live_output(command, cwd):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
    output_lines = []

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            output_lines.append(output.strip())

    process.communicate()  # Wait for the process to finish
    return process.returncode, output_lines

def monitor_folder(data_folder, scripts_folder):
    current_files = set(os.listdir(data_folder))

    while True:
        new_files = set(os.listdir(data_folder))
        new_json_files = new_files - current_files

        for new_file_name in new_json_files:
            if new_file_name.endswith('.json'):
                new_file_path = os.path.join(data_folder, new_file_name)
                print("Znaleziono nowy plik JSON:", new_file_path)

                try:
                    with open(new_file_path, 'r') as json_file:
                        data = json.load(json_file)
                        # tu zmienic na nazwe skryptu z
                        # script_name = "LogIntTesterScript.sh"
                        script_name = "read.sh"
                        script_path = os.path.join(scripts_folder, script_name)

                        for _ in data:
                            for integration_data in _:
                                print("Data:", integration_data)
                                print("Wykonywanie skryptu:", script_name)
                                
                                # Porcjowanie JSONA na mniejsz - problem bash + adb
                                tmp_data_folder = os.path.join(os.getcwd(), "scripts")
                                os.makedirs(tmp_data_folder, exist_ok=True)
                                tmp_data_file = os.path.join(tmp_data_folder, "tmp_data.json")
                                with open(tmp_data_file, 'w') as f:
                                    json.dump(integration_data, f)
                                time.sleep(1)

                                command = ["bash", script_path]
                                return_code, output = run_subprocess_with_live_output(command, scripts_folder)

                                for line in output:
                                    print(line)

                                if return_code == 0:
                                    print("Skrypt wykonany pomyślnie.")
                                else:
                                    print(f"Skrypt zakończony z błędem, kod powrotu: {return_code}")

                        os.remove(new_file_path)
                        # os.remove(tmp_data_file)
                        print("Plik JSON usunięty.")
                except json.JSONDecodeError:
                    print("Błąd dekodowania pliku JSON:", new_file_path)
                except subprocess.CalledProcessError as e:
                    print("Błąd podczas wykonywania skryptu:", e)
                except FileNotFoundError:
                    print("Nie można odnaleźć skryptu:", script_path)

        current_files = new_files
        time.sleep(1)

if __name__ == "__main__":
    data_folder = os.path.join(os.getcwd(), "data")  # Folder do monitorowania
    scripts_folder = os.path.join(os.getcwd(), "scripts")  # Folder zawierający skrypty
    monitor_folder(data_folder, scripts_folder)
