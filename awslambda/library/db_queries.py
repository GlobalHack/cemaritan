# functions for actually making the database calls
from typing import Any, List, Tuple

from models import Connection, Mapping, Organization, Transfer, User, History, Download


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
                ("createddate", "2019-03-09 20:42:03"),
                ("createdby", 1),
                ("type", "A"),
                ("connectioninfo", "{conn string}")
            ),
            (
                ("uid", 2),
                ("organization", 1),
                ("name", "CW"),
                ("createddate", "2019-03-10 04:42:03"),
                ("createdby", 1),
                ("type", "B"),
                ("connectioninfo", "{conn string}")
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
        UID of object to return, if exists
    
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
            ("createddate", "2019-03-09 20:42:03"),
            ("createdby", 1),
            ("type", "A"),
            ("connectioninfo", "{conn string}")
        )

    """
    try:
        if query is None:
            query = f"select * from {table_name} where {table_name}.organization = {organization_id} and {table_name}.UID = {object_id}"
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
        UID of row to delete
    
    Returns
    -------
    bool
        Indicating success or failure of deletion
    """

    try:
        query = f"DELETE from {table_name} where {table_name}.UID={uid}"
        connection.query(query)
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
        Example: 
        (
            ("uid", 1),
            ("name", "CW to SF"),
            ("createddate", "2019-03-20 20:42:03"),
            ("createdby", 1),
            ("organization", 1),
            ("source", 2),
            ("sourcemapping", 2),
            ("destination", 1),
            ("destinationmapping", 1),
            ("startdatetime", "2019-03-13 20:42:03"),
            ("frequency", "1 day"),
            ("recordfilter", "filter a"),
            ("active", 1)
        )
        
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
            ("date", "2019-03-20 20:42:03"),
            ("createdbyuser", 1),
            ("name", None),
            ("details", None),
            ("sourceuid", 0),
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


# Transfers
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
                    t6.UID,
                    t6.Name,
                    t6.Organization2 as Organization,
                    t6.CreatedDate as CreatedDate,
                    t6.Source2 as Source,
                    t6.SourceMapping2 as SourceMapping,
                    t6.Destination2 as Destination,
                    t6.DestinationMapping2 as DestinationMapping,
                    CASE WHEN t6.Active = 1 THEN 'TRUE' ELSE 'FALSE' END Active,
                    t6.StartDateTime as StartTime,
                    t6.frequency as Frequency
                    from 
                    (select t5.*, d2.Name as DestinationMapping2 from
                    (select t4.*, d.Name as SourceMapping2 from 
                    (Select t3.*, c2.Name as Destination2 from
                    (select t2.*, c.Name as Source2 from
                    (select t.*, o.Name as Organization2 from
                    (select * from Transfers where Transfers.organization = {organization_id}) as t
                    LEFT JOIN 
                    Organizations as o
                    on o.UID = t.Organization) as t2
                    LEFT join
                    Connections as c
                    on t2.Source=c.UID) as t3
                    left join
                    Connections as c2
                    on t3.Destination=c2.UID) as t4
                    left join
                    Mappings as d
                    on t4.SourceMapping=d.UID) as t5
                    left join
                    Mappings as d2
                    on t5.DestinationMapping=d2.UID) as t6"""
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
            ("createddate", "2019-03-20 20:42:03"),
            ("createdby", 1),
            ("organization", 1),
            ("source", 2),
            ("sourcemapping", 2),
            ("destination", 1),
            ("destinationmapping", 1),
            ("startdatetime", "2019-03-13 20:42:03"),
            ("frequency", "1 day"),
            ("recordfilter", "filter a"),
            ("active", 1)
        )
        
    """
    QUERY = f"""select 
                    t6.UID,
                    t6.Name,
                    t6.Organization2 as Organization,
                    t6.CreatedDate as CreatedDate,
                    t6.Source2 as Source,
                    t6.SourceMapping2 as SourceMapping,
                    t6.Destination2 as Destination,
                    t6.DestinationMapping2 as DestinationMapping,
                    CASE WHEN t6.Active = 1 THEN 'TRUE' ELSE 'FALSE' END Active,
                    t6.StartDateTime as StartTime,
                    t6.frequency as Frequency
                    from 
                    (select t5.*, d2.Name as DestinationMapping2 from
                    (select t4.*, d.Name as SourceMapping2 from 
                    (Select t3.*, c2.Name as Destination2 from
                    (select t2.*, c.Name as Source2 from
                    (select t.*, o.Name as Organization2 from
                    (select * from Transfers where Transfers.organization = {organization_id} and Transfers.UID = {transfer_id}) as t
                    LEFT JOIN 
                    Organizations as o
                    on o.UID = t.Organization) as t2
                    LEFT join
                    Connections as c
                    on t2.Source=c.UID) as t3
                    left join
                    Connections as c2
                    on t3.Destination=c2.UID) as t4
                    left join
                    Mappings as d
                    on t4.SourceMapping=d.UID) as t5
                    left join
                    Mappings as d2
                    on t5.DestinationMapping=d2.UID) as t6"""
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


