#!/usr/bin/perl
###############################################
# first example using templating, xhtml and css
# (c) ckaduri, 2002-2008
# version 0.9a
#
##############################################
use strict;
use Template;   #step 1
use DBI;
use CGI;

use POSIX qw/ceil/; #allows use of ceiling function
use URI::Escape; #allows encoding strings for url
use HTML::Entities;
use Apache::Session::MySQL;
################################ 
## Declaration of Variables   ##
################################
my($template, $tt_object, $cgi_object, $sample, $vars, @records, %selectBooks, %chapters, $i, $bsect, $bname, $bnum, %sections, %forms, $forms, %translations);
my($debug)=0;
my($database)="bible";
my($hostname)="127.0.0.1";
my($db)="DBI:mysql:database=$database;host=$hostname";
my($user)="root";
my($password)="";

my($searched, $and, $orderBy, $limit, @searchRecords, $offset, $resultsPP);
my($numRowsSearched, $totalPages, $pageNow, $home, $pageN, $pageP, $first, $last);
my(%pageURIs, $curPageURI, $URIGetVals, $resultURIs);
my($prevPage, $nextPage, $prevBulk, $nextBulk, %visiblePages, $visible, $showLeft, $showRight);
my($cnumParam, $bookParam, $goBack);
my($rownum, $bsectR, $bnameR, $bnumR, $cnumR, $vnumR, $vtextR);
my($count_only, $book, $phrase, $bool, $translation);
my($searchOrder, %searchOrder, $searchResultsPP, %searchResultsPP);
my(@compTrans, $transURIs, $vnumParam, $vnumFlag, $flag);
my %sect_names = (
		'A' => 'Entire Bible',
		'O' => 'Old Testament',
		'N' => 'New Testament'
	);
	
%searchResultsPP =
	(
		'10' => '10',
		'20' => '20',
		'50' => '50',
		'100' => '100',
	);	
	
%searchOrder =
	(
		'R' => 'Relevance',
		'N' => 'Natural Book Order',
		'A' => 'Alphabetical Order'
	);

%translations = 
	(
		'asv'			=> 'American Standard',
		'basic_english'	=> 'Basic English',
		'kjv'			=> 'King James',
		'web'			=> 'Web',
		'webster'		=> 'Webster',
		'ylt'			=> 'Young Literal'
	);
sub highlightWords
{
	my($text, $words) = @_;
		#print "before = $text <br/>";
        foreach my $word ($words)
        {
                $text =~ s/($word)/<span class=\"highlight_word\">$1<\/span>/ig;
        }
		#print "after = $text <br/>";
        return $text;
}
#########################
# debug                 #
#########################

if($debug)
    {
    }
	
#########################
# Connect to Database   #
#########################  
 
my $db_handle = DBI->connect($db, $user, $password) or die "Unable to connect: $DBI::errstr\n";

#########################
# Generate Magic Header #
#########################
$cgi_object=new CGI;

print $cgi_object->header('text/html');

################################ 
## New Template Object(step 2)##
################################

$tt_object = Template->new(
    {
    INCLUDE_PATH => 
		[ './tt2' ],
    #PRE_PROCESS=> 'header.ex.tt2',
    #POST_PROCESS=> 'footer.ex.tt2'
    }
    );
$template = 'kjv.tt2';

###################################### 
## Pretend do some work (step 3)	   ##
######################################


=h
tie %session, "Apache::Session::MySQL", $sess_id,
	{
		Handle => $db_handle,
		LockHandle => $db_handle
	};
=cut

=sessionstry
my $sess_id;
my %session;
my %session;
tie %session, "Apache::Session::MySQL";
$session{url} = $ENV{'HTTP_REFERER'};
$sess_id = $session{_session_id};

my %session;
tie %session, "Apache::Session::MySQL", $sess_id;

#print "counter value: $session{url}\n";
#print $sess_id;
=cut
$count_only = $cgi_object->param("count_only");
$book = $cgi_object->param("book");
#$phrase = uri_escape($cgi_object->param("phrase"));
$phrase = encode_entities($cgi_object->param("phrase"));
$searchOrder = $cgi_object->param("searchOrder");
$searchResultsPP = $cgi_object->param("searchResultsPP");
$bool = $cgi_object->param("bool");
$cnumParam = $cgi_object->param("cnum");
$bookParam = $cgi_object->param("book");
$vnumParam = $cgi_object->param("vnum");
$translation = $cgi_object->param("translation");
$flag = $cgi_object->param("flag");
if ($cgi_object->param("cnum"))
{
	$goBack = $ENV{'HTTP_REFERER'};
	#print $goBack;
}


