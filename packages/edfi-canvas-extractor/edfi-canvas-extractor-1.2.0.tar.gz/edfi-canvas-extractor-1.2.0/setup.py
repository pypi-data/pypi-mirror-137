# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edfi_canvas_extractor',
 'edfi_canvas_extractor.api',
 'edfi_canvas_extractor.helpers',
 'edfi_canvas_extractor.mapping']

package_data = \
{'': ['*']}

install_requires = \
['ConfigArgParse>=1.2.3,<2.0.0',
 'SQLAlchemy>=1.3.20,<2.0.0',
 'canvasapi==2.2.0',
 'edfi-lms-extractor-lib>=1.1.0,<2.0.0',
 'edfi-lms-file-utils>=1.0.0,<2.0.0',
 'errorhandler>=2.0.1,<3.0.0',
 'opnieuw>=1.1.0,<2.0.0',
 'pandas>=1.1.2,<2.0.0',
 'python-dotenv==0.15.0',
 'requests>=2.24.0,<3.0.0',
 'xxhash>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'edfi-canvas-extractor',
    'version': '1.2.0',
    'description': 'Extract tool for retrieving student data from Canvas',
    'long_description': '# Canvas Extractor\n\nThis tool retrieves and writes out to CSV students, active sections,\nassignments, and submissions by querying the Canvas API. For more information on\nthe this tool and its output files, please see the main repository\n[readme](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit).\n\n## Getting Started\n\n1. Download the latest code from [the project\n   homepage](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit) by clicking on\n   the green "CODE" button and choosing an appropriate option. If choosing the\n   Zip option, extract the file contents using your favorite zip tool.\n1. Open a command prompt\\* and change to this file\'s directory (* e.g. cmd.exe,\n   PowerShell, bash).\n1. Ensure you have [Python 3.9+ and Poetry](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit#getting-started).\n1. At a command prompt, install all required dependencies:\n\n   ```bash\n   poetry install\n   ```\n\n1. Optional: make a copy of the `.env.example` file, named simply `.env`, and\n   customize the settings as described in the Configuration section below.\n1. Create an access token by signing into your Canvas instance. Go to Account >\n   Settings, then scroll down to the "Approved Integrations" section and click\n   the "New Access Token" button. If using a `.env` file, then copy the token\n   into this file.\n1. Run the extractor one of two ways:\n   * Execute the extractor with minimum command line arguments:\n\n      ```bash\n      poetry run python edfi_canvas_extractor -b [canvas url] -a [api token]\n          -s [start date range] -e [end date range] -f assignments\n      ```\n\n   * Alternately, run with environment variables or `.env` file:\n\n     ```bash\n     poetry run python edfi_canvas_extractor\n     ```\n\n   * For detailed help, execute `poetry run python edfi_canvas_extractor -h`.\n\n## Configuration\n\nApplication configuration is provided through environment variables or command\nline interface (CLI) arguments. CLI arguments take precedence over environment\nvariables. Environment variables can be set the normal way, or by using a\ndedicated [`.env` file](https://pypi.org/project/python-dotenv/) like\n\n```none\nCANVAS_BASE_URL=[CANVAS_BASE_URL]\nCANVAS_ACCESS_TOKEN=[CANVAS_ACCESS_TOKEN]\nSTART_DATE=[CLASS_START_DATE]\nEND_DATE=[CLASS_END_DATE]\nOUTPUT_DIRECTORY=data\n```\n\nSupported parameters:\n\n| Description | Required | Command Line Argument | Environment Variable |\n| ----------- | -------- | --------------------- | -------------------- |\n| Base Canvas URL | yes | `-b` or `--base-url` | CANVAS_BASE_URL |\n| Canvas API access token | yes | `-a` or `--access-token` | CANVAS_ACCESS_TOKEN |\n| Output Directory | no (default: [working directory]/data) | `-o` or `--output-directory` | OUTPUT_DIRECTORY |\n| Sync database directory | no (default: [working directory]/data) | `-d` or `--sync-database-directory` | SYNC_DATABASE_DIRECTORY |\n| Start date*, yyyy-mm-dd format | yes | `-s` or `--start_date` | START_DATE |\n| End date*, yyyy-mm-dd format | yes | `-e` or `--end_date` | END_DATE |\n| Log level** | no (default: INFO) | `-l` or `--log-level` | LOG_LEVEL |\n| Feature*** | no (default: core, not removable) | `-f` or `--feature` | FEATURE |\n\n\\* _Start Date_ and _End Date_ are used in pulling course and system activity\ndata and would typically span a semester or equivalent school calendar timespan.\n\n\\** Valid values for the optional _log level_:\n\n* DEBUG\n* INFO(default)\n* WARNING\n* ERROR\n* CRITICAL\n\n\\*** When there\'s no specified feature, the extractor will always process Users,\nSections, and Section Associations, which are considered the core feature. Other\nfeatures (can combine two or more):\n\n* assignments (Enables the extraction of assignments and submissions)\n* activities (Enables the extraction of section activities and system\n  activities) - **EXPERIMENTAL**, subject to breaking changes\n* grades (Enables the extraction of grades) - **EXPERIMENTAL**, subject to\n  breaking changes\n\nWhen setting features via `.env` file or through environment variable, combine\nfeatures by using a bracketed comma-separate list, e.g. `FEATURE=[activities,\nattendance, assignments, grades]`. To combine features at the command line,\nsimply list them together: `--feature activities, attendance, assignments,\ngrades`.\n\n### Output\n\nCSV files in the data(or the specified output) directory with the [LMS Unifying\nData\nModel](https://techdocs.ed-fi.org/display/EDFITOOLS/LMS+Unifying+Data+Model)\nformat.\n\n### Logging and Exit Codes\n\nLog statements are written to the standard output. If you wish to capture log\ndetails, then be sure to redirect the output to a file. For example:\n\n```bash\npoetry run python edfi_canvas_extractor > 2020-12-07-15-43.log\n```\n\nIf any errors occurred during the script run, then there will be a final print\nmessage to the standard error handler as an additional mechanism for calling\nattention to the error: `"A fatal error occurred, please review the log output\nfor more information."`\n\nThe application will exit with status code `1` if there were any log messages at\nthe ERROR or CRITICAL level, otherwise it will exit with status code `0`.\n\n## Developer Operations\n\n1. Style check: `poetry run flake8`\n1. Static typing check: `poetry run mypy .`\n1. Run unit tests: `poetry run pytest`\n1. Run unit tests with code coverage: `poetry run coverage run -m pytest`\n1. View code coverage: `poetry run coverage report`\n\n_Also see\n[build.py](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/docs/build.md)_ for\nuse of the build script.\n\n### Visual Studio Code (Optional)\n\nTo work in Visual Studio Code install the Python Extension.\nThen type `Ctrl-Shift-P`, then choose `Python:Select Interpreter`,\nthen choose the environment that includes `.venv` in the name.\n\n## Legal Information\n\nCopyright (c) 2022 Ed-Fi Alliance, LLC and contributors.\n\nLicensed under the [Apache License, Version\n2.0](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/LICENSE) (the\n"License").\n\nUnless required by applicable law or agreed to in writing, software distributed\nunder the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR\nCONDITIONS OF ANY KIND, either express or implied. See the License for the\nspecific language governing permissions and limitations under the License.\n\nSee [NOTICES](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/NOTICES.md) for\nadditional copyright and license notifications.\n',
    'author': 'Ed-Fi Alliance, LLC, and contributors',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://techdocs.ed-fi.org/display/EDFITOOLS/LMS+Toolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
