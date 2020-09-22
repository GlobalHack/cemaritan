# functions for actually making the database calls
from typing import Any, List, Tuple

from library.models import Connection, Mapping, Organization, Transfer, User, History, Download, Frequency, Upload
from library.utils import get_future_datetime_formatted, get_now_datetime_formatted

### Generic functions
def get_rows_by_organization(
    table_name: str, connection, organization_id: int, query: str = None
) -> List[Tuple[Tuple[str, Any]]]:
    """Returns list of tuples where each tuple is a row in the database
    
    Parameters
    ----------
    table_name : 
        Name of table in DB
    connection
        Connection to DB
    organization_id
        Id of Organization
    
    Returns
    -------
    List[Tuple[Tuple[str, Any]]]
        List of Tuples of 2-tuples representing each row of the response of the query
        Example: 
        [
            (
                ("uid", 1),
                ("organization", 1),
                ("name", "SF"),
                ("created_datetime", "2019-03-09 20:42:03"),
                ("created_by", 1),
                ("type", "A"),
                ("connection_info", "{conn string}")
            ),
            (
                ("uid", 2),
                ("organization", 1),
                ("name", "CW"),
                ("created_datetime", "2019-03-10 04:42:03"),
                ("created_by", 1),
                ("type", "B"),
                ("connection_info", "{conn string}")
            )
        ]

    """
    if query is None:
        query = f"select * from {table_name} where {table_name}.organization = {organization_id}"
    r = connection.query(query)
    return r


def get_row_by_object_id(
    table_name: str, connection, organization_id: int, object_id: int, query: str = None
) -> Tuple[Tuple[str, Any]]:
    """Returns a tuple of tuples representing a single row in the database
    corresponding to ``organization_id`` and ``object_id``.
    
    Parameters
    ----------
    table_name : 
        Name of table in DB
    connection
        Connection to DB
    organization_id
        Id of Organization
    object_id
        uid of object to return, if exists
    
    Returns
    -------
    Tuple[Tuple[str, Any]]
        Tuple of 2-tuples representing a row of ``table_name`` matching ``organization_id``
        and ``object_id``
        Example: 
        (
            ("uid", 1),
            ("organization", 1),
            ("name", "SF"),
            ("created_datetime", "2019-03-09 20:42:03"),
            ("created_by", 1),
            ("type", "A"),
            ("connection_info", "{conn string}")
        )

    """
    try:
        if query is None:
            query = f"select * from {table_name} where {table_name}.organization = {organization_id} and {table_name}.uid = {object_id}"
        r = connection.query(query)
        return r[0]  # return only first element if possible
    except IndexError:
        return None


def delete_row_by_uid(connection, table_name: str, uid: int):
    """Delete row in ``table_name`` by ``uid``
    
    Parameters
    ----------
    connection
        Connection to database
    table_name : str
        Name of table
    uid : int
        uid of row to delete
    
    Returns
    -------
    bool
        Indicating success or failure of deletion
    """

    try:
        query = f"DELETE from {table_name} where {table_name}.uid={uid}"
        connection.query(query, null_return=True)
    except:
        return False
    return True


# Collections
def get_connections(connection, organization_id: int):
    """Get connections for ``organization_id``
    
    Parameters
    ----------
    connection
        Connection to database
    organization_id : int
        Organization Id
    
    Returns
    -------
    List[models.Connection]
        List of Connection objects

    """

    connections = get_rows_by_organization(
        table_name="connections", connection=connection, organization_id=organization_id
    )
    return [Connection(tup) for tup in connections]


def get_connection(connection, organization_id: int, connection_id: int):
    """Get connection matching ``organization_id`` and ``connection_id``
    
    Parameters
    ----------
    connection : 
        Connection to database
    organization_id : int
        Organization Id
    connection_id : int
        Connection Id
    
    Returns
    -------
    Tuple[Tuple[str, Any]]
        Tuple of 2-tuples representing a row of `connections` table matching ``organization_id``
        and ``connection_id``
    """

    row = get_row_by_object_id(
        table_name="connections",
        connection=connection,
        organization_id=organization_id,
        object_id=connection_id,
    )
    if row is not None:
        return Connection(row)
    else:
        return None  # Unnecessary but good to be explicit


