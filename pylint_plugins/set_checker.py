import os

import astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker


IGNORED_FILES = set(
    map(
        os.path.abspath,
        [
            ##### Instructions #####
            # 1. Select the file you would like to work on.
            # 2. Remove the file from the list.
            # 3. Run `pylint <the file>`.
            # 4. Fix lint errors.
            # 5. File a PR.
            "tests/lightgbm/test_lightgbm_autolog.py",
            "tests/models/test_model_input_examples.py",
            "tests/projects/test_project_spec.py",
            "tests/pyfunc/test_model_export_with_loader_module_and_data_path.py",
            "tests/store/artifact/test_databricks_artifact_repo.py",
            "tests/store/artifact/test_ftp_artifact_repo.py",
            "tests/tensorflow/test_tensorflow2_autolog.py",
            "tests/utils/test_requirements_utils.py",
            "tests/xgboost/test_xgboost_autolog.py",
        ],
    )
)


class SetChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = "set-checker"
    USE_SET_LITERAL = "use-set-literal"
    msgs = {
        "W0005": (
            "Use set literal (e.g. `{'a', 'b'}`) instead of applying `set()` on list or "
            "tuple literal (e.g. `set(['a', 'b'])`)",
            USE_SET_LITERAL,
            "Use set literal",
        ),
    }
    priority = -1

    def visit_call(self, node: astroid.Call):
        if node.root().file in IGNORED_FILES:
            return
        if (
            node.func.as_string() == "set"
            and node.args
            and isinstance(node.args[0], (astroid.List, astroid.Tuple))
        ):
            self.add_message(SetChecker.USE_SET_LITERAL, node=node)
