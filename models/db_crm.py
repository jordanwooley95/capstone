# -*- coding: utf-8 -*-
import os
db.define_table(
    "states",
    Field("state_name", notnull=True),
    format="%(state_name)s",
)


#with open(os.path.join(request.folder, 'private', 'states.csv'), 'rt') as f:
    #db.states.import_from_csv_file(f)

#db.commit()

db.define_table(
    "companies",
    Field("company_name", notnull=True),
    Field("city", notnull=True),
    Field("state_name", "reference states", notnull=True),
    Field("zip_code"),
    Field("industry"),
    Field("website", requires=IS_URL()),
    Field("linkedin", requires=IS_URL()),
    Field("phone_number", requires=IS_MATCH("[\d\-\(\) ]+")),
    format="%(company_name)s",
)

db.define_table(
    "persons",
    Field("company_id", "reference companies"),
    Field("first_name", notnull=True),
    Field("last_name", notnull=True),
    Field("title"),
    Field("work_phone", requires=IS_MATCH("[\d\-\(\) ]+")),
    Field("cell_phone", requires=IS_MATCH("[\d\-\(\) ]+")),
    Field("email", requires=IS_EMAIL()),
    Field("birthday", requires=IS_DATE(format=T("%Y-%m-%d"))),
    Field("person_type", requires=IS_IN_SET(["Customer", "Vendor"])),
    Field("comments", "text"),
    Field("created_by", "reference auth_user", default=auth.user_id),
    Field("created_on", "datetime", default=request.now),
    format="%(last_name)s, %(first_name)s",
)

db.define_table(
    "events",
    Field("user_id", "reference auth_user"),
    Field("person_id","reference persons",),
    Field("comm_type", requires=IS_IN_SET(["Phone", "Email", "In person"])),
    Field("event_datetime", "datetime", requires=IS_DATETIME()),
    Field("status", requires=IS_IN_SET(["Open", "Closed", "Canceled"])),
    Field(
        "event_type",
        requires=IS_IN_SET(
            ["Meeting", "Call", "Email", "Lunch", "Dinner", "Breakfast", "Other"]
        ),
    ),
    Field("comments", "text"),
    format="%(event_type)s",
)
