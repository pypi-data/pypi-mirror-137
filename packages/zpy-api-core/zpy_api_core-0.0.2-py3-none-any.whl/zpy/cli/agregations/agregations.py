adds = {
    "di.py": {
        "type": "file",
        "module": "db-oracle",
        "path": "src/di.py",
        "code": {
            "imports": [
                "from zpy.utils import get_env_or_throw as var\n",
                "from zdb.oracle import ZOracle, ZDBConfig\n"
            ],
            "blocks": [
                "\n",
                "db_config: ZDBConfig = ZDBConfig(\"DB_USER\", \"DB_PASSWORD\", \"DB_NAME\",\"DB_HOST\", 1521,service=\"XE\")\n"
                "db_mngr: ZOracle = ZOracle.setup_of(db_config)\n"
                "\n",
                "if var('ENVIRONMENT') == 'local':\n",
                "   # Setup only the environment is local.\n",
                "   db_mngr.init_local_client(path= var('ORACLE_CLIENT_PATH'))\n",
                "\n"
            ]
        }
    }
}
