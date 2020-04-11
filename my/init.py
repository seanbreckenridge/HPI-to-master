'''
A hook to insert user's config directory into Python's search path.

- Ideally that would be in __init__.py (so it's executed without having to import explicityly)
  But, with namespace packages, we can't have __init__.py in the parent subpackage
  (see http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html#the-init-py-trap)

  Please let me know if you are aware of a better way of dealing with this!
'''


# separate function to present namespace pollution
def setup_config():
    from pathlib import Path
    import sys
    import warnings

    # TODO use appdir??
    cfg_dir = Path('~/.config').expanduser()
    mycfg_dir = cfg_dir / 'my'

    if not mycfg_dir.exists():
        warnings.warn(f"my.config package isn't found! (expected at {mycfg_dir}). This might result in issues.")
        from . import mycfg_stub as mycfg
        sys.modules['my.config'] = mycfg
    else:
        mp = str(mycfg_dir)
        if mp not in sys.path:
            sys.path.insert(0, mp)
        print("UPDATED PATH") # TODO FIXME remove

    try:
        import my.config
    except ImportError as ex:
        warnings.warn(f"Importing my.config failed! (error: {ex}). This might result in issues.")


setup_config()
del setup_config
