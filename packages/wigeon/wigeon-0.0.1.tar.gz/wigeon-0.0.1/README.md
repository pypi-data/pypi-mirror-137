# wigeon
DB Migrations for the coninuous developer.

This is a framework for building and deploying sql database migrations across your CI/CD-based applications!

**STILL VERY MUCH A WORK IN PROGRESS!!**

## Features included
- Database package creation
- Auto-serialized Migration creation
- Migration manifest management
- Migration build tagging
- connection arguments passed at runtime to support deployment across multiple
  enviroments
## Features to build
- json manifests managed via environment variables
- migration changelog written to target database
- connection manager
- connection via environment variables
- deploy/run sql script migrations
- sqlite support
- mssqlserver support

## To use (FROM GIT REPO):
Access help:
```bash
python3 wigeon --help
```

Create `fly` package for `sqlite` with local, dev, qa, and prod environments:
```bash
python3 -m wigeon createpackage fly sqlite --environments=local,dev,qa,prod
```

Add migrations to the `fly` package with build tag of `0.0.1`:
```bash
python3 -m wigeon createmigration initialize_db fly 0.0.1
python3 -m wigeon createmigration add_people_table fly 0.0.1
python3 -m wigeon createmigration add_cars_table fly 0.0.1
```

List all migrations for the `fly` package:
```bash
python3 -m wigeon listmigrations fly
```

Run migrations for the `fly` package (a local sqlite connection):
```bash
python3 -m wigeon runmigrations fly --connstring=/path/to/exampledb.sqlite
```

## To use (FROM PIP INSTALL):
Access help:
```bash
wigeon --help
```

Create `fly` package for `sqlite` with local, dev, qa, and prod environments:
```bash
wigeon createpackage fly sqlite --environments=local,dev,qa,prod
```

Add migrations to the `fly` package with build tag of `0.0.1` :
```bash
wigeon createmigration initialize_db fly 0.0.1
wigeon createmigration add_people_table fly 0.0.1
wigeon createmigration add_cars_table fly 0.0.1
```

List all migrations for the `fly` package:
```bash
wigeon listmigrations fly
```

Run migrations for the `fly` package (a local sqlite connection):
```bash
wigeon runmigrations fly --connstring=/path/to/exampledb.sqlite
```

## Requirements

### For gcc compiler on Ubuntu
```bash
sudo apt install build-essential
```
### For ODBC on Ubuntu
```bash
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
sudo apt-get install -y unixodbc-dev
```

### For mssql-server ODBC on Ubuntu
Found at:
https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15

```bash
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

#Download appropriate package for the OS version
#Choose only ONE of the following, corresponding to your OS version

#Ubuntu 16.04
curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

#Ubuntu 18.04
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

#Ubuntu 20.04
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

#Ubuntu 21.04
curl https://packages.microsoft.com/config/ubuntu/21.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

exit
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install -y unixodbc-dev
```