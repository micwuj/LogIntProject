import os
import subprocess
import time

def monitor_folder(folder_path):
    # Tworzymy zbiór zawierający aktualne pliki w folderze
    current_files = set(os.listdir(folder_path))
    
    while True:
        # Pobieramy aktualną listę plików w folderze
        new_files = set(os.listdir(folder_path))
        
        # Sprawdzamy czy pojawił się nowy plik
        new_file = new_files - current_files
        
        # Jeżeli pojawił się nowy plik, wykonujemy go i usuwamy
        if new_file:
            new_file_name = new_file.pop()
            new_file_path = os.path.join(folder_path, new_file_name)
            print("Znaleziono nowy plik:", new_file_path)
            try:
                # Wykonujemy skrypt bashowy z ustawionym katalogiem roboczym na folder_path
                subprocess.run(["bash", new_file_name], check=True, cwd=folder_path)
                print("Skrypt wykonany pomyślnie.")
                # Usuwamy plik
                os.remove(new_file_path)
                print("Plik usunięty.")
            except subprocess.CalledProcessError as e:
                print("Błąd podczas wykonywania skryptu:", e)
            except FileNotFoundError:
                print("Nie można odnaleźć pliku:", new_file_path)
        
        # Aktualizujemy zbiór plików
        current_files = new_files
        
        # Oczekujemy przez 1 sekundę przed kolejnym sprawdzeniem
        time.sleep(1)

if __name__ == "__main__":
    cwd = os.getcwd()
    folder_path = cwd+"/scripts"  # Ścieżka do monitorowanego folderu
    monitor_folder(folder_path)