# Histories
def get_histories(connection, organization_id: int):
    """Get histories for ``organization_id``
    
    Parameters
    ----------
    connection
        Connection to database
    organization_id : int
        Organization Id
    
    Returns
    -------
    List[models.History]
        List of History objects

    """

    orgs = get_rows_by_organization(
        table_name="histories", connection=connection, organization_id=organization_id
    )
    return [History(tup) for tup in orgs]


def get_history(connection, organization_id: int, history_id: int):
    """Get history matching ``organization_id`` and ``history_id``
    
    Parameters
    ----------
    connection : 
        Connection to database
    organization_id : int
        Organization Id
    history_id : int
        history Id
    
    Returns
    -------
    Tuple[Tuple[str, Any]]
        Tuple of 2-tuples representing a row of `histories` table matching ``organization_id``
        and ``history_id``
        Example: 
        (
            ("uid", 2),
            ("type", "Transfer"),
            ("action", None),
            ("datetime", "2019-03-20 20:42:03"),
            ("name", None),
            ("details", None),
            ("source_uid", 0),
            ("organization", 1)
        )
        
    """

    row = get_row_by_object_id(
        table_name="histories",
        connection=connection,
        organization_id=organization_id,
        object_id=history_id,
    )
    if row is not None:
        return History(row)
    else:
        return None  # Unnecessary but good to be explicit


def create_history(connection, organization_id, history):
    """Create a history record."""
    history_dict = history.to_dict()
    type_ = history_dict["type"]
    action = history_dict["action"]
    name = history_dict["name"]
    datetime = history_dict["datetime"]
    details = history_dict["details"]
    source_uid = history_dict["source_uid"]
    organization_id = history_dict["organization"]
    query = f"INSERT INTO histories (organization, type, action,  datetime, name, details, source_uid) VALUES ('{organization_id}', '{type_}', '{action}', '{datetime}', '{name}', '{details}', '{source_uid}') \n RETURNING uid;"
    return connection.query(query)



# transfers
def get_transfers(connection, organization_id: int):
    """Get transfers for ``organization_id``
    
    Parameters
    ----------
    connection
        Connection to database
    organization_id : int
        Organization Id
    
    Returns
    -------
    List[models.Transfer]
        List of Transfer objects

    """
    QUERY = f"""select 
                    t6.uid,
                    t6.name,
                    t6.organization2 as organization,
                    t6.created_datetime as created_datetime,
                    t6.source2 as source,
                    t6.source_uid as source_uid,
                    t6.source_mapping2 as source_mapping,
                    t6.source_mapping_uid as source_uid,
                    t6.destination2 as destination,
                    t6.destination_uid as destination_uid,
                    t6.destination_mapping2 as destination_mapping,
                    t6.destination_mapping_uid as destination_mapping_uid,
                    CASE WHEN t6.active = 1 THEN 'TRUE' ELSE 'FALSE' END active,
                    t6.start_datetime as start_datetime,
                    t6.frequency as frequency
                    from 
                    (select t5.*, d2.name as destination_mapping2, d2.uid as destination_mapping_uid from
                    (select t4.*, d.name as source_mapping2, d.uid as source_mapping_uid from 
                    (Select t3.*, c2.name as destination2, c2.uid as destination_uid from
                    (select t2.*, c.name as source2, c.uid as source_uid from
                    (select t.*, o.name as organization2, t.uid as transfer_uid from
                    (select * from transfers where transfers.organization = {organization_id}) as t
                    LEFT JOIN 
                    organizations as o
                    on o.uid = t.organization) as t2
                    LEFT join
                    connections as c
                    on t2.source=c.uid) as t3
                    left join
                    connections as c2
                    on t3.destination=c2.uid) as t4
                    left join
                    mappings as d
                    on t4.source_mapping=d.uid) as t5
                    left join
                    mappings as d2
                    on t5.destination_mapping=d2.uid) as t6"""
    transfers = get_rows_by_organization(
        table_name="transfers",
        connection=connection,
        organization_id=organization_id,
        query=QUERY,
    )
    return [Transfer(tup) for tup in transfers]


