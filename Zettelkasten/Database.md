Most databases—for example, [[relational databases]]—are multidimensional, allowing [[information]] to be accessed from various views through internal linking between entries. Traditional flat file systems are one-dimensional. Traditional files present [[information]] from a single point of view and do not interact with other files.

As computing evolved, applications were implemented as separate systems and collections of [[data]]. Payroll was processed using the payroll file, employee records were maintained by the personnel department, and inventory was managed via the inventory file. Much of the [[information]] required by an organization was duplicated throughout the company while related items were stored in separate systems. Database systems integrate the [[information]] stored and maintained by an organization. With such a system, the same employee [[data]] could be used to process payroll, calculate vacation days, and manage employee benefits. Users in logistics could use the same system to record inventory audits, restock orders, and report damaged goods.
### Database Research

Database research is the act of analyzing and converting [[data]] into [[information]] that can be used in decision-making.

Database systems are the underlying technology that supports much of the World Wide Web. Websites interface between clients and databases, responding to client requests. Web servers search a database, organize the results in a web page, and send that page to the client.
### Database Management Systems

A typical database application has two major layers: an application layer and a database management layer. The application layer communicates with the end user and can be fairly complex. For example, when end users access a database through a website, the application layer consists of programs and services within a server that queries the database on behalf of the client.

The application layer of a database does not directly manipulate the [[data]]. After the [[application software]] receives a request from a user, it uses the database management system (DBMS) as a tool to obtain the results. If the request is to add or delete [[data]] to or from the system, the DBMS alters the database after receiving the request through the application layer. If the request is to retrieve [[information]], it is the DBMS that performs the required searches.

The DBMS is similar to an [[operating system]] in that it supports the [[application software]] and the [[data]].

Learn more about database management systems by accessing a free version of [Microsoft Access(opens in new tab)](https://www.microsoft.com/en-us/microsoft-365/access) or [OpenOffice Base(opens in new tab)](https://www.openoffice.org/product/base.html).

A database table is composed of records and fields that hold [[data]]. For more [[information]], do a bit of research on such benefits and weaknesses of Microsoft Access.

### Database Elements

A database table, also known as a datasheet, is composed of records and fields that hold [[data]]. [[Data]] is stored in records. The records are represented as rows in a table with related [[information]]. The example table below has three records storing [[data]] for three different employees.

The columns represent fields. A field contains a single piece of [[data]] about the subject of a record. The five fields in the example table are First Name, Last Name, Age, Position, and Years in Position.

### Database Operations

#### Union Operations
The _**union operation**_ combines distinct fields from multiple tables that have the same set of attributes and [[data]] types. For example, if one column accepts integers and another accepts variable characters, they would not be compatible for a union.

#### Product Operations
The _**product operation**_ creates a result table that includes all of the attributes from the two tables; each row of the second table is added to each row of the first table.

`SELECT Shifts.WingSegment, Shifts.Shift, NurseName.LastName`  
  
`FROM Shifts`  
  
`CROSS JOIN NurseName;`

Notice when you are using more than one table as a source, the table name precedes the attribute name, separated by a period. Shifts.WingSegment refers to the field ‘WingSegment’ from the table ‘Shifts.’

#### Join Operation
A _**join operation**_ combines two tables, but records are only appended when a matching criterion is met. The result table includes a row with the attributes of both tables only when attributes from the first database table match related attributes from the second database table.

`SELECT*`
`FROM Patient, Nurse;`

This syntax selects all the fields from both ‘Patient’ and ‘Nurse’ tables, and joins them into one large table. This is referred to as an implicit join. Alternatively, to get the same results, an explicit join can be used as shown below.

`SELECT*`
`FROM Patient CROSS JOIN Nurse;`

### Database Administration

Database management and administration are important functions in any organization that is dependent on one or more databases. It refers to the whole set of activities that ensure all databases are highly available, secure, and scalable. Scalability is the ability to accommodate increased demands while using existing resources (e.g., increasing memory capacity before being fully exhausted).

### DBA Responsibilities

A majority of the database administration (DBA) responsibilities fall into these categories:

- Database security—ensuring that only authorized users have access to the database and fortifying it against unauthorized access
- Database tuning—optimizing performance of database systems
- High availability—making replicas (copies) of databases available from various locations; if one copy is unavailable due to outage, the alternate location can continue database services
- Business continuity—continuing core business operations effectively, even with the disruption of some auxiliary services
- Backup and recovery—planning for and executing adequate backup and recovery procedures
- Reporting—writing complex queries and generating reports for users
- Designing and developing database applications—writing code to interact with the database resources

The DBA needs a complex set of specialized skills, as well as current knowledge of database developments, acquired through intense professional development.