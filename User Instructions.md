# MDMi Script Template

This script will look for all recently modified records and export the data to Excel. "Recently modified records" are records that have been modified after the date listed in the config file. After the script finishes running, the date in the config is updated to the current day.

## Configuration

The application can be configured to run on different databases and tables. Open the file `config.json` and edit the following fields, the fields bolded are more important. Make sure that whenever you edit this file you save it for changes to take effect.

1. `"MI" > "SERVICE LAYER URL"`
   - The URL of your Granta MI Service Layer. This is most likely `"http://[server name]/mi_servicelayer"`.
2. `"MI" > "VIEWER URL"`
   - The URL of your Granta MI Viewer. This is most likely `"http://[server name]/mi"`.
3. `"MI" > "AUTOLOGON"`
   - To connect to Granta MI with your Windows credentials, set this to `true`.
   - Otherwise, you must provide credentials in the fields below.
4. `"MI" > "USERNAME"`
   - The name of the Granta MI account used for authentication.
5. `"MI" > "_secure" > "PASSWORD"`
   - The password of the Granta MI account used for authentication.
   - This field can be written in plain text, when the script first runs it will encrypt the value for security.
6. `"MI" > "DOMAIN"`
   - Optional. Defaults to `null`.
   - The domain of the Granta MI account used for authentication.
7. `"MI" > "TIMEOUT"`
   - Optional. Defaults to `300000` (or 5 minutes.)
   - How long in milliseconds an individual request to Granta MI should stay alive before it is terminated.
8. `"SOURCE" > "DATABASE KEY"`
   - The database key that contains the table to report records from.
9. `"SOURCE" > "TABLE NAME"`
   - The name of the table to report records from.
10. `"LOG LEVEL"`
    - Optional. Defaults to `"INFO"`.
    - The level of logging to include in the log files.
    - Acceptable values: `"DEBUG"`, `"INFO"`, `"WARNING"`, `"CRITICAL"`, `"ERROR"`
11. `"SEARCH AFTER DATE"`
    - Optional. Defaults to `null`.
    - The application will report records created or modified after the specified date.
    - Date must be in `“yyyy-mm-dd”` format.
    - To report all data, set this value to `null`.

## Running

Double click on the file `run.bat` to run the application. CMD will open and log progress as the application runs. The application should take a few minutes to run and CMD will close once complete.

## Results

1. Microsoft Excel Reports
   - The recently modified records' identities and names will be reported in a Microsoft Excel file inside the `reports` folder. The file name contains the date and time the application was run.
   - Each row in the worksheet corresponds to one record.
2. Logs
   - Output logs as the application runs are stored in the `logs` folder.
   - Use these to identify and track down any issues that may arise while using the application.
