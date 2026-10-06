"""Check the deliberate ordering failure and the corrected notebook.

Run from any directory with nbformat, nbclient and ipykernel installed.
Each execution uses a fresh kernel from this Python environment.
"""

from pathlib import Path
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from jupyter_client import KernelManager

EXPECTED_OUTPUT = "Mean gap above target: 12.0 percentage points\n"


def client_for(name, working_directory):
    notebook = nbformat.read(Path(__file__).parent / name, as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [
        sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"
    ]
    return NotebookClient(
        notebook, km=manager, timeout=30,
        resources={"metadata": {"path": working_directory}},
    )


def check_result(notebook, cell_id):
    result = next(cell for cell in notebook.cells if cell.id == cell_id)
    output = "".join(
        item.text for item in result.outputs if item.output_type == "stream"
    )
    if output != EXPECTED_OUTPUT:
        raise RuntimeError(f"Unexpected result: {output!r}")


def main():
    # Recreate the misleading output in a real kernel, not from saved outputs.
    with tempfile.TemporaryDirectory() as directory:
        reordered = client_for("out-of-order.ipynb", directory)
        code_cells = {
            cell.id: (index, cell)
            for index, cell in enumerate(reordered.nb.cells)
            if cell.cell_type == "code"
        }
        with reordered.setup_kernel(cleanup_kc=True):
            for count, cell_id in enumerate(("data", "target", "calculation"), 1):
                index, cell = code_cells[cell_id]
                reordered.execute_cell(cell, index, execution_count=count)
        check_result(reordered.nb, "calculation")
        print("PASS: running A, C, B reproduces the displayed mean gap of 12.0 percentage points.")

    # Empty working directories avoid relying on files beside the notebooks.
    with tempfile.TemporaryDirectory() as directory:
        broken = client_for("out-of-order.ipynb", directory)
        try:
            broken.execute(cleanup_kc=True)
        except CellExecutionError:
            errors = [
                (cell.id, output)
                for cell in broken.nb.cells if cell.cell_type == "code"
                for output in cell.outputs if output.output_type == "error"
            ]
            if not (
                len(errors) == 1
                and errors[0][0] == "calculation"
                and errors[0][1].ename == "NameError"
                and errors[0][1].evalue == "name 'target_rate' is not defined"
            ):
                raise
            print("PASS: out-of-order notebook fails on undefined target_rate.")
        else:
            raise RuntimeError("Teaching example unexpectedly passed a clean run.")

    with tempfile.TemporaryDirectory() as directory:
        fixed = client_for("reproducible.ipynb", directory)
        fixed.execute(cleanup_kc=True)
        check_result(fixed.nb, "result")
        print("PASS: corrected notebook executes cleanly and returns a mean gap of 12.0 percentage points.")


if __name__ == "__main__":
    main()