def get_transfer(connection, organization_id: int, transfer_id: int):
    """Get transfer matching ``organization_id`` and ``transfer_id``
    
    Parameters
    ----------
    connection : 
        Connection to database
    organization_id : int
        Organization Id
    transfer_id : int
        transfer Id
    
    Returns
    -------
    Tuple[Tuple[str, Any]]
        Tuple of 2-tuples representing a row of `transfers` table matching ``organization_id``
        and ``transfer_id``
        Example: 
        (
            ("uid", 1),
            ("name", "CW to SF"),
            ("created_datetime", "2019-03-20 20:42:03"),
            ("created_by", 1),
            ("organization", 1),
            ("source", 2),
            ("source_mapping", 2),
            ("destination", 1),
            ("destination_mapping", 1),
            ("start_datetime", "2019-03-13 20:42:03"),
            ("frequency", "1 day"),
            ("record_filter", "filter a"),
            ("active", 1)
        )
         
    """
    QUERY = f"""select 
                    t6.uid,
                    t6.name,
                    t6.organization2 as organization,
                    t6.created_datetime as created_datetime,
                    t6.source2 as source,
                    t6.source_uid as source_uid,
                    t6.source_mapping2 as source_mapping,
                    t6.source_mapping_uid as source_mapping_uid,
                    t6.destination2 as destination,
                    t6.destination_uid as destination_uid,
                    t6.destination_mapping2 as destination_mapping,
                    t6.destination_mapping_uid as destination_mapping_uid,
                    CASE WHEN t6.active = 1 THEN 'TRUE' ELSE 'FALSE' END active,
                    t6.start_datetime as start_datetime,
                    t6.frequency as frequency
                    from 
                    (select t5.*, d2.name as destination_mapping2, d2.uid as destination_mapping_uid from
                    (select t4.*, d.name as source_mapping2, d.uid as source_mapping_uid from 
                    (Select t3.*, c2.name as destination2, c2.uid as destination_uid from
                    (select t2.*, c.name as source2, c.uid as source_uid from
                    (select t.*, o.name as organization2, t.uid as transfer_uid from
                    (select * from transfers where transfers.organization = {organization_id} and transfers.uid = {transfer_id}) as t
                    LEFT JOIN 
                    organizations as o
                    on o.uid = t.organization) as t2
                    LEFT join
                    connections as c
                    on t2.source=c.uid) as t3
                    left join
                    connections as c2
                    on t3.destination=c2.uid) as t4
                    left join
                    mappings as d
                    on t4.source_mapping=d.uid) as t5
                    left join
                    mappings as d2
                    on t5.destination_mapping=d2.uid) as t6"""
    row = get_row_by_object_id(
        table_name="transfers",
        connection=connection,
        organization_id=organization_id,
        object_id=transfer_id,
        query=QUERY,
    )
    if row is not None:
        return Transfer(row)
    else:
        return None  # Unnecessary but good to be explicit


def create_transfer(
    connection, organization_id: int, transfer
):
    """Create transfer in database
    
    Parameters
    ----------
    connection
        Connection to database
    transfer
        models.Transfer
    """
    model_as_dict = transfer.to_dict()
    created_datetime = "2019-03-20 20:42:03"  # temporary
    name = model_as_dict['name']
    created_by = model_as_dict['created_by']
    source = model_as_dict['source_uid']
    source_mapping = model_as_dict['source_mapping_uid']
    destination = model_as_dict['destination_uid']
    destination_mapping = model_as_dict['destination_mapping_uid']
    start_datetime = model_as_dict['start_datetime']
    frequency = model_as_dict['frequency']
    active = 1 if model_as_dict['active'] else 0
    query = f"INSERT INTO transfers (organization, name, created_datetime, created_by, source, source_mapping, destination, destination_mapping, start_datetime, frequency, active) VALUES ('{organization_id}', '{name}', '{created_datetime}', '{created_by}', '{source}', '{source_mapping}', '{destination}', '{destination_mapping}', '{start_datetime}', '{frequency}', '{active}') \n RETURNING uid;"
    return connection.query(query)