#print $goBack;
#print "<br / >" .encode_entities($cgi_object->param("phrase"), '"'). "<br />";
#$phrase = encode_entities($cgi_object->param("phrase"));
%forms = $cgi_object->Vars; # all post form data inside %forms
#print $cgi_object->header();
foreach (keys %forms)
{
	#print "$_ = $forms{$_} ";
}
#?phrase='.urlencode($searched).'&book='.urlencode($_GET['book']).'&cnum='.$cnum.'&choice=Search&searchOrder='.urlencode($_GET['searchOrder']).'&searchResultsPP='.urlencode($_GET['searchResultsPP']).'&count_only='.urlencode($_GET['count_only']).'&bool='.urlencode($_GET['bool']).'&page=';
#$URIGetVals = "?phrase=" .uri_escape($phrase). "&book=" .uri_escape($book). "&choice=Search&count_only=" .uri_escape($count_only). "&page=";
#$URIGetVals = "?phrase=" .$phrase. "&book=" .$book. "&choice=Search&count_only=" .$count_only. "&page=";

#print $URIGetVals . "\n";
#$URIGetVals = $ENV{'SCRIPT_NAME'} . "?" . $ENV{'QUERY_STRING'} . "&page=";
$home = $ENV{'SCRIPT_NAME'};
#$URIGetVals = $ENV{'SCRIPT_NAME'} . "?phrase=" .$phrase. "&book=" .$book. "&choice=Search&searchOrder=".$searchOrder. "&searchResultsPP=" .$searchResultsPP."&count_only=" .$count_only. "&bool=" .$bool. "&page=";
$URIGetVals = $ENV{'SCRIPT_NAME'} . "?phrase=" .$phrase. "&book=" .$book. "&choice=Search&translation=".$translation. "&searchOrder=".$searchOrder. "&searchResultsPP=" .$searchResultsPP."&count_only=" .$count_only. "&bool=" .$bool. "&cnum=" .$cnumParam. "&flag=" . $vnumFlag ."&page=";

#print $URIGetVals;
#print $ENV{'REQUEST_URI'};
=head
$query = CGI->new;

%data = $query->Vars;
#print $query->header();
#foreach my $param (keys %data)
#{
#	print "$param = $data{$param}\n";
#}
=cut
$and = "";
if ($book eq 'A')
	{
		$and = "";
	}
elsif ($book eq 'O')
	{
		$and = " AND bsect = 'O' ";
	}
elsif ($book eq 'N')
	{
		$and = " AND bsect = 'N' ";
	}
elsif ($book)
	{
		$and = " AND bnum = $book ";
	}

$orderBy = " ORDER BY relevance ";
$records[0] = {
		section=>'A',
		label=>'Entire Bible'
	};

# $query = "SELECT bsect, bname, bnum FROM kjv_bookmap WHERE bsect = ? ORDER BY bnum";
my $query = "SELECT bsect, bname, bnum FROM kjv_bookmap ORDER BY bnum";
my $query_handle = $db_handle->prepare($query);
#$query_handle->bind_param(1, \$bsect);
=head
foreach my $key (%sect_names)
{
	$bsect = $sect_names{$key};
#    print $bsect;
} 
=cut
$i = 1 ;
$query_handle->execute();
$query_handle->bind_columns(\$bsect, \$bname, \$bnum);
while (my $ref = $query_handle->fetchrow())
{
	push(@records, {number=>$i,section=>$bsect,label=>$sect_names{$bsect},name=>$bname});
	$i++;
}
=h
$searchRecords[0] = {
		rowid=> 0,
		bsect=> 0,
		bname=> 0,
		bnum=> 0,
		cnum=> 0,
		vnum=> 0,
		vtext=> 0
	};
=cut	
$searched = $phrase;
if ($cgi_object->param("bool"))
{
	$searched = $cgi_object->param("phrase");
}

#highlightWords("hello world hello dood", "hello dood");
#my $tempSearched = $searched;
my $tempSearched = decode_entities($searched);
$tempSearched =~ s/^"(.*)"$/$1/g;
#print "$searched";
my @split  = split(undef, $tempSearched);
my $words = "";
foreach my $val (@split)
{
	if ($val >= 'a' && $val <= 'z' || $val >= 'A' && $val <= 'Z' || $val == ' ')
	{
		$words .= $val;
	}
}
#print $tempSearched;
#printf $words;

