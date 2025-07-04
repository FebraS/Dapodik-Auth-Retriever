# GPL-3.0 license
"""
    Dapodik-Auth-Retriever/main.py
    
    Copyright (C) 2025  Febra S
"""

import urllib.parse
import os
import re

def extractParam(content, paramName):
    """
    Mengekstrak nilai parameter dari sebuah string konten.
    Regex mencari 'nama_parameter=' diikuti oleh nilainya.
    """
    # Pola regex untuk menemukan nama_parameter=nilai
    # Nilai adalah semua karakter kecuali '&', spasi, atau karakter baris baru
    pattern = rf"{re.escape(paramName)}=([^&\s\n\r]*)"
    match = re.search(pattern, content)
    
    if match:
        paramValueEncoded = match.group(1)
        # Dekode nilai jika ada karakter khusus (misal: %40 untuk @)
        decodedValue = urllib.parse.unquote_plus(paramValueEncoded)
        return decodedValue if decodedValue else None
    return None

def main():
    """
    Fungsi utama untuk membaca file input, mengekstrak parameter yang ditentukan,
    dan menulis hasilnya ke file output.
    """
    # File input yang akan dibaca
    inputFilePath = "C:/Program Files (x86)/Dapodik/webserver/logs/access.log"
    # File output untuk menyimpan hasil
    outputFileName = "OutputRetriever.txt" 

    # Daftar parameter yang akan diekstrak
    paramsToExtract = ["npsn", "sekolah_id", "kode_registrasi", "username", "password"]
    
    foundData = {}

    try:
        # Buka file input untuk dibaca
        with open(inputFilePath, 'r', encoding='utf-8', errors='ignore') as inputFile:
            # Baca seluruh konten file ke dalam satu string
            fileContent = inputFile.read()

            # Ekstrak setiap parameter dari konten file
            for param in paramsToExtract:
                value = extractParam(fileContent, param)
                if value:
                    foundData[param] = value
        
        # Tulis data yang ditemukan ke file output
        with open(outputFileName, 'w', encoding='utf-8') as outputFile:
            if foundData:
                outputFile.write("------- Kredensial Ditemukan -------\n")
                for key, value in foundData.items():
                    outputFile.write(f"{key.replace('_', ' ').title()}: {value}\n")
                outputFile.write("------------------------------\n")
                print(f"Proses ekstraksi berhasil. Hasil disimpan di file '{outputFileName}'.")
                print(f"   Total data yang ditemukan: {len(foundData)}")
            else:
                message = "Tidak ada parameter yang cocok ditemukan di dalam file."
                outputFile.write(message + "\n")
                print(f"{message}")

    except FileNotFoundError:
        message = f"Error: File log tidak ditemukan. \nPastikan Dapodik terpasang di perangkat Anda."
        print(message)
        # Tulis pesan error ke file output
        try:
            with open(outputFileName, 'w', encoding='utf-8') as outputFile:
                outputFile.write(message + "\n")
        except IOError:
            # Gagal menulis ke file output
            pass
            
    except Exception as e:
        message = f"Terjadi kesalahan tak terduga: {e} \nPastikan Anda memiliki izin baca untuk file tersebut."
        print(message)
        # Tulis pesan error ke file output
        try:
            with open(outputFileName, 'w', encoding='-utf8') as outputFile:
                outputFile.write(message + "\n")
        except IOError:
            # Gagal menulis ke file output
            pass

if __name__ == "__main__":
    main()
