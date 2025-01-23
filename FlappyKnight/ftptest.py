from ftplib import FTP

def increment_and_update_ftp_file(ftp_url, ftp_path, filename, username, password):     # Connect to the FTP server
    ftp = FTP(ftp_url)
    ftp.login(user=username, passwd=password)

    # Change to the directory where the file is located
    ftp.cwd(ftp_path)

     # Read the current content of the file
    with open(filename, 'wb') as local_file:
        ftp.retrbinary('RETR ' + filename, local_file.write)

    # Increment the value
    with open(filename, 'r') as local_file:
        current_value = int(local_file.read())
        new_value = current_value + 1

        # Write the updated value back to the file
    with open(filename, 'w') as local_file:
        local_file.write(str(new_value))

        # Upload the modified file back to the FTP server
    with open(filename, 'rb') as local_file:
        ftp.storbinary('STOR ' + filename, local_file)

    ftp.quit()

# Example usage:
ftp_url = "luan.sternblick.ch"
ftp_path = "/ftp"
filename = "downloads.txt"
username = "luanftp.sternblick.ch"
password = "Luan-Ftp12"  # Replace with a more secure method in a production environment

increment_and_update_ftp_file(ftp_url, ftp_path, filename, username, password)
