import pkgutil
import re
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from io import StringIO
from typing import List, Optional, Sequence

if sys.version_info >= (3, 9):
    from typing import Annotated, Literal
else:
    from typing_extensions import Annotated

    if sys.version_info >= (3, 8):
        from typing import Literal
    else:
        from typing_extensions import Literal

from corgy import Corgy, CorgyHelpFormatter
from corgy.types import (
    InputTextFile,
    KeyValuePairs,
    LazyOutputDirectory,
    OutputBinFile,
    OutputDirectory,
)

from ._version import __version__

__all__ = ("TEMPLATE_RESOURCES", "MDCMain")

TEMPLATE_RESOURCES = {
    "iclr": ["iclr.bst", "iclr.sty"],
    "icml": ["icml.bst", "icml.sty"],
    "neurips": ["neurips.sty"],
}


class MDCMain(Corgy):
    verbose: Annotated[bool, "make latexmk verbose", ["-v", "--verbose"]] = False

    input_file: Annotated[
        Optional[InputTextFile],
        "input file (if not specified, input will be read from stdin)",
        ["input"],
    ] = None
    output_file: Annotated[
        Optional[OutputBinFile],
        "write output to this file instead of stdout",
        ["-o", "--output-file"],
    ] = None

    builtin_template: Annotated[
        Literal[
            "iclr", "icml", "neurips", "note", "simple", "standalone", "stylish", "stub"
        ],
        "use one of the built-in templates",
        ["-t", "--builtin-template"],
    ] = "simple"
    custom_template_file: Annotated[
        Optional[InputTextFile], "use a custom template", ["-T", "--custom-template"],
    ] = None

    cache_dir: Annotated[
        OutputDirectory, "directory for storing dependencies", ["-c", "--cache-dir"],
    ] = LazyOutputDirectory(".mdc")
    ignore_cache: Annotated[
        bool, "don't use existing contents of the cache directory"
    ] = False

    build_dir: Annotated[
        OutputDirectory, "directory for latexmk build files", ["-d", "--build-dir"],
    ] = LazyOutputDirectory(".mdc/_build")
    rebuild: Annotated[bool, "build from scratch by passingn `-gg` to latexmk"] = False

    from_: Annotated[str, "pandoc input format", ["-f", "--from"]] = "markdown"

    bibliography: Annotated[
        Optional[InputTextFile],
        "bibliography argument for pandoc",
        ["-b", "--bibliography"],
    ] = None
    bib_type: Annotated[
        Literal["natbib", "biblatex"],
        "bibliography type sent to pandoc",
        ["-B", "--bib-type"],
    ] = "natbib"

    include: Annotated[
        Sequence[InputTextFile], "files to include before body", ["-i", "--include"]
    ] = ()

    appendix: Annotated[
        Optional[InputTextFile], "appendix tex file", ["-a", "--appendix"]
    ] = None

    meta: Annotated[
        KeyValuePairs, "additional meta variables to pass to pandoc"
    ] = KeyValuePairs(
        {
            "figPrefix": "Figure",
            "eqnPrefix": "Equation",
            "tblPrefix": "Table",
            "lstPrefix": "List",
            "secPrefix": "Section",
        }
    )

    def_img_ext: Annotated[
        str, "default image extension for pandoc", ["-x", "--def-img-ext"]
    ] = "pdf"

    def build_pandoc_cmd(self) -> List[str]:
        """Build required pandoc command."""
        cmd = ["pandoc"]

        cmd.append(f"--from={self.from_}")
        cmd.append("--to=latex")
        cmd.append("--wrap=none")

        if self.custom_template_file is not None:
            cmd.append(f"--template={self.custom_template_file}")
        else:
            # Use `self.builtin_template`.
            template_path = self.cache_dir / f"{self.builtin_template}.tex"
            if self.ignore_cache or not template_path.exists():
                template_data = pkgutil.get_data(
                    "mdc", f"templates/{self.builtin_template}.tex"
                )
                if not template_data:
                    raise AssertionError(
                        f"failed to load '{self.builtin_template}' template: "
                        f"installation might be corrupt: try reinstalling"
                    )
                with template_path.open("wb") as _f1:
                    _f1.write(template_data)
            cmd.append(f"--template={template_path}")

        if self.bibliography is not None:
            cmd.append(f"--bibliography={self.bibliography}")
            cmd.append(f"--{self.bib_type}")

        cmd.append("--filter=pandoc-crossref")

        for i in self.include:
            cmd.append(f"--include-before-body={i}")

        for mk, mv in self.meta.items():
            cmd.append(f"--metadata={mk}={mv}")
        cmd.append(f"--metadata=dotmdc={self.cache_dir}")

        if self.appendix is not None:
            cmd.append(f"--metadata=appendix={self.appendix}")

        cmd.append(f"--default-image-extension={self.def_img_ext}")

        if self.input_file is not None:
            cmd.append(str(self.input_file))
        return cmd

    def run_compile(self, pandoc_cmd: List[str]):
        """Run pandoc command to generate tex/pdf output."""
        if self.custom_template_file is None:
            # Using built-in template.
            for resc in TEMPLATE_RESOURCES.get(self.builtin_template, ()):
                resc_path = self.cache_dir / resc
                if self.ignore_cache or not resc_path.exists():
                    resc_data = pkgutil.get_data("mdc", f"resources/{resc}")
                    if not resc_data:
                        raise AssertionError(
                            f"failed to load 'resources/{resc}: "
                            f"installation might be corrupt: try reinstalling"
                        )
                    with resc_path.open("wb") as _f1:
                        _f1.write(resc_data)

        if self.output_file is None:
            pdone = subprocess.run(pandoc_cmd, check=True, capture_output=True)
            pout = StringIO(pdone.stdout.decode())
            _fix_tables(pout)
            print(pout.getvalue())
        elif self.output_file.name.endswith(".tex"):
            pandoc_cmd.append(f"--output={self.output_file}")
            subprocess.run(pandoc_cmd, check=True)
            with open(self.output_file.name, "r+", encoding="utf-8") as _f2:
                _fix_tables(_f2)
        elif self.output_file.name.endswith(".pdf"):
            # Generate tex, then compile with latexmk
            tex_file_name = self.build_dir / "main.tex"

            pandoc_cmd.append(f"--output={tex_file_name}")
            subprocess.run(
                pandoc_cmd,
                check=True,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
            )
            with open(tex_file_name, "r+", encoding="utf-8") as _f3:
                _fix_tables(_f3)

            latexmk_cmd = [
                "latexmk",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-pdf",
                "-lualatex",
                f"-output-directory={self.build_dir}",
                f"{tex_file_name}",
            ]
            if not self.verbose:
                latexmk_cmd.append("-quiet")
            if self.rebuild:
                latexmk_cmd.append("-gg")
            subprocess.run(
                latexmk_cmd,
                check=True,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
            )

            shutil.copyfile(self.build_dir / "main.pdf", self.output_file.name)
        else:
            raise ValueError("output file extension must be .tex/.pdf")

    def __call__(self):
        """Entry point."""
        try:
            self.cache_dir.init()
            pandoc_cmd = self.build_pandoc_cmd()
            self.run_compile(pandoc_cmd)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        except OSError as e:
            print(
                f"ERROR: {e.filename}: {e.strerror} [code {e.errno}]", file=sys.stderr
            )
            return e.errno
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {e.cmd[0]} failed [code {e.returncode}]", file=sys.stderr)
            return e.returncode
        except KeyboardInterrupt:
            return -1
        return 0


