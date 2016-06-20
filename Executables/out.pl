#!/usr/bin/perl -s


#mac - tag address scanned
#time - time the tag was scanned
#stand - whether the person is entering or leaving
#location - where the scanner is located. pse321

$_ = $time;
@ti = split(/:/);
$hour = $ti[0];
$min  = $ti[1];
$location = 'pse321';
$stand = $stand;

exec("java -jar b.jar $mac $hour $min $location" );


