import sys
from streamlit import cli as stcli


def main() -> None:
    sys.argv = [
        "streamlit",
        "run",
        "botpress_nlu_testing/gui.py",
        "--server.port",
        "8501",
        "--theme.base",
        "dark",
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
