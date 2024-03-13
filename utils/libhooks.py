import os
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    try:
        from vatf.utils import config_handler
        config = config_handler.get_config()
    except config_handler.NoConfigException as nce:
        import sys
        print(f"{nce}", file = sys.stderr)
        return
    from pathlib import Path
    Path(config.status_file.dir_path).mkdir(parents=True, exist_ok=True)
    def create_empty_result_file(result):
        from vatf.utils import config_handler
        config = config_handler.get_config()
        with open(os.path.join(config.status_file.dir_path, result), 'w') as f:
            pass
    outcome = yield
    try:
        res = outcome.get_result()
    except Exception as e:
        res = f"False\n{e}"
    raw_res = res
    if isinstance(res, str):
        raw_res = "True" if "True" in res else "False"
    create_empty_result_file(str(raw_res))
    with open(os.path.join(config.status_file.dir_path, "status"), 'w') as f:
        f.write(f"{str(res)}\n")

