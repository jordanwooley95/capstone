# -*- coding: utf-8 -*-
import os

db.define_table(
    "states",
    Field("state_name", notnull=True),
    format="%(state_name)s",
)
################################################################################
# leave this commented out, uncomment and run once to populate the states table

# with open(os.path.join(request.folder, 'private', 'states.csv'), 'rt') as f:
# db.states.import_from_csv_file(f)
################################################################################

db.commit()

db.define_table(
    "brands",
    Field("brand_name", notnull=True),
    Field("city", notnull=True),
    Field("state_name", "reference states", notnull=True),
    Field("zip_code"),
    Field("website", requires=IS_URL()),
    Field("linkedin", requires=IS_URL()),
    Field("phone_number", requires=IS_MATCH("[\d\-\(\) ]+")),
    format="%(brand_name)s",
)

db.define_table(
    "customers",
    Field("company_id", "reference brands"),
    Field("first_name", notnull=True),
    Field("last_name", notnull=True),
    Field("city", notnull=True),
    Field("state_name", "reference states", notnull=True),
    Field("zip_code"),
    Field("phone_number", requires=IS_MATCH("[\d\-\(\) ]+")),
    Field("email", requires=IS_EMAIL()),
    Field("birthday", requires=IS_DATE(format=T("%Y-%m-%d"))),
    Field("comments", "text"),
    Field("created_by", "reference auth_user", default=auth.user_id),
    Field("created_on", "datetime", default=request.now),
    format="%(last_name)s, %(first_name)s",
)

db.define_table(
    "events",
    Field("user_id", "reference auth_user"),
    Field(
        "person_id",
        "reference customers",
    ),
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

db.define_table(
    "products",
    Field("product_name", notnull=True),
    Field(
        "category",
        requires=IS_IN_SET(
            ["Flower", "Edible", "Concentrate", "Pre-roll", "Topical", "Accessory"]
        ),
    ),
    Field("strain", requires=IS_IN_SET(["Indica", "Sativa", "Hybrid"])),
    Field("description", "text"),
    Field(
        "thc_content", "double", requires=IS_FLOAT_IN_RANGE(0, 100)# THC content in percentage
    ),  
    Field(
        "cbd_content", "double", requires=IS_FLOAT_IN_RANGE(0, 100)# CBD content in percentage
    ),  
    Field("price", "double", requires=IS_FLOAT_IN_RANGE(0)),  # Price per unit
    Field("stock_quantity", "integer", default=0),  # Current stock quantity
    Field("created_by", "reference auth_user", default=auth.user_id),
    Field("created_on", "datetime", default=request.now),
    format="%(product_name)s",
)

db.define_table(
    "orders",
    Field("customer_id", "reference customers"),
    Field("product_id", "reference products"),
    Field("quantity", "integer", notnull=True),
    Field("ordered_on", "datetime", default=request.now),
)
