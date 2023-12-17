class FtpRepo:

    def __init__(self, db):
        self.db = db

    def get_all(self ,auth ):
        try:
            if auth is not None and auth.user['type'] == 1:
                rows = self.db(self.db.ftp_management.ftp_administration_level == auth.user['agent_id']).select(self.db.ftp_management.ALL)
            else:
                rows = self.db().select(self.db.ftp_management.ALL)
            return rows
        except Exception as ex:
            raise ex

    def get_ftp_by_id(self, ftp_id):
        try:
            row = self.db(self.db.ftp_management.id == ftp_id).select().first()
            return row
        except Exception as ex:
            raise ex
