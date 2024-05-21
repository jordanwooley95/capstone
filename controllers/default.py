# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------


# ---- example index page ----
def index():
    import datetime

    # Fetch the top 3 most recent orders
    recent_orders = []
    orders = db().select(
        db.orders.ALL, db.customers.ALL,
        join=db.orders.on(db.orders.customer_id == db.customers.id),
        orderby=~db.orders.ordered_on,
        limitby=(0, 3)  # Limit to the top 3 recent orders
    )
    
    for order in orders:
        # Fetch the state name for the customer
        state = db(db.states.id == order.customers.state_id).select().first()
        state_name = state.state_name if state else 'N/A'

        # Calculate days ago
        current_datetime = datetime.datetime.now()
        order_datetime = order.orders.ordered_on
        days_ago = abs((current_datetime - order_datetime)).days

        # Prepare the order details
        order_details = {
            'id': order.orders.id,  # Directly access the id field of the orders table
            'name': f"{order.customers.first_name} {order.customers.last_name}",
            'state': state_name,
            'days_ago': days_ago
        }
        recent_orders.append(order_details)
    # Fetch the aggregate data
    sqlstmt = "SELECT SUM(o.quantity) as howmany, strain FROM orders o JOIN products p ON o.product_id = p.id GROUP BY strain"
    rows = db.executesql(sqlstmt, as_dict=True)

    return dict(recent_orders=recent_orders, rows=rows)



def about():
    return dict(message="About us")


def productz():
    return dict(message="Our products")


@auth.requires_login()
def cannalytics():
    return dict(message="Hello from Cannalytics!")


@auth.requires_login()
def dataadmin():
    return dict(message="Hello from Cannalytics!")


@auth.requires_login()
def brands():
    grid = SQLFORM.grid(db.brands)
    return dict(grid=grid)


@auth.requires_login()
def customers():
    grid = SQLFORM.grid(db.customers)
    return dict(grid=grid)


@auth.requires_login()
def events():
    grid = SQLFORM.grid(db.events)
    return dict(grid=grid)


@auth.requires_login()
def states():
    grid = SQLFORM.grid(db.states)
    return dict(grid=grid)


@auth.requires_login()
def products():
    grid = SQLFORM.grid(db.products)
    return dict(grid=grid)


@auth.requires_login()
def orders():
    grid = SQLFORM.grid(db.orders)
    return dict(grid=grid)


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == "GET":
        raise HTTP(403)
    return response.json({"status": "success", "email": auth.user.email})


# ---- Smart Grid (example) -----
@auth.requires_membership("admin")  # can only be accessed by members of admin groupd
def grid():
    response.view = "generic.html"  # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables:
        raise HTTP(403)
    grid = SQLFORM.smartgrid(
        db[tablename], args=[tablename], deletable=False, editable=False
    )
    return dict(grid=grid)


# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu()  # add the wiki to the menu
    return auth.wiki()


# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
