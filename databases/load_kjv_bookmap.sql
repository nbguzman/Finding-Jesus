# Load kjv_bookmap.txt into the kjv_bookmap  table

DELETE FROM kjv_bookmap;
LOAD DATA LOCAL INFILE 'kjv_bookmap.txt' INTO TABLE kjv_bookmap;
