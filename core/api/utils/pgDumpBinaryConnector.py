from dbbackup.db.postgresql import PgDumpBinaryConnector as CorePgDumpBinaryConnector, create_postgres_uri

class PgDumpBinaryConnector(CorePgDumpBinaryConnector):
    if_exists = False

    def _restore_dump(self, dump):
        dbname = create_postgres_uri(self)
        cmd = f"{self.restore_cmd} {dbname}"

        if self.single_transaction:
            cmd += " --single-transaction"
        if self.drop:
            cmd += " --clean"
        if self.if_exists:
            cmd += " --if-exists"
        cmd = f"{self.restore_prefix} {cmd} {self.restore_suffix}"
        stdout, stderr = self.run_command(cmd, stdin=dump, env=self.restore_env)
        return stdout, stderr