def update_transfer(connection, organization_id: int, transfer_id:int, transfer: Transfer):
    """Update a Transfer in the database."""
    
    d = transfer.to_dict()
    name = d['name']
    source_uid = d['source_uid']
    source_mapping_uid = d['source_mapping_uid']
    destination_uid = d['destination_uid']
    destination_mapping_uid = d['destination_mapping_uid']
    start_datetime = d['start_datetime']
    frequency = d['frequency']
    #record_filter = d['record_filter']
    active = 1 if d['active'] else 0

    query = f"""Update transfers
            Set name='{name}',
                source='{source_uid}',
                source_mapping='{source_mapping_uid}',
                destination='{destination_uid}',
                destination_mapping='{destination_mapping_uid}',
                start_datetime='{start_datetime}',
                frequency='{frequency}',
                
                active='{active}'
            Where organization='{organization_id}' and uid='{transfer_id}' 
            returning uid
            """
    result = connection.query(query)
    if result is None:
        raise ValueError('Something went wrong with update_transfer query.')
    return True


def get_frequencies_list(connection):
    """Get static list of frequencies."""
    query = "Select name, value from list_frequencies"
    frequencies = connection.query(query)
    return [Frequency(tup) for tup in frequencies]


# Users
def get_user_by_auth_id(connection, auth_id: str, auth_service: str=None):
    """Get the Cemaritan ID for the auth service ID."""
    if auth_service is None:
        auth_service = 'firebase'
    query = f"Select cemaritan_id from auth where firebase_id='{auth_id}' and auth_service='{auth_service}'"
    users = connection.query(query)
    return User({'uid': users[0][0][1]})


def get_user_by_uid(connection, user_uid):
    """Get all user info by Cemaritan id."""
    query = f"Select * from users where uid='{user_uid}'"
    users = connection.query(query)
    return User(users[0])


# def get_users(connection, organization_id: int):
#     """Get users for ``organization_id``
    
#     Parameters
#     ----------
#     connection
#         Connection to database
#     organization_id : int
#         Organization Id
    
#     Returns
#     -------
#     List[models.User]
#         List of User objects

#     """
#     users = get_rows_by_organization(
#         table_name="users", connection=connection, organization_id=organization_id
#     )
#     return [User(tup) for tup in users]


# def get_user(connection, organization_id: int, user_id: int):
#     """Get user matching ``organization_id`` and ``user_id``
    
#     Parameters
#     ----------
#     connection : 
#         Connection to database
#     organization_id : int
#         Organization Id
#     user_id : int
#         user Id
    
#     Returns
#     -------
#     Tuple[Tuple[str, Any]]
#         Tuple of 2-tuples representing a row of `users` table matching ``organization_id``
#         and ``user_id``
#         Example: 
#         (
#             ("uid", 1),
#             ("name", "Matt"),
#             ("created_datetime", "2019-03-10 10:42:03"),
#             ("organization", 1)
#         )
        
#     """

#     row = get_row_by_object_id(
#         table_name="users",
#         connection=connection,
#         organization_id=organization_id,
#         object_id=user_id,
#     )
#     if row is not None:
#         return User(row)
#     else:
#         return None  # Unnecessary but good to be explicit


# Downloads
def get_downloads(connection, organization_id: int):
    """Get downloads for ``organization_id``
    
    Parameters
    ----------
    connection
        Connection to database
    organization_id : int
        Organization Id
    
    Returns
    -------
    List[models.Download]
        List of Download objects

    """
    downloads = get_rows_by_organization(
        table_name="downloads", connection=connection, organization_id=organization_id
    )
    return [Download(tup) for tup in downloads]


def get_download(connection, organization_id: int, download_id: int):
    """Get download matching ``organization_id`` and ``download_id``
    
    Parameters
    ----------
    connection : 
        Connection to database
    organization_id : int
        Organization Id
    download_id : int
        Download Id
    
    Returns
    -------
    Tuple[Tuple[str, Any]]
        Tuple of 2-tuples representing a row of `users` table matching ``organization_id``
        and ``user_id``
        Example: 
        (
            ("uid", 1),
            ("name", "Some download"),
            ("expirationdatetime", "2019-03-10 10:42:03"),
            ("transfername", "some transfer name"),
            ("historyuid", 1),
            ("organization", 1)
        )
        
    """

    row = get_row_by_object_id(
        table_name="downloads",
        connection=connection,
        organization_id=organization_id,
        object_id=download_id,
    )
    if row is not None:
        return Download(row)
    else:
        return None  # Unnecessary but good to be explicit


