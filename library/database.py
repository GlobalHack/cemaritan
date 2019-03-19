# functions for actually making the database calls
from typing import List, Tuple

# import models

# Sample "create" queries
"""
add new organization: DONE
INSERT INTO Organizations (Name, CreatedDate) VALUES (_name_, _createddate_)

add new data mapping: DONE
INSERT INTO DataMappings (Organization, Name, MappingInfo) VALUES ((select Organization from Users where Users.UID = 1), _name_, _mapping_info_);

add a new connection: DONE
INSERT INTO Connections (Organization, Name, CreatedDate, CreatedBy, Type, ConnectionInfo) 
                VALUES ((select Organization from Users where Users.UID = 1), _name_, _createddate_, createdby_, _type_, _connecitoninfo_);

for deleting user: DONE
DELETE from Users where Users.UID=6

#####
Also have functions return in JSON for front end
#####
"""


def get_rows_by_organization(
    table_name: str, connection, organization_id: int
) -> List[Tuple]:
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
    List[Tuple]
        List of tuples representing each row of the response of the query
        
    """
    query = f"select * from {table_name} where {table_name}.organization = (select organization from users where users.UID = {organization_id})"
    return connection.query(query).fetchall()


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

    return get_rows_by_organization(
        table_name="connections", connection=connection, organization_id=organization_id
    )


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
    return get_rows_by_organization(
        table_name="transfers", connection=connection, organization_id=organization_id
    )


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
    return get_rows_by_organization(
        table_name="users", connection=connection, organization_id=organization_id
    )


def get_data_mappings(connection, organization_id: int):
    """Get data mappings for ``organization_id``
    
    Parameters
    ----------
    connection
        Connection to database
    organization_id : int
        Organization Id
    
    Returns
    -------
    List[models.DataMapping]
        List of DataMapping objects

    """
    return get_rows_by_organization(
        table_name="datamappings",
        connection=connection,
        organization_id=organization_id,
    )


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
    return connection.query(query).fetchall()


def get_organizations(connection, organization_id: int):
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
    return connection.query(query).fetchall()


def create_organization(connection, name: str, created_date: str):
    """Create organization in database
    
    Parameters
    ----------
    connection
        Connection to database
    name : str
        Name of database
    created_date : str
        Date created

    """
    query = f"INSERT INTO Organizations (Name, CreatedDate) VALUES ('{name}', '{created_date}')"
    connection.query(query)


def create_data_mapping(connection, user_id: int, name: str, mapping_info: str):
    """Create data mapping in database
    
    Parameters
    ----------
    connection
        Connection to database
    name : str
        Name of database
    created_date : str
        Date created

    """
    query = f"INSERT INTO DataMappings (Organization, Name, MappingInfo) VALUES ((select Organization from Users where Users.UID = {user_id}), '{name}', '{mapping_info}');"
    connection.query(query)


def create_connection(
    connection,
    user_id: int,
    name: str,
    created_date: str,
    created_by: int,
    connection_type: str,
    connection_info: str,
):
    """Create connection in database
        
        Parameters
        ----------
        connection
            Connection to database
        name : str
            Name of database
        created_date : str
            Date created

        """
    query = f"INSERT INTO Connections (Organization, Name, CreatedDate, CreatedBy, Type, ConnectionInfo) VALUES ((select Organization from Users where Users.UID = {user_id}), '{name}', '{created_date}', '{created_by}', '{connection_type}', '{connection_info}');"
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

    query = f"DELETE from Users where Users.UID={user_id}"
    connection.query(query)