$offset = 0;
$resultsPP = 10;
$orderBy = " ORDER BY relevance ";
if ($cgi_object->param("searchResultsPP"))
{
	$resultsPP = $cgi_object->param("searchResultsPP");
}
if($cgi_object->param("searchOrder") eq 'N')
{
	$orderBy = "ORDER BY bnum ";
}
elsif($cgi_object->param("searchOrder") eq 'A')
{
	$orderBy = "ORDER BY bname ASC ";
}
$pageNow = (!$cgi_object->param("page"))?1:$cgi_object->param("page");
$offset = (($pageNow-1)*$resultsPP);
$limit = "LIMIT $offset, $resultsPP";
=h
$numRowsSearched = $rowsSearched->num_rows;
	$totalPages = ceil($numRowsSearched/$resultsPP);
	$offset = (($pageNow-1)*$resultsPP);
=cut

#my $resultsQuery = "SELECT bsect, bname, bnum, cnum, vnum, vtext, MATCH(bname, vtext) AGAINST ('".$searched."' IN BOOLEAN MODE) AS relevance FROM kjv WHERE MATCH (bname, vtext) AGAINST ('".$searched."' IN BOOLEAN MODE) ".$and." ".$orderBy;
#print "here = " . $searched . "</br />";
if ($cgi_object->param("cnum") && $cgi_object->param("book"))
{
	$book = $cgi_object->param("book");
	#$and .= " AND $book = bnum ";
	$cnumR = $cgi_object->param("cnum");
	$and .= " AND $cnumR = cnum ";
}
#print $and;
my $resultsQuery = "SELECT bsect, bname, bnum, cnum, vnum, vtext, MATCH(bname, vtext) AGAINST ('$searched' IN BOOLEAN MODE) AS relevance FROM $translation WHERE MATCH (bname, vtext) AGAINST ('$searched' IN BOOLEAN MODE) ".$and." ".$orderBy;
my $resultsQuery_handle = $db_handle->prepare($resultsQuery);
$resultsQuery_handle->execute();
$numRowsSearched = $resultsQuery_handle ->rows;
$totalPages = ceil($numRowsSearched/$resultsPP);
$offset = (($pageNow-1)*$resultsPP);
=h
my $searchQuery = "SELECT \@rownum:=\@rownum+1 rownum, bsect, bname, bnum, cnum, vnum, vtext, MATCH(bname, vtext) AGAINST ('".$searched."' IN BOOLEAN MODE) AS relevance FROM (SELECT \@rownum:=0) row, kjv WHERE MATCH (bname, vtext) AGAINST ('".$searched."' IN BOOLEAN MODE) ".$and." ".$orderBy." ".$limit;
=cut
my $searchQuery;
if ($flag eq 1)
{
	$vnumR = $cgi_object->param("vnum");
	$and .= " AND $vnumR = vnum ";
	foreach my $t(keys %translations)
	{
		if ($t ne $cgi_object->param("translation"))
			{
			$searchQuery = "SELECT \@rownum:=\@rownum+1 rownum, bsect, bname, bnum, cnum, vnum, vtext, MATCH(bname, vtext) AGAINST ('$searched' IN BOOLEAN MODE) AS relevance FROM (SELECT \@rownum:=0) row, $t WHERE MATCH (bname, vtext) AGAINST ('$searched' IN BOOLEAN MODE) ".$and." ".$orderBy." ".$limit;
			#print $searchQuery . "<br /><br/>";
			my $sqh = $db_handle->prepare($searchQuery);
			$sqh->execute();
			$sqh->bind_columns(\$rownum, \$bsectR, \$bnameR, \$bnumR, \$cnumR, \$vnumR, \$vtextR);
			while (my $ref = $sqh->fetchrow())
			{
				$resultURIs = $ENV{'SCRIPT_NAME'} . "?phrase=" .$phrase."&book=" .$bnumR. "&choice=Search&translation=".$t. "&searchOrder=".$searchOrder. "&searchResultsPP=" .$searchResultsPP."&count_only=" .$count_only. "&bool=" .$bool. "&cnum=" . $cnumR ."&vnum=" . $vnumR. "&flag=" . $vnumFlag ."&page=";
				#print $resultURIs . "<br />";
				push(@compTrans, {rowid=>$rownum+1,bsect=>$bsectR,bname=>$bnameR,cnum=>$cnumR,vnum=>$vnumR,vtext=>highlightWords($vtextR,$words),transURI=>$resultURIs,translation=>$translations{$t}});
				#print $vtextR . "<br />";
=h
				if (!$cgi_object->param("vnum"))
				{
					foreach (keys %translations)
					{
						if ($_ ne $cgi_object->param("translation"))
						{
							push(@compTrans, {rowid=>$rownum+1,bsect=>$bsectR,bname=>$bnameR,cnum=>$cnumR,vnum=>$vnumR,vtext=>highlightWords($vtextR,$words),transURI=>$resultURIs,translation=>$translations{$_}});
						}
					}
				}
=cut
			}
		}
	}
}
else
{
$searchQuery = "SELECT \@rownum:=\@rownum+1 rownum, bsect, bname, bnum, cnum, vnum, vtext, MATCH(bname, vtext) AGAINST ('$searched' IN BOOLEAN MODE) AS relevance FROM (SELECT \@rownum:=0) row, $translation WHERE MATCH (bname, vtext) AGAINST ('$searched' IN BOOLEAN MODE) ".$and." ".$orderBy." ".$limit;

my $searchQuery_handle = $db_handle->prepare($searchQuery);
$searchQuery_handle->execute();
$searchQuery_handle->bind_columns(\$rownum, \$bsectR, \$bnameR, \$bnumR, \$cnumR, \$vnumR, \$vtextR);
while (my $ref = $searchQuery_handle->fetchrow())
{
	$vnumFlag = 1;
	$resultURIs = $ENV{'SCRIPT_NAME'} . "?phrase=" .$phrase."&book=" .$bnumR. "&choice=Search&translation=".$translation. "&searchOrder=".$searchOrder. "&searchResultsPP=" .$searchResultsPP."&count_only=" .$count_only. "&bool=" .$bool. "&cnum=" . $cnumR ."&vnum=" . $vnumR. "&page=";

	$transURIs = $ENV{'SCRIPT_NAME'} . "?phrase=" .$phrase."&book=" .$bnumR. "&choice=Search&translation=".$translation. "&searchOrder=".$searchOrder. "&searchResultsPP=" .$searchResultsPP."&count_only=" .$count_only. "&bool=" .$bool. "&cnum=" . $cnumR ."&vnum=" . $vnumR."&flag=" . $vnumFlag . "&page=";
	#push(@searchRecords, {rowid=>$rownum+1,bsect=>$bsectR,bname=>$bnameR,cnum=>$cnumR,vnum=>$vnumR,vtext=>$vtextR});

	if (!$cgi_object->param("vnum"))
	{
		foreach (keys %translations)
		{
			if ($_ ne $cgi_object->param("translation"))
			{
				push(@compTrans, {rowid=>$rownum+1,bsect=>$bsectR,bname=>$bnameR,cnum=>$cnumR,vnum=>$vnumR,vtext=>highlightWords($vtextR,$words),transURI=>$transURIs,translation=>$translations{$_}},flag=>1);
				$vnumFlag = 1;
			}
		}
	}
	if($cgi_object->param("cnum") && $cgi_object->param("book"))
	{
		push(@searchRecords, {rowid=>$rownum+1,bsect=>$bsectR,bname=>$bnameR,cnum=>$cnumR,vnum=>$vnumR,vtext=>highlightWords($vtextR,$words)});
		#push(@compTrans, {rowid=>$rownum+1,bsect=>$bsectR,bname=>$bnameR,cnum=>$cnumR,vnum=>$vnumR,vtext=>highlightWords($vtextR,$words),transURI=>$resultURIs,translation=>$translations{$_}},flag=>1);
	}
	else
	{
		push(@searchRecords, {rowid=>$rownum+1,bsect=>$bsectR,bname=>$bnameR,cnum=>$cnumR,vnum=>$vnumR,vtext=>highlightWords($vtextR,$words),uri=>$resultURIs});
	}
	#print $resultURIs . "<br / >";
}
}
#print $cgi_object->param("flag");
=h
if ($cgi_object->param("translation") && !$cgi_object->param("vnum"))
{
my $v = $cgi_object->param("vnum");
$and .= "AND vnum = $v";
my $sq2 = "SELECT \@rownum:=\@rownum+1 rownum, bsect, bname, bnum, cnum, vnum, vtext, MATCH(bname, vtext) AGAINST ('$searched' IN BOOLEAN MODE) AS relevance FROM (SELECT \@rownum:=0) row, $translation WHERE MATCH (bname, vtext) AGAINST ('$searched' IN BOOLEAN MODE) ".$and." ".$orderBy." ".$limit;
my $sq2_h = $db_handle->prepare($sq2);
$sq2_h->execute();
$sq2_h->bind_columns(\$rownum, \$bsectR, \$bnameR, \$bnumR, \$cnumR, \$vnumR, \$vtextR);
while (my $ref = $sq2_h->fetchrow())
{
	$transURIs = $ENV{'SCRIPT_NAME'} . "?phrase=" .$phrase."&book=" .$bnumR. "&choice=Search&translation=".$translation. "&searchOrder=".$searchOrder. "&searchResultsPP=" .$searchResultsPP."&count_only=" .$count_only. "&bool=" .$bool. "&cnum=" . $cnumR ."&vnum=" . $vnumR. "&page=";
	#push(@searchRecords, {rowid=>$rownum+1,bsect=>$bsectR,bname=>$bnameR,cnum=>$cnumR,vnum=>$vnumR,vtext=>$vtextR});
	if ($cgi_object->param("cnum") && $cgi_object->param("book"))
	{
		push(@compTrans, {rowid=>$rownum+1,bsect=>$bsectR,bname=>$bnameR,cnum=>$cnumR,vnum=>$vnumR,vtext=>highlightWords($vtextR,$words)});
	}
	else
	{
		push(@compTrans, {rowid=>$rownum+1,bsect=>$bsectR,bname=>$bnameR,cnum=>$cnumR,vnum=>$vnumR,vtext=>highlightWords($vtextR,$words),uri=>$resultURIs});
	}
	if($cgi_object->param("translation") && $cgi_object->param("vnum") || $cgi_object->param("cnum") && $cgi_object->param("book"))
	{
		push(@compTrans, {rowid=>$rownum+1,bsect=>$bsectR,bname=>$bnameR,cnum=>$cnumR,vnum=>$vnumR,vtext=>highlightWords($vtextR,$words),uriT=>$transURIs});
	}
	print $transURIs . "<br / >";
}
}
=cut





