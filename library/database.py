# functions for actually making the database calls
from library.connection import SQLite
from sqlite3 import Connection
from typing import List, Tuple

# Sample "create" queries
"""
add new organization: DONE
INSERT INTO Organizations (Name, CreatedDate) VALUES (_name_, _createddate_)

add new data mapping
INSERT INTO DataMappings (Organization, Name, MappingInfo) VALUES ((select Organization from Users where Users.UID = 1), _name_, _mapping_info_);

add a new connection
INSERT INTO Connections (Organization, Name, CreatedDate, CreatedBy, Type, ConnectionInfo) 
                VALUES ((select Organization from Users where Users.UID = 1), _name_, _createddate_, createdby_, _type_, _connecitoninfo_);

for deleting user
DELETE from Users where Users.UID=6
"""

def get_rows_by_organization(
    table_name: str, connection: Connection, organization_id: str
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


def get_connections(connection, organization_id):
    return get_rows_by_organization(
        table_name="connections", connection=connection, organization_id=organization_id
    )


def get_transfers(connection, organization_id):
    return get_rows_by_organization(
        table_name="transfers", connection=connection, organization_id=organization_id
    )


def get_users(connection, organization_id):
    return get_rows_by_organization(
        table_name="users", connection=connection, organization_id=organization_id
    )


def get_data_mappings(connection, organization_id):
    return get_rows_by_organization(
        table_name="datamappings", connection=connection, organization_id=organization_id
    )


def get_organizations(connection, organization_id):
    query = f"select * from organizations where organizations.uid = '{organization_id}'"
    return connection.query(query).fetchall()


def create_organization(connection, name, created_date):
    query = f"INSERT INTO Organizations (Name, CreatedDate) VALUES ('{name}', '{created_date}')"
    connection.query(query)


def create_data_mapping(connection, user_id, name, mapping_info):
    query = f"INSERT INTO DataMappings (Organization, Name, MappingInfo) VALUES ((select Organization from Users where Users.UID = {user_id}), '{name}', '{mapping_info}');"
    connection.query(query)


def update_organization(id):
    pass


def delete_organization(id):
    pass


def update_user(id):
    pass


def create_user(id):
    pass


def delete_user(id):
    pass


def update_transfer(id):
    pass


def create_transfer(id):
    pass


def delete_transfer(id):
    pass


def update_connection(id):
    pass


def create_connection(id):
    pass


def delete_connection(id):
    pass


def update_data_mapping(id):
    pass


def delete_data_mapping(id):
    pass

