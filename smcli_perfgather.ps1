# IBM SMCli (DS Storage) performance monitoring script

# Windows PowerShell

# EJ; September 2013



#### IBM smcli must be in system path



####################

## control block - your input goes here!

## All of these values are required.

# management IP addresses for storage system controllers

$cont_A_IP = "10.134.3.65"

$cont_B_IP = "10.134.3.67"



# storage system name

$arrayname = "USUS1SAN1020_room2"



# destination file - will be appended.  Fully qualified path is a requirement.  Script output to this file is typically in CSV format.

$destfile = "D:\smcli_performance_data\USUS1SAN1020_room2.csv"



# root file system of your destination in $destfile - e.g. "D:", "\\foo\bar" etc

$destroot = "D:"



## end control block

####################



if ( ( $cont_A_IP -or $cont_B_IP -or $arrayname -or $destfile ) -eq $null ) {

    echo "Missing required value from control block!"

    echo "Exiting."

    exit 2

}



# check for disk space

# if less than 10% or 250MB remaining script will fail

$mhost = hostname

$cur_root = get-wmiobject -class win32_logicaldisk -computername $mhost -filter "Name = $destroot"

if ( ( $cur_root.FreeSpace / $cur_root.Size ) -lt 0.1 ) {

    echo "Less than ten percent disk space remaining!  Script will not run."

    echo "No operations performed."

    echo "Exiting."

    exit 4

}

elseif ( $cur_root.FreeSpace -lt 262144000 ) {

    echo "Less than 250MB disk space remaining!  Script will not run."

    echo "No operations performed.  Exiting."

    exit 5

}



# is smcli available?  if so, pull data from it

if ( Get-Command smcli ) {

    $smcli_output = smcli $cont_A_IP $cont_B_IP -n $arrayname -c "show allLogicalDrives performanceStats;"

    # parse your crap into smcli and modify it into something tabular!

    # totally tabular dude!

    $curtime = Get-Date

    $cnt = 0

    foreach ( $i in $smcli_output ) {

        if ( ( $i -cmatch "^CONTROLLER" ) -or ( $i -cmatch "^Logical Drive " ) -or ( $i -cmatch "^STORAGE SUBSYSTEM TOTALS" ) ) {

            echo "$arrayname,$curtime,$cont_A_IP,$cont_B_IP,$i" >> $destfile

        }

    }

    # dump to console (troubleshooting purposes, etc)

    echo "!!!! RAW smcli OUTPUT FOLLOWS !!!!"

    echo $smcli_output

}

else {

    echo "smcli not found; aborting.  smcli must be in path!"

    echo "Exiting."

    exit 1

}



## destination file rollover?

$dlength = (Get-Item "$destfile").length

# default $dlength == 50MB - file will be rolled over at this size

if ( $dlength > 52428800 ) {

    $m = 0

    # where is 7-zip?

    if ( Get-Command '7z.exe' ) {

        $m = 1

    }

    elseif ( Get-Command 'C:\Program Files\7-Zip\7z.exe' ) {

        $m = 3

    }

    else {

        echo "7zip not found; file at $destfile cannot be rolled over"

    }

    if ( $m -gt 0 ) {

        $month = $curtime.Month

        $day = $curtime.Day

        $year = $curtime.Year

        $rollname = "$destfile.$month-$day-$year.zip"

        if ( ( Test-Path $rollname ) -eq False ) {

            if ( $m -eq 1 ) {

                & '7z.exe' a -t zip $rollname $destfile

            }

            elsif ( $m -eq 3 ) {

                & 'C:\Program Files\7-Zip\7z.exe' a -tzip $rollname $destfile

            }

            else {

                echo "Error - invalid value for 7zip path marker variable.  Please check code - terminating."

                exit 3

            }

            echo "$destfile rolled over to $rollname"

            rm $destfile

        }

        else {

            echo "$destfile rolled over in > 24 hours!"

            echo "Recommend to run script manually to detect any errors, reduce scheduled frequency, or raise default $dlength var"

        }

    }

}



exit 0