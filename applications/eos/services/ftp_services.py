
from applications.eos.models.ftp import FtpInfo
from gluon.utils import logger


def check_ftp_connection_by_id(db, ftp_id):
    # type (string) -> bool
    try:
        row = db(db.ftp_management.id == ftp_id).select().first()
        ftp_info = FtpInfo(row.ftp_ip, row.ftp_port, row.ftp_user, row.ftp_password)
        if ftp_info.check_connection():
            return True
        return False
    except Exception as e:
        logger.error(str(e))
        return False

def check_ftp_status(data):
    from ftplib import FTP
    import ftplib
    res = True
    ftp_ip = data.data_server
    data_folder = data.data_folder
    username = data.username
    password = data.pwd
    ftp_port = data.data_server_port
    ftp = FTP()
    try:
        ftp.connect(ftp_ip, ftp_port)
        ftp.login(username, password)
        ftp.cwd(data_folder)
    except ftplib.all_errors:
        res = False
    finally:
        try:
            ftp.quit()
        except Exception as ex:
            pass
    return res