def _fix_tables(latexf):
    """Modify a latex file to use regular 'table' instead of 'longtable'."""

    def _fix(match):
        match_str = match.group(1)

        # Capture caption to move to the end
        cap_match = re.search(r"(\\caption{.*})(\\tabularnewline)?", match_str)
        cap = ""
        if cap_match:
            cap_match_str, cap = cap_match.group(0), cap_match.group(1)
            match_str = match_str.replace(cap_match_str, "")
            cap += "\n"

        # Remove everything between '\endfirsthead' and '\endhead'
        match_str = re.sub(
            r"(\\endfirsthead.*?)?\\endhead", "", match_str, flags=re.DOTALL
        )

        return (
            "\\begin{table}\n"
            "\\centering\n"
            "\\begin{tabular}"
            f"{match_str}"
            "\\end{tabular}\n"
            f"{cap}"
            "\\end{table}"
        )

    latexs = latexf.read()
    fixed_latexs = re.sub(
        r"\\begin{longtable}(.*?)\\end{longtable}", _fix, latexs, flags=re.DOTALL
    )

    latexf.truncate(0)
    latexf.seek(0)
    print(fixed_latexs, file=latexf)


def main():
    arg_parser = ArgumentParser(formatter_class=CorgyHelpFormatter)
    arg_parser.add_argument("-V", "--version", action="version", version=__version__)
    _main = MDCMain.parse_from_cmdline(arg_parser)
    sys.exit(_main())
