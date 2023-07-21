# Refactoring Steps

- Test existing script and fix if broken
- Ensure requirements.txt is correct
- Rename main file to main.py
- Convert to snake_case
- Autoformat
	- Black for Python files
	- JSON files if necessary
- Use project_functions.py from script template
	- Copy file over without losing functionality from original project_functions.py
	- Remove extraneous functionality
		- Unused functions
		- References to the Streamlined API if the script only uses Foundation
		- Etc.
	- Remove redundant functionality from main.py
		- Config
		- Local session instances
		- Etc.
	- Change logger name
	- Update .gitignore if necessary
- General cleanup
	- Add whitespace for readability
	- Remove unused imports and variables
	- Delete commented-out code
	- Change variable and function names
	- Add typehints
	- Add/edit docstrings
	- Replace string concatenation and `.format()` calls with f-strings
	- Replace constructors with literals where possible
- Split up big files
- Logging
	- `print` statements
		- Replace with logging
		- Remove where not needed
	- Clean up existing logging if necessary
	- Add additional logging where appropriate
- Update logic and control flow
	- Fix any bugs
	- Simplify logic where possible
	- Split up big functions
	- Replace `if` statements with guard clauses where possible
	- Convert loops to comprehensions wherever ChatGPT decrees
- Add comments for readability
- Extra development
	- Resolve any TODO comments
	- Add additional functionality if appropriate
- Update this checklist if anything else came up