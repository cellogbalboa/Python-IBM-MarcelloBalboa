# IBM CAI Challenge 2018 - Database Migration Starter
This is the starter app to help you manage your Postgres database migrations using Flyway and manual database access with pgAdmin.

Database migrations are the series of scripts that create, modify, delete, and otherwise affect objects in your database.

This starter gives you easy to use tools to get started managing your database for the challenge and a 'Hello, World!' example.

## Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Code Structure
* `flyway.conf` contains the Flyway configuration settings
* `sql` contains the sql-based database migration scripts. The convention is that they are versioned such that V1_5_name_of_the_script.sql would be Version 1.5. Flyway parses these filenames very strictly. 

### Prerequisites
* You will need Flyway CLI: https://flywaydb.org/
* You will need pgAdmin: https://www.pgadmin.org/download/

### Creating a database
First, you need to create a database for your application. 

Make sure you have the IBM Cloud CLI installed. If you need to install it check here: https://console.bluemix.net/docs/cli/index.html#overview

Run this command to check you have the tools installed. If you saw a version number then you are ready to proceed!
```
ibmcloud --version
```

Log in to the IBM Cloud CLI
```
ibmcloud login -a https://api.ng.bluemix.net
```

Target your CLI session for cloud foundry and resource groups
```
ibmcloud target --cf
ibmcloud target -g cai-challenge
```

Before proceeding, here is how to find help
```
ibmcloud help
```

Create a database. Use your first initial + lastname-pgsql for YOUR_DATABASE_NAME ie jdoe-pgsql
```
ibmcloud resource service-instance-create *YOUR_DATABASE_NAME* databases-for-postgresql standard us-south
```

Check your database creation process. Once state = 'active' then proceed. This can take a while, so start thinking about your user stories and code. Check back on this periodically. 
```
ibmcloud resource service-instances
```

Create a service alias so your database can be used in cloud foundry
```
ibmcloud resource service-alias-create *YOUR_DATABASE_NAME* --instance-name *YOUR_DATABASE_NAME*
```

Verify your database is available in cloud foundry
```
ibmcloud cf services
```

Bind your database service to your application. This creates credentials and connection information for you to use. This command will fail if you did not create your application yet (you hopefully should have been doing that while you waited for the database to be provisioned).
```
ibmcloud cf bind-service cai-challenge *YOUR_DATABASE_NAME*
```

You'll need to restage (aka restart) your application to pick up the new database credentials provided as environment variables. 
```
ibmcloud cf restage cai-challenge
```

Find out your app's database connection information. It is stored in the `VCAP_SERVICES` environment variable for your app. 
```
ibmcloud cf env cai-challenge
```
### Using Flyway
You should first have set up your database in IBM Cloud with the preceeding commands and make sure you have flyway installed.

Check if flyway is installed. If you get version number then flyway is ready.
```
flyway -v
```

Get your database host name, port number, database name, username, and password from the VCAP_SERVICES environment variable. You'll use these in the next step.
```
ibmcloud cf env cai-challenge
```

Edit `flyway.conf` and replace these variables with your actual values from the previous step. `flyway.conf` now has your secret password in it - don't check that into GitHub!
```
flyway.url=jdbc:postgresql://$HOSTNAME:$PORT/$DBNAME?sslmode=require
flyway.user=$USERNAME
flyway.password=$PASSWORD
```

Flyway should now be configured. Lets test it. 

Change directory to the database folder. This is where flyway commands should be executed from.
```
cd database
```

Check migration status
```
flyway info
```

If flyway can connect to your database you should see something very similar to this:
```
Benjamins-MacBook-Pro:database ben.stokes@us.ibm.com$ flyway info
Flyway Community Edition 5.1.4 by Boxfuse

Database: jdbc:postgresql://582a69d8-23f6-42c3-ad11-d0b140eb4dd2.8f7bfd8f3faa4218aec56e069eb46187.databases.appdomain.cloud:31434/ibmclouddb (PostgreSQL 10.5)
Schema version: << Empty Schema >>

+-----------+---------+--------------------------+------+--------------+---------+
| Category  | Version | Description              | Type | Installed On | State   |
+-----------+---------+--------------------------+------+--------------+---------+
| Versioned | 2.0     | create cai schema        | SQL  |              | Pending |
| Versioned | 2.1     | create hello world table | SQL  |              | Pending |
| Versioned | 2.2     | hydrate test data        | SQL  |              | Pending |
+-----------+---------+--------------------------+------+--------------+---------+
```

Now its time to run your database migrations.
```
flyway migrate
```

Run `flyway info` again and you will see the migrations have been installed.
```
+-----------+---------+------------------------------+--------+---------------------+---------+
| Category  | Version | Description                  | Type   | Installed On        | State   |
+-----------+---------+------------------------------+--------+---------------------+---------+
|           |         | << Flyway Schema Creation >> | SCHEMA | 2018-10-12 19:03:46 | Success |
| Versioned | 2.0     | create cai schema            | SQL    | 2018-10-12 19:03:47 | Success |
| Versioned | 2.1     | create hello world table     | SQL    | 2018-10-12 19:03:47 | Success |
| Versioned | 2.2     | hydrate test data            | SQL    | 2018-10-12 19:03:48 | Success |
+-----------+---------+------------------------------+--------+---------------------+---------+
```

Flyway can also clean your schema. Clean means *delete everything.* Go ahead and try it. Don't worry, we'll install it again very quickly.
```
flyway clean
```

`flyway info` will now show you that the migrations are pending again. Check it and then reinstall the database.
```
flyway migrate
```

Flyway's database migrations are designed for this and it is helpful to clean and recreate in a development environment. You should be mindful that, if you make changes outside of flyway, then run `flyway clean` then you will lose those changes! Be careful!

### Using pgAdmin
pgAdmin is a graphical database management tool for Postgres. 

To get started, get your database host name, port number, database name, username, and password from the VCAP_SERVICES environment variable. You'll use these in the next step. You can also pull them from your `flyway.conf` file - its the same thing. 
```
ibmcloud cf env cai-challenge
```

Launch pgAdmin and create a new server. Enter your connection information into the corresponding fields and connect.

1. Browse to the `ibmclouddb.schemas.cai.tables` tree. 
2. Right click Tables and enter some information into the creation dialog (like table name, add a column, etc).
3. Click on the SQL tab and you will see that pgAdmin will generate the SQL for you based on your inputs to the GUI. 

It can be very helpful to use the GUI to create these scripts and then add them as flyway migrations and let flyway actually run the scripts for you. Remember, anything you create outside of flyway will be deleted if you run `flway clean`!

#### Query Tool
pgAdmin has a query tool that is very helpful. Open a query tool tab from the Tools menu. 

Enter a query like this, select the text, and click the lightening bolt toolbar button.
```
select * from cai.flyway_schema_history;
```