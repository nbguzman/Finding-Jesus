mcb-kjv - Files for the MySQL Cookbook KJV distribution

Paul DuBois
paul@kitebird.com

This distribution contains some of the files for the examples in the
MySQL Cookbook that use the kjv table containing the text of the King
James Version of the Bible.

kjv.txt: Text file containing KJV data to be loaded into the kjv table
kjv.sql: SQL script to create the kjv table
load_kjv.sql: SQL script to load/reload kjv.txt into kjv.sql

kjv.sql creates the kjv table using the MyISAM storage engine by default.
It contains instructions about using InnoDB instead (requires MySQL 5.6
or higher).

Use the files as follows (I assume you have created a cookbook database
already, as per the instructions in the Cookbook):

% mysql cookbook < kjv.sql
% mysql cookbook < load_kjv.sql

If you want to use the kjv.pl search script, you must also create
the kjv_bookmap tables, which involves these files:

kjv.pl: The search script itself
kjv_bookmap.txt: Text file containing book number-to-name mapping
kjv_bookmap.sql: SQL script to create the kjv_bookmap table
load_kjv_bookmap.sql: SQL script to load kjv_bookmap.txt into kjv_bookmap.sql

Use the files as follows:

% mysql cookbook < kjv_bookmap.sql
% mysql cookbook < load_kjv_bookmap.sql

Then install kjv.pl in your Web server's script directory.  (The script
requires a library file, Cookbook.pm, from the MySQL Cookbook recipes
distribution. Make sure that file is in a directory searched by your
Perl interpreter.)

The kjv.txt file was created from the version of the KJV that is available
at the Unbound Bible Project at Biola University. See:
    http://unbound.biola.edu/
    http://unbound.biola.edu/zips/index.cfm?lang=English

The MySQL Cookbook distribution has been modified somewhat to make it
easier to use for FULLTEXT searching.  Differences between the Biola
and Cookbook KJV distributions are as follows:

- Biola represents books using book ID values consisting of a number
  followed by a letter.  The number is a two-digit value from 01 to
  86 representing the index of the book within the file.  (01 to 39 are
  for Old Testament books, 40 through 66 are New Testament books, and
  67 through 86 are books of the Apocrypha).  The letter is O (Old
  Testament), N (New Testament), or A (Apocrypha).
- The Cookbook uses separate book number and book section columns,
  and the numbers are not zero-filled.
- The Cookbook does not include any Apocrypha books, so book numbers
  range from 1 to 66.
- The Cookbook includes book names (Genesis, Exodus, etc.) as well as
  the numbers.  This denormalizes the dataset, but avoids the need for
  a join to display book names in search results.
