# ShynaDatabase

***Suggested: Not to use***

This package will take care of cleaning the database and querying the database. More functionality will be added as I process.

```
test = ShynaDatabase() # Make the object of the class
# share the host and password credentail and key file
cred_filename_host = 'host.ini' 
key_file_host = 'host.key'
cred_filename_pass = 'dbpass.ini'
key_file_pass = 'dbpass.key'
test.host = test.set_host(cred_filename_host=cred_filename_host, key_file_host=key_file_host)
test.passwd = test.set_password(cred_filename_pass=cred_filename_pass, key_file_pass=key_file_pass)


print(test.check_connectivity()) # True if the database is connected
query = "SELECT * FROM test"
print(test.create_insert_update_or_delete(query=query)) # returns a dictoinary with result or 'EMPTY' as string

````
