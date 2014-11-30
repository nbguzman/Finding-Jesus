# Load kjv.txt into the kjv table

DELETE FROM kjv;
LOAD DATA LOCAL INFILE 'kjv.txt' INTO TABLE kjv;
