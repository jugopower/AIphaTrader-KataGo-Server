@app.get("/health")

def health():

    katago_bin = os.getenv("KATAGO_BIN", "/opt/katago/katago")

    katago_model = os.getenv("KATAGO_MODEL", "/opt/katago/model.bin.gz")

    katago_config = os.getenv(

        "KATAGO_CONFIG",

        "/app/config/analysis.cfg",

    )

    checks = {

        "katago_binary": (

            os.path.isfile(katago_bin)

            and os.access(katago_bin, os.X_OK)

        ),

        "katago_model": os.path.isfile(katago_model),

        "katago_config": os.path.isfile(katago_config),

    }

    missing = []

    if not checks["katago_binary"]:

        missing.append(katago_bin)

    if not checks["katago_model"]:

        missing.append(katago_model)

    if not checks["katago_config"]:

        missing.append(katago_config)

    katago_ready = all(checks.values())

    return {

        "status": "healthy",

        "katago_ready": katago_ready,

        "mode": "katago" if katago_ready else "demo",

        "build": "Build018.4",

        "checks": checks,

        "missing": missing,

    }

    
