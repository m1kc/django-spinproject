_CONTENT = {
	"base.py": """\
from django.db.backends.postgresql import base


try:
	get_psycopg_version = base.psycopg_version
except AttributeError:		# For older django versions
	get_psycopg_version = base.psycopg2_version


PSYCOPG_VERSION_MAJOR: int = get_psycopg_version()[0]		# Final cannot be used (python 3.8+ required)


if PSYCOPG_VERSION_MAJOR < 3:
	class DatabaseWrapper(base.DatabaseWrapper):
		def get_new_connection(self, conn_params):
			conn = super(DatabaseWrapper, self).get_new_connection(conn_params)
			conn.set_session(readonly=True)
			return conn
else:
	class DatabaseWrapper(base.DatabaseWrapper):
		def get_new_connection(self, conn_params):
			conn = super().get_new_connection(conn_params)
			conn.read_only = True
			return conn
"""
}
