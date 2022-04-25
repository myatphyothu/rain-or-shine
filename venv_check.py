import sys

def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

def in_virtualenv():
    venv = get_base_prefix_compat() != sys.prefix
    return 'Am I in virtual env? ==> ' + ('yes' if venv == True else 'no')

if __name__ == '__main__':
    print(in_virtualenv())