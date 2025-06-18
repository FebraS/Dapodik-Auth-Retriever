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
    
    # Fungsi utama untuk membaca log, mengektrak data, dan menulis ke file output.
    
    # Jalur file access.log
    logFilePath = "C:/Program Files (x86)/Dapodik/webserver/logs/access.log"
    # Nama file output
    outputFileName = "OutputRetriever.txt"

    # Inisialisasi logFile dan outputFile ke None. Ini penting jika ada exception sebelum logFile dibuka.
    logFile = None 
    outputFile = None

    try:
        # **Langkah 1: Buka file output terlebih dahulu.**
        outputFile = open(outputFileName, 'w', encoding='utf-8')
        
        try:
            # **Langkah 2: Coba buka file log.**
            logFile = open(logFilePath, 'r', encoding='utf-8', errors='ignore')
            
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

                            # Hanya tulis ke file output jika ketiga parameter ditemukan dan tidak kosong
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
            print(f"Error: File log tidak ditemukan.")
            print("Pastikan Dapodik terpasang di perangkat Anda.")
            # Kita bisa menulis pesan error ini juga ke file output jika diinginkan
            outputFile.write(f"Error: File log tidak ditemukan. \nPastikan Dapodik terpasang di perangkat Anda.\n")
        except PermissionError:
            print(f"Error: Tidak dapat mengakses file log.")
            print("Pastikan Anda memiliki izin baca untuk file tersebut.")
            # Kita bisa menulis pesan error ini juga ke file output jika diinginkan
            outputFile.write(f"Error: Tidak dapat mengakses file log. \nPastikan Anda memiliki izin baca untuk file tersebut.\n")
        except Exception as e:
            print(f"Terjadi kesalahan tak terduga: {e}")
            outputFile.write(f"Terjadi kesalahan tak terduga: {e}\n")
        
    except Exception as e:
        # Tangani error jika outputFile tidak bisa dibuat
        print(f"Error: Tidak dapat membuat file output '{outputFileName}'.")
        print(f"Detail error: {e}")
    
    finally:
        # Pastikan file log ditutup jika berhasil dibuka
        if logFile:
            logFile.close()
        # Pastikan file output ditutup jika berhasil dibuka
        if outputFile:
            outputFile.close()

if __name__ == "__main__":
    main()
