from mdc._version import __version__


def mathify():
    """Generate a standalone PDF from the math input on stdin."""
    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    from contextlib import redirect_stderr, redirect_stdout
    from tempfile import NamedTemporaryFile, TemporaryDirectory

    from corgy import CorgyHelpFormatter
    from corgy.types import OutputDirectory

    from mdc.mdc import MDCMain

    class Formatter(CorgyHelpFormatter, RawDescriptionHelpFormatter):
        pass

    parser = ArgumentParser(
        formatter_class=Formatter,
        usage="echo <raw latex math> | mathify",
        description=(
            "\nexample:\n"
            "$ mathify\n"
            "\\exp{x}\n"
            "^D\n"
            "<path to a pdf file with the rendered math>"
        ),
    )
    parser.parse_args()

    with (
        NamedTemporaryFile(mode="x", suffix=".pdf", delete=False) as pdf_out_f,
        NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as log_f,
        TemporaryDirectory() as cache_dir,
    ):
        mdc_main = MDCMain(
            output_file=pdf_out_f,
            builtin_template="standalone",
            cache_dir=OutputDirectory(cache_dir),
            verbose=True,
        )

        with redirect_stdout(log_f), redirect_stderr(log_f):
            ret_code = mdc_main()
        if ret_code:
            print(f"mdc error code {ret_code}: check log file {log_f.name}")
        else:
            print(pdf_out_f.name)