$curPageURI = $URIGetVals . $pageNow;

for (my $i = 1; $i <= $totalPages; $i++)
{
	$pageURIs{$i} = $URIGetVals . $i;
	#print $pageURIs{$i} . "<br \>";
}

$showLeft = 3;
$showRight = 3;
$visible = $showLeft + $showRight;
if ($totalPages > 1)
{
	for(my $page=$pageNow-$showLeft; $page < $totalPages+1 && $page<=$pageNow+$showRight; $page++)
	{
		if ($page > 0 && $page < $totalPages+1 )
		{
			$visiblePages{$page} = $URIGetVals . $page;
		}
		if($pageNow != $page && $page != 0 && $page < $totalPages+1 && $page>0)
		{
			$visiblePages{$page} = $URIGetVals . $page;
		}
	}
}

if ($pageNow != 1)
{
	$prevPage = $URIGetVals . ($pageNow-1);
	if ($pageNow-10 >= 1)
	{
		$prevBulk = $URIGetVals . ($pageNow-10)
	}
}
if ($pageNow != $totalPages)
{
	$nextPage = $URIGetVals . ($pageNow+1);
	if ($pageNow+10 < $totalPages)
	{
		$nextBulk = $URIGetVals . ($pageNow+10)
	}
}

$pageN = $pageNow + 10;
$pageP = $pageNow - 10;
$first = $URIGetVals . 1;
$last = $URIGetVals . $totalPages;
foreach (keys %pageURIs)
{
	#print "$_ = $pageURIs{$_} ";
}