def create_download(connection, organization_id: int, download):
    """Create a download record in the database."""
    model_as_dict = download.to_dict()
    organization = int(organization_id)
    # created_datetime = get_now_datetime_formatted()
    name = model_as_dict['name']
    transfer_name = model_as_dict['transfer_name']
    history_uid = int(model_as_dict['history_uid'])
    bucket_name = model_as_dict['bucket_name']
    obj_name = model_as_dict['obj_name']
    expiration_datetime = get_future_datetime_formatted(days=14)
    query = f"INSERT INTO downloads (name, transfer_name, history_uid, expiration_datetime, organization, bucket_name, obj_name) VALUES('{name}', '{transfer_name}', '{history_uid}', '{expiration_datetime}', '{organization}', '{bucket_name}', '{obj_name}' ) \n RETURNING uid;"
    return connection.query(query)



# Mappings
def get_mappings(connection, organization_id: int):
    """Get data mappings for ``organization_id``
    
    Parameters
    ----------
    connection
        Connection to database
    organization_id : int
        Organization Id
    
    Returns
    -------
    List[models.Mapping]
        List of Mapping objects

    """
    data_mappings = get_rows_by_organization(
        table_name="mappings", connection=connection, organization_id=organization_id
    )
    return [Mapping(tup) for tup in data_mappings]


def get_mapping(connection, organization_id: int, mapping_id: int):
    """Get mapping matching ``organization_id`` and ``mapping_id``
    
    Parameters
    ----------
    connection : 
        Connection to database
    organization_id : int
        Organization Id
    mapping_id : int
        mapping Id
    
    Returns
    -------
    Tuple[Tuple[str, Any]]
        Tuple of 2-tuples representing a row of `mappings` table matching ``organization_id``
        and ``mapping_id``
        Example: 
        (
            ("uid", 1),
            ("organization", 1),
            ("name", "SF to HUD"),
            ("mapping_info", "{}"),
            ("start_format", "csv"),
            ("end_format", "json"),
            ("num_of_transfers", 1)
        )
        
    """

    row = get_row_by_object_id(
        table_name="mappings",
        connection=connection,
        organization_id=organization_id,
        object_id=mapping_id,
    )
    if row is not None:
        return Mapping(row)
    else:
        return None  # Unnecessary but good to be explicit


# Organizations
def get_organization(connection, organization_id: int):
    """Get organization with ``organization_id``
    
    Parameters
    ----------
    connection
        Connection to database
    organization_id : int
        Organization Id
    
    Returns
    -------
    models.Organization
        Organization object

    """
    query = f"select * from organizations where organizations.uid = '{organization_id}'"
    rows = connection.query(query)
    org = rows[0]  # should be only one org
    return Organization(org)


def get_organizations(connection):
    """Get all organizations

    Parameters
    ----------
    connection
        Connection to database
    organization_id : int
        Organization Id

    Returns
    -------
    List[models.Organization]
        List of Organization objects

    """
    query = f"select * from organizations"
    rows = connection.query(query)
    return [Organization(tup) for tup in rows]


# Uploads
def create_upload(connection, organization_id: int, upload):
    """Create upload. Return UID of new record.
    """
    model_as_dict = upload.to_dict()
    organization = int(organization_id)
    created_datetime = get_now_datetime_formatted()
    created_by_uid = model_as_dict['created_by']
    source_mapping_uid = int(model_as_dict['source_mapping_uid'])
    destination_uid = int(model_as_dict['destination_uid'])
    destination_mapping_uid = int(model_as_dict['destination_mapping_uid'])
    location = model_as_dict['location']
    expiration_dt = get_future_datetime_formatted(days=14)
    query = f"INSERT INTO uploads (organization, created_datetime, created_by, source_mapping_uid, destination_uid, destination_mapping_uid, location, expiration_datetime) VALUES ('{organization_id}', '{created_datetime}', '{created_by_uid}', '{source_mapping_uid}', '{destination_uid}', '{destination_mapping_uid}', '{location}', '{expiration_dt}') \n RETURNING uid;"
    return connection.query(query)