# Users
def get_users(connection, organization_id: int):
    """Get users for ``organization_id``
    
    Parameters
    ----------
    connection
        Connection to database
    organization_id : int
        Organization Id
    
    Returns
    -------
    List[models.User]
        List of User objects

    """
    users = get_rows_by_organization(
        table_name="users", connection=connection, organization_id=organization_id
    )
    return [User(tup) for tup in users]


def get_user(connection, organization_id: int, user_id: int):
    """Get user matching ``organization_id`` and ``user_id``
    
    Parameters
    ----------
    connection : 
        Connection to database
    organization_id : int
        Organization Id
    user_id : int
        user Id
    
    Returns
    -------
    Tuple[Tuple[str, Any]]
        Tuple of 2-tuples representing a row of `users` table matching ``organization_id``
        and ``user_id``
        Example: 
        (
            ("uid", 1),
            ("name", "Matt"),
            ("createddate", "2019-03-10 10:42:03"),
            ("organization", 1)
        )
        
    """

    row = get_row_by_object_id(
        table_name="users",
        connection=connection,
        organization_id=organization_id,
        object_id=user_id,
    )
    if row is not None:
        return User(row)
    else:
        return None  # Unnecessary but good to be explicit


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
            ("mappinginfo", "{}"),
            ("startformat", "csv"),
            ("endformat", "json"),
            ("numoftransfers", 1)
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
#     query = f"INSERT INTO Organizations (Name, CreatedDate) VALUES ('{name}', '{created_date}')"
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
#     query = f"INSERT INTO Mappings (Organization, Name, MappingInfo) VALUES ((select Organization from Users where Users.UID = {user_id}), '{name}', '{mapping_info}');"
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
#     query = f"INSERT INTO Connections (Organization, Name, CreatedDate, CreatedBy, Type, ConnectionInfo) VALUES ((select Organization from Users where Users.UID = {user_id}), '{name}', '{created_date}', '{created_by}', '{connection_type}', '{connection_info}');"
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

#     query = f"INSERT INTO Users (Organization, Name, CreatedDate) VALUES ('{organization_id}', '{name}', '{created_date}');"
#     connection.query(query)


def create_transfer(
    connection,
    user_id: int,
    name: str,
    created_date: str,
    created_by: int,
    organization_id: int,
    source: int,
    source_mapping: int,
    destination: int,
    destination_mapping: int,
    start_date_time: str,
    frequency: str,
    record_filter: str,
    active: bool,
):
    """Create transfer in database
    
    Parameters
    ----------
    connection
        Connection to database
    user_id : int
        User creating transfer
    name : str
        Name of transfer
    created_date : str
        Date transfer was created 
    created_by : int
        User creating transfer
    organization_id : int
        Organization user belongs to
    source : int
        Id of Connection source
    source_mapping : int
        Mapping of source system
    destination : int
        Id of destination Connection
    destination_mapping : int
        Mapping of destination system
    start_date_time : str
        Date to start transfer
    frequency : str
        Frequency of transfer
    record_filter : str
        Filter records parameters
    active : bool
        Is connection currently active
    
    """

    query = f"INSERT INTO Transfers (Organization, Name, CreatedDate, CreatedBy, Source, SourceMapping, Destination, DestinationMapping, StartDateTime, Frequency, RecordFilter, Active) VALUES ((select Organization from Users where Users.UID = {user_id}), '{name}', '{created_date}', '{created_by}', '{source}', '{source_mapping}', '{destination}', '{destination_mapping}', '{start_date_time}', '{frequency}', '{record_filter}', '{active}');"
    connection.query(query)


def delete_user(connection, user_id: int):
    """Delete user with ``user_id`` in database
    
    Parameters
    ----------
    connection
        Connection to database
    user_id : int
        Id of user
    
    """
    return delete_row_by_uid(connection, "Users", user_id)


def delete_organization(connection, organization_id: int):
    """Delete organization with ``organization_id`` in database
    
    Parameters
    ----------
    connection
        Connection to database
    organization_id : int
        Id of organization
    
    """
    return delete_row_by_uid(connection, "Organizations", organization_id)


def delete_data_mapping(connection, data_mapping_id: int):
    """Delete data_mapping with ``data_mapping_id`` in database
    
    Parameters
    ----------
    connection
        Connection to database
    data_mapping_id : int
        Id of data_mapping
    
    """
    return delete_row_by_uid(connection, "Mappings", data_mapping_id)


def delete_connection(connection, connection_id: int):
    """Delete connection with ``connection_id`` in database
    
    Parameters
    ----------
    connection
        Connection to database
    connection_id : int
        Id of connection
    
    """
    return delete_row_by_uid(connection, "Connections", connection_id)


def delete_transfer(connection, transfer_id: int):
    """Delete transfer with ``transfer_id`` in database
    
    Parameters
    ----------
    connection
        Connection to database
    transfer_id : int
        Id of transfer
    
    """
    return delete_row_by_uid(connection, "Transfers", transfer_id)
