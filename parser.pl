#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;
use SQLite::DB;

my %GSTAT;
my %RES;
my @failed;
my %LOG;

# parse header
while (<>) {
	if (m/^# (\w+):\s+(\d+)/) {
		$GSTAT{$1} = $2;
		next;
	}
	last if (m/contents/);
}

my $log = "";

while (my $line = <>) {

	if ($line =~ m|^FAIL: .*tests/(\w+)|) {
		# read a single test
		<>;<>; # discard two empty lines
		my $test = $1;
		push(@failed, $test);
		while ($line = <>) {
			$log .= $line;
			chomp($line);

			if ($line =~ m/debug\| Platform: (.*)$/) {
				$GSTAT{arch} = $1;
			}
			if ($line =~m/revision\s(\w+)/){
				$GSTAT{rev} = $1;
			}
			if ($line =~ m/^#\s+top\s+TEST .*FAILED \(([^)]+)\)/) {
				$LOG{$test}{runtime} = $1;
			}

			if ($line =~ m/^FAIL/) {
				$LOG{$test}{log} = $log;
				$log = "";
				last;
			}
		}
	} 

my $db = SQLite::DB->new("stats.sqlite");
$db->connect() or die($!);
$db->transaction_mode;

$db->exec("insert into batches (arch,rev,timestamp,error,xfail,pass,skip,total,xpass,fail) 
	VALUES (?,?,?,?,?,?,?,?,?,?)", 
	$GSTAT{'arch'}, $GSTAT{'rev'},time(),$GSTAT{'ERROR'}, $GSTAT{'XFAIL'},$GSTAT{'PASS'},
	$GSTAT{'SKIP'}, $GSTAT{'TOTAL'}, $GSTAT{'XPASS'}, $GSTAT{'FAIL'});
my $batchd  =  SQLite::DB::last_insert_rowid;

for my $test (keys %LOG){
	print "Inserting test $test\n";
	$db->exec("insert into failures (test,runtime,log) values (?,?,?)",
			   $test, $LOG{$test}{'runtime'}, $LOG{$test}{'log'});
}

$db->commit || print $db->get_error."\n";
