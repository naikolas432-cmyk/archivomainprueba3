import pymysql

# Engañamos a Django sobre la versión de mysqlclient para evitar el ImproperlyConfigured
pymysql.version_info = (2, 2, 7, "final", 0)
pymysql.install_as_MySQLdb()