from vatf.executor import shell
import psutil

def test_double_kill():
    try:
        p = shell.bg("sleep 100")
        shell.kill(p)
        shell.kill(p)
    except psutil.NoSuchProcess:
        assert False
