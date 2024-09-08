def get_db_connection_string(
    username: str, password: str, env: str, name: str, host: str, port: str
) -> str:
    if env == "production":  # UNIX socket for host in cloud run
        return f"postgresql:///{name}?host={host}&port={port}&user={username}&password={password}"
    else:
        return f"postgresql://{username}:{password}@{host}:{port}/{name}"
