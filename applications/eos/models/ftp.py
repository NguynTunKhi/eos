import ftplib

FTP_TIME_OUT = 5


class FtpInfo:
    def __init__(self, ip, port, user, password, timeout=FTP_TIME_OUT):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout

    def setTimeout(self, timeout):
        self.timeout = timeout

    def check_connection(self):  # -> bool
        try:
            ftp = ftplib.FTP()
            ftp.connect(self.ip, self.port, self.timeout)
            ftp.login(self.user, self.password)
        except ftplib.all_errors:
            return False
        finally:
            # ftp.quit()
            try:
                ftp.quit()
            except Exception as ex:
                pass
        return True
