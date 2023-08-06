from functools import wraps, partial
from pathlib import Path

def magicdir(_func=None, *, dir):
    artifact = 'magicdir'
    if _func is None: return partial(magicdir, dir=dir)
    @wraps(_func)
    def func(self):
        from io import BytesIO
        from tarfile import TarFile
        existing = getattr(self, artifact, None)
        Path(dir).mkdir(exist_ok=True)
        if existing:
            buf = BytesIO(existing)
            with TarFile(mode='r', fileobj=buf) as tar:
                tar.extractall()
        _func(self)
        buf = BytesIO()
        with TarFile(mode='w', fileobj=buf) as tar:
            tar.add(dir)
        setattr(self, artifact, buf.getvalue())
    return func

STEP_DECORATORS = [magicdir]
