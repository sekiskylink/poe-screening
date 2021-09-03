less poes.csv|awk -F"#" '{print "INSERT INTO ports (name,dhis2_code, dhis2_path, dhis2_parent) VALUES(\47" $1 "\47, \47" $2 "\47, \47" $3 "\47, \47" $4 "\47);"}' > poes.sql

less regions.csv|awk -F"#" '{print "INSERT INTO orgunits (name,dhis2_code, dhis2_level, dhis2_parent, dhis2_path) VALUES(\47" $1 "\47, \47" $2 "\47, 2, \47" $4 "\47, \47" $3 "\47);"}' > regions.sql

less districts.csv|awk -F"#" '{print "INSERT INTO orgunits (name,dhis2_code, dhis2_level, dhis2_parent, dhis2_path) VALUES(\47" $1 "\47, \47" $2 "\47, 3, \47" $4 "\47, \47" $3 "\47);"}' > districts.sql