def get_upload(connection, organization_id: int, upload_uid: int):
    row = get_row_by_object_id(
    table_name="uploads",
    connection=connection,
    organization_id=organization_id,
    object_id=upload_uid,
    )
    if row is not None:
        return Upload(row)
    else:
        return None  # Unnecessary but good to be explicit




# def create_organization(connection, name: str, created_date: str):
#     """Create organization in database

#     Parameters
#     ----------
#     connection
#         Connection to database
#     name : str
#         Name of database
#     created_date : str
#         Date created

#     """
#     query = f"INSERT INTO organizations (name, created_datetime) VALUES ('{name}', '{created_date}')"
#     connection.query(query)


# def create_data_mapping(connection, user_id: int, name: str, mapping_info: str):
#     """Create data mapping in database

#     Parameters
#     ----------
#     connection
#         Connection to database
#     name : str
#         Name of database
#     created_date : str
#         Date created

#     """
#     query = f"INSERT INTO mappings (Organization, name, MappingInfo) VALUES ((select Organization from users where users.uid = {user_id}), '{name}', '{mapping_info}');"
#     connection.query(query)


# def create_connection(
#     connection,
#     user_id: int,
#     name: str,
#     created_date: str,
#     created_by: int,
#     connection_type: str,
#     connection_info: str,
# ):
#     """Create connection in database

#         Parameters
#         ----------
#         connection
#             Connection to database
#         name : str
#             Name of database
#         created_date : str
#             Date created

#         """
#     query = f"INSERT INTO connections (Organization, name, created_datetime, created_by, Type, ConnectionInfo) VALUES ((select Organization from users where users.uid = {user_id}), '{name}', '{created_date}', '{created_by}', '{connection_type}', '{connection_info}');"
#     connection.query(query)


# def create_user(connection, organization_id: int, name: str, created_date: str):
#     """Create user in database

#     Parameters
#     ----------
#     connection
#         Connection to database
#     organization_id : int
#         Organization to crete user in
#     name : str
#         Name of user
#     created_date : str
#         Date Created

#     """

#     query = f"INSERT INTO users (Organization, name, created_datetime) VALUES ('{organization_id}', '{name}', '{created_date}');"
#     connection.query(query)



# def delete_user(connection, user_id: int):
#     """Delete user with ``user_id`` in database
    
#     Parameters
#     ----------
#     connection
#         Connection to database
#     user_id : int
#         Id of user
    
#     """
#     return delete_row_by_uid(connection, "users", user_id)


# def delete_organization(connection, organization_id: int):
#     """Delete organization with ``organization_id`` in database
    
#     Parameters
#     ----------
#     connection
#         Connection to database
#     organization_id : int
#         Id of organization
    
#     """
#     return delete_row_by_uid(connection, "organizations", organization_id)


# def delete_data_mapping(connection, data_mapping_id: int):
#     """Delete data_mapping with ``data_mapping_id`` in database
    
#     Parameters
#     ----------
#     connection
#         Connection to database
#     data_mapping_id : int
#         Id of data_mapping
    
#     """
#     return delete_row_by_uid(connection, "mappings", data_mapping_id)


# def delete_connection(connection, connection_id: int):
#     """Delete connection with ``connection_id`` in database
    
#     Parameters
#     ----------
#     connection
#         Connection to database
#     connection_id : int
#         Id of connection
    
#     """
#     return delete_row_by_uid(connection, "connections", connection_id)


# def delete_transfer(connection, transfer_id: int):
#     """Delete transfer with ``transfer_id`` in database
    
#     Parameters
#     ----------
#     connection
#         Connection to database
#     transfer_id : int
#         Id of transfer
    
#     """
#     return delete_row_by_uid(connection, "transfers", transfer_id)
