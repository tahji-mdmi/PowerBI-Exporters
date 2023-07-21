import json
import time
from datetime import datetime
from pathlib import Path

import project_functions as pf
import reporter
from GRANTA_MIScriptingToolkit import granta
from project_functions import MI_DATETIME_FORMAT, UTC


def main() -> None:
    """ """
    pf.start()
    try:
        db_key: str = pf.args.db_key or pf.config["SOURCE"]["DATABASE KEY"]
        table_name: str = pf.args.table_name or pf.config["SOURCE"]["TABLE NAME"]
        search_after_datetime: str | None = (
            pf.args.search_after_datetime or pf.config.get("SEARCH AFTER DATETIME")
        )

        current_datetime = datetime.now(tz=UTC).strftime(MI_DATETIME_FORMAT)

        db = pf.session.get_db(db_key=db_key)
        table = db.get_table(table_name)

        records = get_records(table, search_after_datetime, current_datetime)
        table.bulk_fetch(records=records, attributes=None)

        reports_folder_path = Path(
            pf.config["OUTPUT FOLDER"] or (pf.parent_directory / "reports")
        )
        reporter.report_recently_modified_records(reports_folder_path, records)

        update_config_search_after_datetime(current_datetime)

        pf.logger.info("Done!")
    except Exception as ex:
        pf.logger.exception(ex)
    time.sleep(5)
    return


def get_records(
    table: granta.Table,
    search_start_datetime: str | None,
    search_end_datetime: str | None,
) -> list[granta.Record]:
    if search_start_datetime and search_end_datetime:
        pf.logger.info(
            f"Getting records modified between {search_start_datetime}"
            + f" and {search_end_datetime}"
        )
        return get_recently_modified_records(
            table, search_start_datetime, search_end_datetime
        )
    pf.logger.info("Getting all records")
    return table.all_records()


def get_recently_modified_records(
    table: granta.Table,
    minimum_date: str,
    maximum_date: str,
) -> list[granta.Record]:
    modified_criterion = granta.SearchCriterion(
        granta.PseudoAttributeDefinition("modifiedDate"),
        "BETWEEN",
        (minimum_date, maximum_date),
    )
    modified_records = table.search_for_records_where([modified_criterion])
    return modified_records


def update_config_search_after_datetime(new_datetime: str) -> None:
    with open(pf.config_file_path, "r") as f:
        contents = json.load(f)

    contents["SEARCH AFTER DATETIME"] = new_datetime

    with open(pf.config_file_path, "w") as f:
        json.dump(contents, f, indent="\t")

    pf.logger.info(
        "Next time this script runs, it will look for"
        + f" records modified after {new_datetime}!"
    )
    return


if __name__ == "__main__":
    main()
