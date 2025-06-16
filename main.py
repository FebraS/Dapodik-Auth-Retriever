# GPL-3.0 license
"""
    Dapodik-Auth-Retriever/main.py
    
    Copyright (C) 2025  Febra S
"""

import urllib.parse
import os
import re

def extractParam(queryString, paramName):
    # Regex untuk mencari 'nama_parameter=' diikuti oleh nilai (yang tidak mengandung '&', spasi, atau baris baru)
    pattern = rf"{re.escape(paramName)}=([^&\s\n\r]*)"
    match = re.search(pattern, queryString)
    
    if match:
        paramValueEncoded = match.group(1)
        decodedValue = urllib.parse.unquote_plus(paramValueEncoded)
        # Kembalikan nilai yang didekode jika tidak kosong, jika tidak kembalikan None
        return decodedValue if decodedValue else None 
    return None # Parameter tidak ditemukan

def main():
    """
    Fungsi utama untuk membaca log, mengekstrak data, dan menulis ke file output.
    """
    # Jalur file log.
    logFilePath = "C:/Program Files (x86)/Dapodik/webserver/logs/access.log"
    outputFileName = "OutputRetriever.txt"

    print(f"Mulai mengekstrak kredensial dari: {logFilePath}")
    print(f"Hasil akan disimpan ke: {outputFileName}")

    try:
        # Buka file log untuk dibaca. 'errors=ignore' membantu mengatasi potensi masalah encoding.
        with open(logFilePath, 'r', encoding='utf-8', errors='ignore') as logFile:
            # Buka file output untuk menulis.
            with open(outputFileName, 'w', encoding='utf-8') as outputFile:
                foundEntriesCount = 0
                for lineNum, line in enumerate(logFile, 1):
                    # Cari pola "GET /" yang menandakan permintaan web
                    getRequestStart = line.find("GET /")
                    if getRequestStart != -1:
                        # Cari tanda '?' yang menandakan awal string kueri
                        queryStringStart = line.find('?', getRequestStart)
                        if queryStringStart != -1:
                            # Pindahkan posisi setelah '?'
                            queryStringStart += 1
                            # Cari pola " HTTP/1.1" yang menandakan akhir string kueri
                            httpVersionEnd = line.find(" HTTP/1.1", queryStringStart)

                            if httpVersionEnd != -1:
                                # Ekstrak string kueri mentah
                                rawQueryString = line[queryStringStart:httpVersionEnd]

                                # Ekstrak dan dekode setiap parameter
                                registrationCode = extractParam(rawQueryString, "kode_registrasi")
                                username = extractParam(rawQueryString, "username")
                                password = extractParam(rawQueryString, "password")

                                # Hanya tulis ke file output jika ketiga parameter ditemukan DAN tidak kosong
                                if registrationCode and username and password:
                                    outputFile.write("------- Kredensial Ditemukan -------\n")
                                    outputFile.write(f"Kode Registrasi: {registrationCode}\n")
                                    outputFile.write(f"Username: {username}\n")
                                    outputFile.write(f"Password: {password}\n")
                                    outputFile.write("------------------------------------\n\n")
                                    foundEntriesCount += 1
                                    
        print(f"\nProses ekstraksi selesai. Hasil disimpan di **{outputFileName}**.")
        print(f"Total entri kredensial yang berhasil diekstrak: {foundEntriesCount}")

    except FileNotFoundError:
        print(f"Error: File log tidak ditemukan di '{logFilePath}'.")
        print("Pastikan jalur file sudah benar dan file tersebut ada.")
    except PermissionError:
        print(f"Error: Tidak dapat mengakses file log '{logFilePath}'.")
        print("Pastikan Anda memiliki izin baca untuk file tersebut.")
    except Exception as e:
        print(f"Terjadi kesalahan tak terduga: {e}")

if __name__ == "__main__":
    main()