###################################### 
## Prep vars for template (step 4a) ##
######################################

$vars =
{
	books=>\%selectBooks,
	sect_names=>\%sect_names,
	records=>\@records,
	forms=>\%forms,
	count_only=>$count_only,
	book=>$book,
	phrase=>$phrase,
	bool=>$bool,
	searchRecords=>\@searchRecords,
	compTrans=>\@compTrans,
	numSearched=>$numRowsSearched,
	pageURIs=>\%pageURIs,
	resultsPP=>$resultsPP,
	totalPages=>$totalPages,
	pageNow=>$pageNow,
	prevPage=>$prevPage,
	nextPage=>$nextPage,
	visiblePages=>\%visiblePages,
	curPageURI=>$curPageURI,
	prevBulk=>$prevBulk,
	nextBulk=>$nextBulk,
	pageN=>$pageN,
	pageP=>$pageP,
	first=>$first,
	last=>$last,
	home=>$home,
	searchOrder=>$searchOrder,
	searchOrderSelect=>\%searchOrder,
	searchResultsPP=>$searchResultsPP,
	searchResultsPPSelect=>\%searchResultsPP,
	cnumParam=>$cnumParam,
	bookParam=>$bookParam,
	vnumParam=>$vnumParam,
	goBack=>$goBack,
	flag=>$flag,
	translations=>\%translations,
	translation=>$translation,
	#sections=>\%sections,
};

###################################### 
## Bind and pass flow (step 4b + 5) ##
######################################
$tt_object->process ( $template, $vars ) 
	or die( $tt_object->error() );

   
######################################

__END__



