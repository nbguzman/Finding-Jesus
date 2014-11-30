# kjv_bookmap table used by kjv.pl script

# bsect is O = Old Testament, N = New Testamant, A = Apocrypha
# bnum is the book number.  This actually is sufficient to
# identify any book.  (The section isn't needed.)

DROP TABLE IF EXISTS kjv_bookmap;
CREATE TABLE kjv_bookmap
(
  bsect ENUM('O','N','A') NOT NULL, # book section
  bnum  TINYINT UNSIGNED NOT NULL, # book number
  bname CHAR(40),                  # book name
  INDEX (bsect),
  INDEX (bnum)
);
