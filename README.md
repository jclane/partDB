# SubHunt

Originally I was using a MS Access database to keep track of various PC parts currently in our main database.  The main parts database does not allow me to narrow parts down to their specs.  A CPU is a CPU is a CPU you might say.  This made finding parts that could be subbed for one another tedious.  This app allows me to input part numbers and their specifications making that task much more efficient (and without the performance issues I had with MS Access).

## Jun. 12 2019
Added the ability to export results in treeview of "browse" page.

### Jun. 11 2019
Finally added a "browse" page so I can see everything in the database (and filter it!).

### Dec. 11 2018
I've been using this fairly regularly now, but eventually I got tired of manually pulling the part orders report and using a VBA script to get a list of harddrives, memory, and CPUs to check.  I've not added an "Auto Hunt" feature under search that will pull the report, match parts on order against the all known HDDs, CPUs, and MEM and finally check if they need to be added to the database or need sub.  If so, they will be saved to an Excel file along with the order number (for non-warranty) so the part can be reordered once the sub has been added.

Also, the progress bar took longer than I'd like to admit.

### Nov. 14 2018
Added the ability to confirm if two part numbers are valid subs (using the GUI).  Also added docstrings for all functions.

### Nov. 12 2018
I was able to find a one-size-fits-all solution the part editing issue.  Classes for the parts were created, but have not been uploaded as there is currently no use for them.

Code is still ugly.

### Nov. 9 2018
Fixed various issues (formatting, parts not showin up on list_subs after being added via GUI, others).  Started working on allowing users to edit part information/records.  I've realized if I continue with the this the way things are written I'll have to write different functions so users can edit the various part types.  I was hoping for a one-size-fits-all solution.

Currently entertaining the idea of creating classes for each part type (HDD, SSD, SSHD, MEM, CPU) and let them handle the adding/editing rather than continue down this path.  I'll likely have to either way, the code is getting hard to read.

### Nov. 8 2018
Most functions have been implemented.  I need to improve error handling and the aesthetics of the UI.

### Oct. 18 2018
The limitations of shelve became apparent as the application was developed enough to actually become useful.  Most of the original backend code has been scrapped and SQLite3 is being implemented.

### Oct. 17 2018
Initial upload.
