#!/usr/bin/perl -w
# use strict;

my $filename = 'yields.dat';

open (IN, "$ARGV[0]");
open (FH, ">", $filename) or die $!;

$getit = 0;

LINE:
while (<IN>) {
   $line = $_;
   chomp ($line);

   if ($line =~ /INTEGRATED\sYIELDS/) {
      $getit = 1;
      next LINE;
   }

   #elsif (($line =~ /ENERGY\sRANGE/) and ($getit == 1)) {
	 elsif (($line =~ /ENERGY\s+?/) and ($getit == 1)) {

			#print "i get here\n";

      if ($line =~ /SCATTERING\sANGLE\sRANGE/) {
         $line =~ s/.+SCATTERING\sANGLE\sRANGE\s+//;
         $value1 = $line;
         $value1 =~ s/\-.+//;
         $value2 = $line;
         $value2 =~ s/.+\-\-\-\s//;
         $value2 =~ s/\s.+//;

         $value3 = ($value1 + $value2)/2;
 
         next LINE;
      } 

      else {
         $line =~ s/.+THETA\s+//;
         $value3 = $line;
         $value3 =~ s/\s.+//;

         next LINE;
      }
         
   }
   
   elsif (($line =~ /^(\s+2\s+)/) and ($getit == 1)) {
      $line =~ s/\s+/\t/g;
      @line_list = split (/\t/, $line);

      $value4 = $line_list[5];

			#print "$value3 $value4\n";
      print FH "$value3 $value4\n";

			$getit = 0;
      next LINE;
   }

   else {
      next LINE;
   }
}

close(FH);
